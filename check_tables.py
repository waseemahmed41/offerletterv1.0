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

def check_sqlite_tables():
    """Check what tables exist in SQLite database"""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tables in SQLite database:")
    for table in sorted(tables):
        print(f"  - {table}")

def check_neon_tables():
    """Check what tables exist in Neon database"""
    from django.db import connections
    cursor = connections['neon'].cursor()
    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
    tables = [row[0] for row in cursor.fetchall()]
    print("\nTables in Neon database:")
    for table in sorted(tables):
        print(f"  - {table}")

if __name__ == '__main__':
    check_sqlite_tables()
    check_neon_tables()
