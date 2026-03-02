#!/usr/bin/env python
"""
Gunicorn configuration for Render deployment
Optimized for web requests only (heavy processing handled by Celery)
"""

import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"

# Worker processes - optimized for web requests
workers = int(os.getenv('WEB_CONCURRENCY', '2'))  # Use 2 workers as per render.yaml
worker_class = "sync"
worker_connections = 1000
timeout = 60  # Reduced since heavy processing is now async
graceful_timeout = 30
keepalive = 2

# Worker lifecycle
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Memory optimization
worker_memory_limit = 512 * 1024 * 1024  # 512MB limit
worker_tmp_dir = "/dev/shm"  # Use RAM disk for temp files

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "offer_automation"

# Server mechanics - Optimized for Render
daemon = False
pidfile = None  # Let Render manage process
user = None
group = None
tmp_upload_dir = None

# SSL - Not needed for Render (handled by load balancer)
keyfile = None
certfile = None

# Django settings
raw_env = [
    f'DJANGO_SETTINGS_MODULE=offer_automation.settings',
]

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
