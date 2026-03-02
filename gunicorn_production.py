import os

# Production-optimized configuration for Render
# Designed for heavy Google Docs API operations

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"

# Worker processes - Ultra conservative for stability
workers = 1  # Single worker to prevent memory conflicts
worker_class = "sync"
worker_connections = 500  # Reduced connections
timeout = 600  # 10 minutes for Google Docs API
graceful_timeout = 600  # Graceful shutdown
keepalive = 2

# Aggressive memory management
max_requests = 50  # Very aggressive restarts
max_requests_jitter = 10
preload_app = True

# Memory optimization
worker_memory_limit = 400 * 1024 * 1024  # 400MB limit (conservative)
worker_tmp_dir = "/tmp"  # Use standard temp dir

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "offer_automation"

# Server mechanics - Production ready
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL - Not needed for Render
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
