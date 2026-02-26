#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from django.db import connection

def reset_offers_migrations():
    """Reset offers migrations from SQLite database"""
    cursor = connection.cursor()
    cursor.execute('DELETE FROM django_migrations WHERE app = "offers";')
    print('Deleted offers migrations from SQLite')

if __name__ == '__main__':
    reset_offers_migrations()
