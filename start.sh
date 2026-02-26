#!/usr/bin/env python
"""
Render startup script for Django application
"""

import os
import subprocess
import sys

def main():
    """Main entry point for Render deployment"""
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
    
    # Collect static files
    print("Collecting static files...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error collecting static files: {e}")
        sys.exit(1)
    
    # Run database migrations
    print("Running database migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        sys.exit(1)
    
    # Start Gunicorn
    print("Starting Gunicorn server...")
    cmd = [
        'gunicorn',
        '--config', 'gunicorn_config.py',
        'offer_automation.wsgi:application'
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Gunicorn: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
