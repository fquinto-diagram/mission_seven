import redis
from celery import Celery
import os
from app.modules.common.models import load_models
from app.config.log import setup_logger

celery = Celery(
    "app",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
    include=[
        "app.modules.roles.tasks",
        "app.modules.companies.tasks"
    ]
)
load_models()
setup_logger()

celery.autodiscover_tasks(["app.modules"])

redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=os.getenv("REDIS_DB"), password=os.getenv("REDIS_PASSWORD"), decode_responses=True)
