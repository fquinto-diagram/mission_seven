from app.config.worker import celery

class WorkerAdapter:
    def __init__(self):
        self.celery = celery

    def send(self, task_name: str, args: list = None, queue: str = None, kwargs: dict = None):
        return self.celery.send_task(task_name, args=args, queue=queue, kwargs=kwargs)
    
    def delay(self, task_name: str, args: list = None, queue: str = None, kwargs: dict = None):
        return self.celery.delay(task_name, args=args, queue=queue, kwargs=kwargs)
    
    def apply_async(self, task_name: str, args: list = None, queue: str = None, kwargs: dict = None):
        return self.celery.apply_async(task_name, args=args, queue=queue, kwargs=kwargs)
    
    def apply(self, task_name: str, args: list = None, queue: str = None, kwargs: dict = None):
        return self.celery.apply(task_name, args=args, queue=queue, kwargs=kwargs)
    

worker_adapter = WorkerAdapter()
    
    
