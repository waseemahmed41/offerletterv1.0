#!/usr/bin/env python
import pandas as pd

def debug_phone_validation():
    """Debug phone number validation"""
    # Read the CSV file
    df = pd.read_csv('test_bulk_upload.csv')
    
    print("CSV Content:")
    print(df.to_string())
    
    print("\nPhone number analysis:")
    for index, row in df.iterrows():
        phone = str(row['phone']).strip()
        phone_digits = ''.join(filter(str.isdigit, phone))
        
        print(f"Row {index + 1}:")
        print(f"  Original phone: '{phone}'")
        print(f"  Phone digits: '{phone_digits}'")
        print(f"  Length: {len(phone_digits)}")
        print(f"  Valid: {len(phone_digits) >= 10}")
        print()

if __name__ == '__main__':
    debug_phone_validation()
