#!/usr/bin/env python
"""
Check project readiness for deployment
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

def check_deployment_readiness():
    """Check if project is ready for deployment"""
    print("=== DEPLOYMENT READINESS CHECK ===\n")
    
    checks = []
    
    # 1. Database Configuration
    print("1. DATABASE CONFIGURATION")
    try:
        from django.db import connection
        db_name = connection.settings_dict['NAME']
        db_engine = connection.settings_dict['ENGINE']
        print(f"   ✅ Connected to: {db_engine}")
        print(f"   ✅ Database: {db_name}")
        
        # Test basic query
        from accounts.models import User
        user_count = User.objects.count()
        print(f"   ✅ Database responsive: {user_count} users found")
        checks.append("Database: OK")
    except Exception as e:
        print(f"   ❌ Database error: {str(e)}")
        checks.append("Database: FAILED")
    
    # 2. Environment Variables
    print("\n2. ENVIRONMENT VARIABLES")
    required_vars = ['SECRET_KEY', 'DEBUG']
    optional_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: Set")
        else:
            print(f"   ⚠️  {var}: Not set (using default)")
    
    print("\n   Database Variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            masked_value = value[:4] + "***" if len(value) > 4 else "***"
            print(f"   ✅ {var}: {masked_value}")
        else:
            print(f"   ⚠️  {var}: Not set")
    
    checks.append("Environment: OK")
    
    # 3. Models and Migrations
    print("\n3. MODELS AND MIGRATIONS")
    try:
        from offers.models import Candidate, Template, OfferLetter
        from accounts.models import User
        
        # Check if models can be queried
        candidate_count = Candidate.objects.count()
        template_count = Template.objects.count()
        offer_letter_count = OfferLetter.objects.count()
        
        print(f"   ✅ Candidates: {candidate_count} records")
        print(f"   ✅ Templates: {template_count} records")
        print(f"   ✅ Offer Letters: {offer_letter_count} records")
        checks.append("Models: OK")
    except Exception as e:
        print(f"   ❌ Model error: {str(e)}")
        checks.append("Models: FAILED")
    
    # 4. Static Files and Media
    print("\n4. STATIC FILES AND MEDIA")
    try:
        from django.conf import settings
        
        static_root = settings.STATIC_ROOT
        media_root = settings.MEDIA_ROOT
        
        print(f"   ✅ STATIC_ROOT: {static_root}")
        print(f"   ✅ MEDIA_ROOT: {media_root}")
        
        # Check if directories exist
        if os.path.exists(static_root):
            print(f"   ✅ Static directory exists")
        else:
            print(f"   ⚠️  Static directory not found (will be created)")
        
        if os.path.exists(media_root):
            print(f"   ✅ Media directory exists")
        else:
            print(f"   ⚠️  Media directory not found (will be created)")
        
        checks.append("Static/Media: OK")
    except Exception as e:
        print(f"   ❌ Static/Media error: {str(e)}")
        checks.append("Static/Media: FAILED")
    
    # 5. URLs and Views
    print("\n5. URLS AND VIEWS")
    try:
        from django.urls import reverse
        from offers.views import dashboard
        
        # Test URL reversal
        dashboard_url = reverse('offers:dashboard')
        print(f"   ✅ Dashboard URL: {dashboard_url}")
        
        # Test key URLs
        key_urls = ['offers:dashboard', 'offers:bulk_upload', 'offers:create_offer', 'offers:templates']
        for url_name in key_urls:
            try:
                url = reverse(url_name)
                print(f"   ✅ {url_name}: {url}")
            except:
                print(f"   ❌ {url_name}: URL not found")
        
        checks.append("URLs: OK")
    except Exception as e:
        print(f"   ❌ URL error: {str(e)}")
        checks.append("URLs: FAILED")
    
    # 6. Security Settings
    print("\n6. SECURITY SETTINGS")
    try:
        from django.conf import settings
        
        secret_key = settings.SECRET_KEY
        debug = settings.DEBUG
        
        if len(secret_key) > 20:
            print(f"   ✅ SECRET_KEY: Set ({len(secret_key)} chars)")
        else:
            print(f"   ⚠️  SECRET_KEY: Too short ({len(secret_key)} chars)")
        
        if isinstance(debug, bool):
            print(f"   ✅ DEBUG: {debug}")
            if debug:
                print("   ⚠️  DEBUG is True (should be False in production)")
        
        checks.append("Security: OK")
    except Exception as e:
        print(f"   ❌ Security error: {str(e)}")
        checks.append("Security: FAILED")
    
    # 7. Dependencies
    print("\n7. DEPENDENCIES")
    try:
        import django
        print(f"   ✅ Django: {django.get_version()}")
        
        # Check key packages
        packages = ['pandas', 'python-docx', 'psycopg2-binary', 'sendgrid']
        for package in packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"   ✅ {package}: Installed")
            except ImportError:
                print(f"   ❌ {package}: Not installed")
        
        checks.append("Dependencies: OK")
    except Exception as e:
        print(f"   ❌ Dependency error: {str(e)}")
        checks.append("Dependencies: FAILED")
    
    # Summary
    print("\n" + "="*50)
    print("DEPLOYMENT READINESS SUMMARY")
    print("="*50)
    
    failed_checks = [check for check in checks if "FAILED" in check]
    
    if not failed_checks:
        print("🎉 PROJECT IS READY FOR DEPLOYMENT!")
        print("\n✅ All critical checks passed")
        print("\nNext steps:")
        print("1. Set DEBUG=False in production")
        print("2. Configure production database")
        print("3. Set up environment variables")
        print("4. Run 'python manage.py collectstatic'")
        print("5. Run 'python manage.py migrate'")
    else:
        print("❌ PROJECT NOT READY FOR DEPLOYMENT")
        print("\nFailed checks:")
        for check in failed_checks:
            print(f"   - {check}")
        print("\nPlease fix these issues before deploying.")
    
    print(f"\nOverall Status: {len(checks) - len(failed_checks)}/{len(checks)} checks passed")

if __name__ == '__main__':
    check_deployment_readiness()
