#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from offers.utils import process_bulk_upload
from accounts.models import User
from django.core.files import File

def debug_bulk_upload():
    """Debug bulk upload functionality"""
    print("Debugging bulk upload...")
    
    # Get admin user
    try:
        admin_user = User.objects.get(username='admin')
        print(f"Using admin user: {admin_user.username}")
    except User.DoesNotExist:
        print("Admin user not found!")
        return
    
    # Test with the actual CSV file
    csv_file_path = 'test_bulk_upload.csv'
    
    try:
        with open(csv_file_path, 'rb') as f:
            file_obj = File(f, name='test_bulk_upload.csv')
            
            print(f"File name: {file_obj.name}")
            print(f"File size: {file_obj.size}")
            
            # Process bulk upload
            candidates, errors = process_bulk_upload(file_obj, admin_user)
            
            print(f"Candidates returned: {candidates}")
            print(f"Errors returned: {errors}")
            
            if candidates is None:
                print("❌ process_bulk_upload returned None")
                if errors:
                    print(f"Error details: {errors}")
            else:
                print(f"✅ Successfully processed {len(candidates)} candidates")
                if errors:
                    print(f"⚠️  But encountered {len(errors)} errors")
                    for error in errors:
                        print(f"  - {error}")
    
    except Exception as e:
        print(f"❌ Exception during debug: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_bulk_upload()
