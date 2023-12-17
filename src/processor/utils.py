from multiprocessing import Queue
from queue import Empty
from time import sleep


def _wait_for_tasks_to_complete(task_ids: set[str], queue: Queue):
    while task_ids:
        try:
            task_id = queue.get_nowait()
            if task_id:
                task_ids.remove(task_id)
        except Empty:
            pass
        sleep(0.0001)
    return True
