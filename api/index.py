import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')

try:
    # Get the Django WSGI application
    django_application = get_wsgi_application()
    print("Django application loaded successfully")
except Exception as e:
    print(f"Error loading Django application: {e}")
    print(traceback.format_exc())

# Vercel serverless function handler
def handler(environ, start_response):
    try:
        print(f"Request received: {environ.get('PATH_INFO', '/')}")
        return django_application(environ, start_response)
    except Exception as e:
        print(f"Error in handler: {e}")
        print(traceback.format_exc())
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [f"Error: {str(e)}".encode()]

# Export the handler for Vercel
app = handler
