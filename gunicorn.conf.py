import os
from pathlib import Path


chdir = str(Path(__file__).resolve().parent)
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
workers = int(os.getenv("GUNICORN_WORKERS", "3"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "30"))
accesslog = "-"
errorlog = "-"
capture_output = True
wsgi_app = "config.wsgi:application"
