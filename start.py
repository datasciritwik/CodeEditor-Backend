import os

workers = os.getenv("WEB_CONCURRENCY") or os.getenv("WORKERS") or "1"
timeout = os.getenv("GUNICORN_TIMEOUT", "120")
bind = os.getenv("BIND", "0.0.0.0:8080")
app_module = os.getenv("APP_MODULE", "app.main:app")
log_level = os.getenv("GUNICORN_LOG_LEVEL", "info")

cmd = [
    "gunicorn",
    "-k", "uvicorn.workers.UvicornWorker",
    app_module,
    "--bind", bind,
    "--workers", str(workers),
    "--timeout", str(timeout),
    "--log-level", log_level,
]

# Replace current process with gunicorn
os.execvp(cmd[0], cmd)