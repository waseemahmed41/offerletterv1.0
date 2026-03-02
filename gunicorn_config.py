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

# Graceful shutdown - Optimized for Render
max_requests = 1000  # Increased for better handling
max_requests_jitter = 50
preload_app = True

# Worker configuration - Production optimized
workers = 1  # Fixed single worker to prevent SIGKILL
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Increased timeout for Google Docs API
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s'

# Process naming
proc_name = "offer_automation"

# Server socket
bind = "0.0.0.0:10000"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
