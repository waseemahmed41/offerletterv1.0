#!/usr/bin/env python
"""
Final verification that both databases are clean
"""
import os
import sys
import django
import sqlite3

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'offer_automation.settings')
django.setup()

from offers.models import Candidate, OfferLetter
from django.db import connection

def check_sqlite():
    """Check SQLite directly"""
    print("=== SQLite Database ===")
    
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        print("SQLite database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM candidates")
        sqlite_candidates = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM offers_offerletter")
        sqlite_offer_letters = cursor.fetchone()[0]
        
        print(f"Candidates: {sqlite_candidates}")
        print(f"Offer Letters: {sqlite_offer_letters}")
        
        conn.close()
        
        return sqlite_candidates, sqlite_offer_letters
        
    except Exception as e:
        print(f"❌ Error checking SQLite: {str(e)}")
        return None, None

def check_neon():
    """Check Neon PostgreSQL"""
    print("\n=== Neon PostgreSQL Database ===")
    
    try:
        neon_candidates = Candidate.objects.count()
        neon_offer_letters = OfferLetter.objects.count()
        
        print(f"Database: {connection.settings_dict['NAME']}")
        print(f"Candidates: {neon_candidates}")
        print(f"Offer Letters: {neon_offer_letters}")
        
        return neon_candidates, neon_offer_letters
        
    except Exception as e:
        print(f"❌ Error checking Neon: {str(e)}")
        return None, None

def main():
    print("=== Final Verification: Both Databases Clean ===\n")
    
    sqlite_cands, sqlite_letters = check_sqlite()
    neon_cands, neon_letters = check_neon()
    
    print("\n=== Summary ===")
    
    if sqlite_cands == 0 and sqlite_letters == 0:
        print("✅ SQLite: Clean (0 candidates, 0 offer letters)")
    else:
        print(f"❌ SQLite: NOT CLEAN ({sqlite_cands} candidates, {sqlite_letters} offer letters)")
    
    if neon_cands == 0 and neon_letters == 0:
        print("✅ Neon: Clean (0 candidates, 0 offer letters)")
    else:
        print(f"❌ Neon: NOT CLEAN ({neon_cands} candidates, {neon_letters} offer letters)")
    
    if (sqlite_cands == 0 and sqlite_letters == 0 and 
        neon_cands == 0 and neon_letters == 0):
        print("\n🎉 SUCCESS: Both databases are completely clean!")
        print("Work ID sequence will start from 0A20 for new candidates.")
    else:
        print("\n⚠️  WARNING: Some databases still contain data.")

if __name__ == '__main__':
    main()
