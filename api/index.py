import os
import sys
from django.core.wsgi import get_wsgi_application

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')

# Get Django application
application = get_wsgi_application()

# Vercel serverless function handler
def handler(request):
    return application(request)

# Export the handler for Vercel
app = handler
