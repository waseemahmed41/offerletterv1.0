import os
import sys
from django.core.wsgi import get_wsgi_application

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')

# Get Django application
django_app = get_wsgi_application()

# Vercel serverless function handler
def handler(request):
    return django_app(request)

# Export for Vercel
app = handler
