from app.modules.common.helpers.chunk_list import chunk_list
from app.adapters.worker_adapter import worker_adapter


def send_task_with_chunks(job_id: str, task_name: str, ids: list, chunk_size: int = 100):
    for i, chunk in enumerate(chunk_list(ids, chunk_size)):
        worker_adapter.send(task_name, args=[job_id, chunk, (1 + i) * chunk_size, len(ids)])