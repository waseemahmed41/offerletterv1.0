import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')

# Get WSGI application for Vercel
application = get_wsgi_application()
