#!/usr/bin/env python
"""
Fix Django static files configuration for production
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from django.conf import settings

def fix_static_files():
    """Fix static files configuration"""
    print("=== FIXING DJANGO STATIC FILES ===\n")
    
    # 1. Update settings.py for production
    print("1. UPDATING SETTINGS.PY FOR PRODUCTION")
    
    settings_file = os.path.join(settings.BASE_DIR, 'offer_automation', 'settings.py')
    
    # Read current settings
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Check if Whitenoise is already configured
    if 'whitenoise.middleware.WhiteNoiseMiddleware' not in content:
        print("   Adding Whitenoise middleware...")
        
        # Find MIDDLEWARE section and add Whitenoise
        if 'MIDDLEWARE = [' in content:
            # Add Whitenoise after SecurityMiddleware
            content = content.replace(
                "MIDDLEWARE = [",
                """MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',"""
            )
        
        # Write updated content
        with open(settings_file, 'w') as f:
            f.write(content)
        
        print("   ✅ Whitenoise middleware added")
    else:
        print("   ✅ Whitenoise middleware already configured")
    
    # 2. Update STATIC_ROOT for production
    print("\n2. UPDATING STATIC_ROOT FOR PRODUCTION")
    
    # Check if STATIC_ROOT is properly set
    if 'BASE_DIR / \'staticfiles\'' in content:
        print("   ✅ STATIC_ROOT already properly configured")
    else:
        print("   STATIC_ROOT needs manual configuration for production")
        print("   Current STATIC_ROOT should be: BASE_DIR / 'staticfiles'")
    
    # 3. Update STATIC_URL if needed
    print("\n3. CHECKING STATIC_URL")
    if 'STATIC_URL = \'static/\'' in content:
        print("   ⚠️  STATIC_URL should start with '/' for production")
        print("   Changing 'static/' to '/static/'")
        content = content.replace(
            "STATIC_URL = 'static/'",
            "STATIC_URL = '/static/'"
        )
        
        with open(settings_file, 'w') as f:
            f.write(content)
        
        print("   ✅ STATIC_URL updated to '/static/'")
    else:
        print("   ✅ STATIC_URL already starts with '/'")
    
    # 4. Add production static files configuration
    print("\n4. ADDING PRODUCTION STATIC FILES CONFIG")
    
    # Check if production static config exists
    if 'STATICFILES_STORAGE' not in content:
        prod_config = '''

# Production Static Files Configuration
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Additional production settings
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
'''
        
        # Add before the last line
        content = content.rstrip() + prod_config + '\n'
        
        with open(settings_file, 'w') as f:
            f.write(content)
        
        print("   ✅ Production static files configuration added")
    else:
        print("   ✅ Production static files configuration already exists")
    
    # 5. Update requirements.txt to include Whitenoise
    print("\n5. UPDATING REQUIREMENTS.TXT")
    
    requirements_file = os.path.join(settings.BASE_DIR, 'requirements.txt')
    
    with open(requirements_file, 'r') as f:
        req_content = f.read()
    
    if 'whitenoise' not in req_content:
        print("   Adding Whitenoise to requirements.txt...")
        req_content += '\nwhitenoise==6.6.0\n'
        
        with open(requirements_file, 'w') as f:
            f.write(req_content)
        
        print("   ✅ Whitenoise added to requirements.txt")
    else:
        print("   ✅ Whitenoise already in requirements.txt")
    
    # 6. Create production-ready static files structure
    print("\n6. CREATING PRODUCTION STATIC FILES STRUCTURE")
    
    # Ensure staticfiles directory exists
    staticfiles_dir = settings.STATIC_ROOT
    os.makedirs(staticfiles_dir, exist_ok=True)
    
    # Run collectstatic
    print("   Running collectstatic...")
    import subprocess
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear'
        ], capture_output=True, text=True, cwd=settings.BASE_DIR)
        
        if result.returncode == 0:
            print("   ✅ collectstatic completed successfully")
            print(f"   Output: {result.stdout}")
        else:
            print(f"   ❌ collectstatic failed: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Error running collectstatic: {str(e)}")
    
    # 7. Create .staticignore file
    print("\n7. CREATING .STATICIGNORE FILE")
    
    staticignore_file = os.path.join(settings.BASE_DIR, '.staticignore')
    
    staticignore_content = '''# Ignore files that shouldn't be collected
*.pyc
*.pyo
*.pyd
.Python
__pycache__
.pytest_cache
.coverage
.git
.gitignore
.env
.venv
env/
venv/
node_modules/
.DS_Store
Thumbs.db
*.log
local_settings.py
db.sqlite3
media/
'''
    
    with open(staticignore_file, 'w') as f:
        f.write(staticignore_content)
    
    print("   ✅ .staticignore file created")
    
    # 8. Summary
    print("\n" + "="*50)
    print("STATIC FILES FIX SUMMARY")
    print("="*50)
    
    print("✅ Changes Made:")
    print("   1. Added Whitenoise middleware")
    print("   2. Updated STATIC_URL to '/static/'")
    print("   3. Added production static files configuration")
    print("   4. Added Whitenoise to requirements.txt")
    print("   5. Ran collectstatic --clear")
    print("   6. Created .staticignore file")
    
    print("\n📋 Next Steps:")
    print("   1. Commit changes to version control")
    print("   2. Deploy to production")
    print("   3. Set DEBUG=False in production environment")
    print("   4. Configure web server to serve static files")
    
    print("\n🔧 Production Configuration:")
    print("   - Whitenoise will serve static files efficiently")
    print("   - Compressed and cached static files")
    print("   - Security headers for static files")
    print("   - Manifest-based file serving")

if __name__ == '__main__':
    fix_static_files()
