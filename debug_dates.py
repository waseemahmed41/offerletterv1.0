#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from django.utils import timezone
import pandas as pd

def debug_dates():
    """Debug date validation"""
    print("Current timezone info:")
    print(f"Current timezone: {timezone.get_current_timezone()}")
    print(f"Current time: {timezone.now()}")
    print(f"Current date: {timezone.now().date()}")
    
    print("\nCSV Date Analysis:")
    df = pd.read_csv('test_bulk_upload.csv')
    
    for index, row in df.iterrows():
        joining_date = pd.to_datetime(row['joining_date']).date()
        current_date = timezone.now().date()
        
        print(f"Row {index + 1}:")
        print(f"  Joining date: {joining_date}")
        print(f"  Current date: {current_date}")
        print(f"  Is future: {joining_date > current_date}")
        print(f"  Days difference: {(joining_date - current_date).days}")
        print()

if __name__ == '__main__':
    debug_dates()
