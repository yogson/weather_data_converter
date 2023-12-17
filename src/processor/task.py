import logging
from multiprocessing import Queue
from queue import Empty
from time import sleep
from typing import Callable, Any

from settings import LOG_LEVEL
from utils.common import init_logger

task_function = Callable[[Any, dict[str, Any]], bytes | None]

logger = init_logger(__name__)


class Task:
    def __init__(self, _id: str, context: dict[str, Any], pipeline: list[task_function]):
        self.id = _id
        self.context = context
        self.pipeline = pipeline
        self._payload = None
        self.completed = False

    def run(self):
        for target in self.pipeline:
            try:
                self._payload = target(self._payload, self.context)
            except Exception as e:
                logger.error(f"{self.id}, {target.__name__}, {e}")
                return
        self.completed = True


def simple_worker(*args, task_queue: Queue, result_queue: Queue):
    while True:
        task = None
        try:
            task = task_queue.get(timeout=1)
        except Empty:
            pass
        if isinstance(task, Task):
            task.run()
            result_queue.put(task.id)
        sleep(0.0001)
