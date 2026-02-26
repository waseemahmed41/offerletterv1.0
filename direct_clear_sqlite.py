#!/usr/bin/env python
"""
Direct SQLite database clear
"""
import sqlite3
import os

def clear_sqlite_direct():
    """Clear candidates directly from SQLite"""
    print("=== Clearing SQLite Database Directly ===")
    
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        print("SQLite database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check candidates before deletion
        cursor.execute("SELECT COUNT(*) FROM offers_candidate")
        candidate_count = cursor.fetchone()[0]
        print(f"Found {candidate_count} candidates in SQLite")
        
        cursor.execute("SELECT COUNT(*) FROM offers_offerletter")
        offer_letter_count = cursor.fetchone()[0]
        print(f"Found {offer_letter_count} offer letters in SQLite")
        
        if candidate_count > 0:
            # Show candidates
            cursor.execute("SELECT work_id, name, email FROM offers_candidate ORDER BY work_id")
            candidates = cursor.fetchall()
            print("\nCandidates in SQLite:")
            for work_id, name, email in candidates:
                print(f"  {work_id}: {name} ({email})")
        
        if candidate_count > 0 or offer_letter_count > 0:
            # Delete offer letters first
            cursor.execute("DELETE FROM offers_offerletter")
            deleted_offer_letters = cursor.rowcount
            print(f"\nDeleted {deleted_offer_letters} offer letters from SQLite")
            
            # Delete candidates
            cursor.execute("DELETE FROM offers_candidate")
            deleted_candidates = cursor.rowcount
            print(f"Deleted {deleted_candidates} candidates from SQLite")
            
            conn.commit()
            print("\n✅ SQLite database cleared!")
        else:
            print("No data to clear in SQLite.")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error clearing SQLite: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    clear_sqlite_direct()
