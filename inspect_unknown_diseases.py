#!/usr/bin/env python
"""
Inspect Unknown Diseases in MongoDB
"""
from pymongo import MongoClient
import json
from datetime import datetime

def inspect_unknown_diseases():
    """Inspect diseases with 'Unknown' names"""
    print("🔍 Inspecting Unknown Diseases...")
    print("=" * 50)
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['plant_diseases']
        collection = db['diseases']
        
        # Find diseases with missing or unknown names
        unknown_diseases = list(collection.find({
            "$or": [
                {"name": {"$exists": False}},
                {"name": ""},
                {"name": None},
                {"name": "unknown"}
            ]
        }))
        
        print(f"📊 Found {len(unknown_diseases)} diseases with missing/unknown names")
        
        for i, disease in enumerate(unknown_diseases, 1):
            print(f"\n🔍 Unknown Disease #{i}:")
            print(f"ID: {disease.get('_id')}")
            print(f"Name: {repr(disease.get('name', 'MISSING'))}")
            print(f"Description: {repr(disease.get('description', 'MISSING'))}")
            print(f"Solutions: {len(disease.get('solutions', []))}")
            
            # Show full document structure
            print("📄 Full document:")
            for key, value in disease.items():
                if key != '_id':
                    print(f"  {key}: {repr(value)}")
        
        return unknown_diseases
        
    except Exception as e:
        print(f"❌ Error inspecting diseases: {e}")
        return []

def clean_unknown_diseases():
    """Clean up unknown/empty diseases"""
    print("\n🧹 Cleaning Unknown Diseases...")
    print("=" * 50)
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['plant_diseases']
        collection = db['diseases']
        
        # Find and delete diseases with no useful data
        criteria = {
            "$or": [
                {"name": {"$exists": False}},
                {"name": ""},
                {"name": None},
                {"name": "unknown"},
                {"$and": [
                    {"name": {"$exists": True}},
                    {"solutions": {"$size": 0}}
                ]}
            ]
        }
        
        # Count before deletion
        count_before = collection.count_documents(criteria)
        print(f"📊 Found {count_before} diseases to clean up")
        
        if count_before > 0:
            confirm = input(f"Delete {count_before} incomplete diseases? (y/n): ").strip().lower()
            if confirm == 'y':
                result = collection.delete_many(criteria)
                print(f"✅ Deleted {result.deleted_count} incomplete diseases")
                
                # Show remaining count
                remaining = collection.count_documents({})
                print(f"📊 Remaining diseases: {remaining}")
                return True
            else:
                print("❌ Cleanup cancelled")
                return False
        else:
            print("✅ No diseases need cleanup")
            return True
            
    except Exception as e:
        print(f"❌ Error cleaning diseases: {e}")
        return False

def show_valid_diseases():
    """Show all valid diseases"""
    print("\n📋 Valid Diseases in Database:")
    print("=" * 50)
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['plant_diseases']
        collection = db['diseases']
        
        # Find diseases with valid names and solutions
        valid_diseases = list(collection.find({
            "name": {"$exists": True, "$ne": "", "$ne": None},
            "solutions": {"$exists": True, "$not": {"$size": 0}}
        }))
        
        print(f"📊 Found {len(valid_diseases)} valid diseases:")
        
        for i, disease in enumerate(valid_diseases, 1):
            name = disease.get('name', 'Unknown').title()
            solutions = disease.get('solutions', [])
            organic_count = len([s for s in solutions if s.get('type') == 'organic'])
            inorganic_count = len([s for s in solutions if s.get('type') == 'inorganic'])
            
            print(f"{i:2d}. {name}")
            print(f"    📝 {disease.get('description', 'No description')[:60]}...")
            print(f"    💊 {len(solutions)} solutions ({organic_count} organic, {inorganic_count} inorganic)")
            
            if disease.get('added_manually'):
                print(f"    ✏️  Added manually")
        
        return valid_diseases
        
    except Exception as e:
        print(f"❌ Error showing valid diseases: {e}")
        return []

def fix_database():
    """Fix database issues"""
    print("\n🔧 Database Repair Tool")
    print("=" * 50)
    
    # Inspect unknown diseases
    unknown_diseases = inspect_unknown_diseases()
    
    if unknown_diseases:
        # Clean up unknown diseases
        cleaned = clean_unknown_diseases()
        
        if cleaned:
            print("\n✅ Database cleaned successfully!")
        else:
            print("\n⚠️  Database cleanup skipped")
    
    # Show valid diseases
    valid_diseases = show_valid_diseases()
    
    print(f"\n📊 Final Database Status:")
    print(f"Valid diseases: {len(valid_diseases)}")
    print(f"Ready for web display: ✅")

def main():
    """Main function"""
    print("🔧 MongoDB Database Inspector & Cleaner")
    print("=" * 60)
    
    fix_database()
    
    print("\n🌐 Test your web interface:")
    print("• Database View: http://127.0.0.1:8000/database/")
    print("• Search: http://127.0.0.1:8000/")

if __name__ == "__main__":
    main()
