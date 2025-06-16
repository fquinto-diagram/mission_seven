import multiprocessing
import os

# Número de workers
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "uvicorn.workers.UvicornWorker"

# Bind
bind = "0.0.0.0:8000"

# Timeout
timeout = 120

# Access log
accesslog = "-"

# Error log
errorlog = "-"

# Log level
loglevel = "info"

# Preload app
preload_app = True

# Max requests
max_requests = 1000
max_requests_jitter = 50

# Graceful timeout
graceful_timeout = 120

# Keep alive
keepalive = 30 