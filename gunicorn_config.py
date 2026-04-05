"""
Configuración de gunicorn para producción
"""

import multiprocessing

# Bind
bind = "0.0.0.0:8000"
backlog = 2048

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Server mechanics
daemon = False
pidfile = None
tmp_upload_dir = None
umask = 0
user = None
group = None

# Server hooks
def on_starting(server):
    print("🌋 Iniciando servidor Seismic Analysis...")

def when_ready(server):
    print("✅ Servidor listo para recibir conexiones")

def on_exit(server):
    print("👋 Servidor detenido")

# SSL (si está disponible)
keyfile = None
certfile = None

# Performance
max_requests = 1000
max_requests_jitter = 100
