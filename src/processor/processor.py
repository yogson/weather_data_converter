import asyncio
from multiprocessing import Queue, Process, cpu_count
from pathlib import Path
from typing import Callable, Awaitable, AsyncGenerator
from uuid import uuid4

from processor.task import Task, simple_worker
from processor.utils import _wait_for_tasks_to_complete
from receivers.http_receiver import receive
from settings import TEMP_DIR, OUTPUT_DIR, CPU_CORES
from transformers import (
    uncompress_bzip,
    extract_regular_grid_data,
    save_array_and_meta,
    subtract_previous_hour,
    replace_nan_with_sentinel,
    replace_grib_missing_value_with_sentinel,
    build_wgf,
)
from transformers.loaders import write_wgf


class WeatherDataProcessor:
    receiver: AsyncGenerator[Path, str] = receive
    load_pipeline = [
        uncompress_bzip,
        extract_regular_grid_data,
        replace_nan_with_sentinel,
        replace_grib_missing_value_with_sentinel,
        save_array_and_meta,
    ]
    transform_pipeline = [
        subtract_previous_hour,
        build_wgf,
        write_wgf,
    ]

    def __init__(self, source: str):
        self.source = source
        self.workers = []
        self.task_queue = Queue()
        self.result_queue = Queue()

    def _spawn_processes(self, num_proc: int = None):
        for _ in range(num_proc or cpu_count()):
            proc = Process(
                target=simple_worker,
                kwargs={
                    "task_queue": self.task_queue,
                    "result_queue": self.result_queue,
                },
            )
            proc.daemon = True
            proc.start()

    def _set_task(self, context: dict, pipeline: list[Callable]) -> str:
        task_id = str(uuid4())
        self.task_queue.put(Task(_id=task_id, context=context, pipeline=pipeline))
        return task_id

    async def _run(self):
        task_ids = set()
        file_paths = []
        async for file_path in self.receiver(source_url=self.source):
            file_paths.append(file_path)
            context = {"source_path": file_path, "output_dir": TEMP_DIR}
            task_id = self._set_task(
                context=context,
                pipeline=self.load_pipeline,
            )
            task_ids.add(task_id)
        _wait_for_tasks_to_complete(task_ids, self.result_queue)

        file_paths.sort(key=lambda x: x.name)
        file_pairs = [
            (file_paths[i].with_suffix("").name, file_paths[i - 1].with_suffix("").name)
            for i, _ in enumerate(file_paths)
        ]
        file_pairs[0] = (file_pairs[0][0], None)
        for pair in file_pairs:
            task_id = self._set_task(
                context={"files_pair": pair, "output_dir": OUTPUT_DIR}, pipeline=self.transform_pipeline
            )
            task_ids.add(task_id)
        _wait_for_tasks_to_complete(task_ids, self.result_queue)

    def run(self):
        self._spawn_processes(CPU_CORES)
        asyncio.run(self._run())
