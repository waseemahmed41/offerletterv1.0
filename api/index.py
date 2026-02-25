import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')

# Get the Django WSGI application
application = get_wsgi_application()
