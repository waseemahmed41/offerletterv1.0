#!/usr/bin/env python
"""
Check SQLite tables
"""
import sqlite3
import os

def check_sqlite_tables():
    """Check what tables exist in SQLite"""
    print("=== Checking SQLite Tables ===")
    
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        print("SQLite database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Found {len(tables)} tables:")
        for table in tables:
            table_name = table[0]
            print(f"  - {table_name}")
            
            # Count records in each table
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"    Records: {count}")
            except:
                print(f"    Records: Unable to count")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_sqlite_tables()
