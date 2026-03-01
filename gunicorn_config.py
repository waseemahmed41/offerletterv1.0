#!/usr/bin/env python
"""
Gunicorn configuration for Render deployment
"""

import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"

# Worker processes
workers = int(os.getenv('WEB_CONCURRENCY', '1'))
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "offer_automation"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None

# Django settings
raw_env = [
    f'DJANGO_SETTINGS_MODULE=offer_automation.settings',
]

# Graceful shutdown
max_requests = 1000
max_requests_jitter = 100
preload_app = True
