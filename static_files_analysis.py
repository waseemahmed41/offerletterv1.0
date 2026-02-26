#!/usr/bin/env python
"""
Analyze and fix Django static files configuration issues
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
from django.contrib.staticfiles.finders import get_finders

def analyze_static_files():
    """Analyze static files configuration"""
    print("=== DJANGO STATIC FILES ANALYSIS ===\n")
    
    # 1. Configuration Check
    print("1. STATIC FILES CONFIGURATION")
    print(f"   STATIC_URL: {settings.STATIC_URL}")
    print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"   STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    # 2. Directory Structure Check
    print("\n2. DIRECTORY STRUCTURE")
    base_dir = settings.BASE_DIR
    
    static_dir = os.path.join(base_dir, 'static')
    staticfiles_dir = settings.STATIC_ROOT
    media_dir = settings.MEDIA_ROOT
    
    print(f"   Base Directory: {base_dir}")
    print(f"   Static Directory: {static_dir}")
    print(f"   Staticfiles Directory: {staticfiles_dir}")
    print(f"   Media Directory: {media_dir}")
    
    # Check if directories exist
    for name, path in [
        ("static", static_dir),
        ("staticfiles", staticfiles_dir),
        ("media", media_dir)
    ]:
        exists = os.path.exists(path)
        print(f"   {name.capitalize()}: {'✅ EXISTS' if exists else '❌ MISSING'}")
    
    # 3. Static Files Content
    print("\n3. STATIC FILES CONTENT")
    
    # Check what's in static directories
    if os.path.exists(static_dir):
        print(f"   Contents of {static_dir}:")
        for root, dirs, files in os.walk(static_dir):
            level = root.replace(static_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
    
    # Check what's in staticfiles
    if os.path.exists(staticfiles_dir):
        staticfiles_str = str(staticfiles_dir)
        print(f"\n   Contents of {staticfiles_str}:")
        for root, dirs, files in os.walk(staticfiles_dir):
            level = root.replace(staticfiles_str, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:10]:  # Limit to first 10 files
                print(f"{subindent}{file}")
            if len(files) > 10:
                print(f"{subindent}... and {len(files) - 10} more files")
    
    # 4. Static Files Finders
    print("\n4. STATIC FILES FINDERS")
    all_finders = get_finders()
    for finder in all_finders:
        print(f"   Finder: {finder.__class__.__name__}")
        if hasattr(finder, 'locations'):
            for location, prefix in finder.locations:
                print(f"     Location: {location} (prefix: {prefix})")
    
    # 5. Template Static References
    print("\n5. TEMPLATE STATIC REFERENCES")
    templates_dir = os.path.join(base_dir, 'templates')
    if os.path.exists(templates_dir):
        static_refs = []
        for root, dirs, files in os.walk(templates_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if '{% static' in content:
                                static_refs.append(file_path)
                    except:
                        pass
        
        print(f"   Templates using {{% static %}}: {len(static_refs)}")
        for ref in static_refs[:5]:  # Show first 5
            rel_path = os.path.relpath(ref, templates_dir)
            print(f"     {rel_path}")
        if len(static_refs) > 5:
            print(f"     ... and {len(static_refs) - 5} more")
    
    # 6. Issues and Recommendations
    print("\n6. ISSUES AND RECOMMENDATIONS")
    
    issues = []
    
    # Check if STATIC_URL starts with /
    if not settings.STATIC_URL.startswith('/'):
        issues.append("STATIC_URL should start with '/'")
    
    # Check if STATIC_ROOT is outside project directory
    if staticfiles_dir and str(staticfiles_dir).startswith(str(base_dir)):
        issues.append("STATIC_ROOT should be outside project directory for production")
    
    # Check if staticfiles exists
    if not os.path.exists(staticfiles_dir):
        issues.append("Run 'python manage.py collectstatic' to create staticfiles")
    
    # Check for missing static files
    required_files = [
        'js/alpine.min.js',
        'css/font-awesome.min.css'
    ]
    
    for file in required_files:
        file_path = os.path.join(staticfiles_dir, file)
        if not os.path.exists(file_path):
            issues.append(f"Missing static file: {file}")
    
    if issues:
        print("   ❌ ISSUES FOUND:")
        for issue in issues:
            print(f"     - {issue}")
    else:
        print("   ✅ No critical issues found")
    
    # 7. Production Recommendations
    print("\n7. PRODUCTION RECOMMENDATIONS")
    print("   1. Set STATIC_ROOT to /var/www/static/ or similar")
    print("   2. Configure web server to serve static files")
    print("   3. Use Whitenoise for static file serving")
    print("   4. Set STATIC_URL = '/static/'")
    print("   5. Run collectstatic during deployment")
    print("   6. Use CDN for static files in production")

if __name__ == '__main__':
    analyze_static_files()
