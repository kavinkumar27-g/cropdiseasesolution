#!/usr/bin/env python
"""
Complete Database Connection Fix
"""
import requests
from pymongo import MongoClient
import subprocess
import time

def check_mongodb_status():
    """Check if MongoDB is running and accessible"""
    print("🔍 Checking MongoDB Status...")
    print("=" * 50)
    
    try:
        # Test MongoDB connection
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ MongoDB is running and accessible")
        
        # Check database and collection
        db = client['plant_diseases']
        count = db.diseases.count_documents({})
        print(f"📊 Found {count} diseases in database")
        
        # Show sample diseases
        diseases = list(db.diseases.find({}).limit(5))
        print("📋 Sample diseases:")
        for i, disease in enumerate(diseases, 1):
            name = disease.get('name', 'Unknown')
            print(f"  {i}. {name.title()}")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def check_django_server():
    """Check if Django server is running"""
    print("\n🌐 Checking Django Server...")
    print("=" * 50)
    
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print(f"✅ Django server is running (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Django server is not running")
        return False
    except Exception as e:
        print(f"❌ Error checking Django server: {e}")
        return False

def test_database_page():
    """Test the database page specifically"""
    print("\n📊 Testing Database Page...")
    print("=" * 50)
    
    try:
        response = requests.get("http://127.0.0.1:8000/database/", timeout=10)
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Database page loaded successfully")
            
            # Check for error messages in content
            content = response.text.lower()
            if "database connection failed" in content:
                print("❌ Database connection failed message found in page")
                return False
            elif "no diseases found" in content:
                print("⚠️  'No diseases found' message in page")
                return False
            else:
                print("✅ No error messages found in page")
                return True
                
        elif response.status_code == 302:
            print("🔄 Redirected (likely to login page)")
            print("💡 Database page requires authentication")
            return False
        else:
            print(f"❌ Database page returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing database page: {e}")
        return False

def restart_services():
    """Restart MongoDB and Django services"""
    print("\n🔄 Restarting Services...")
    print("=" * 50)
    
    print("🛑 Note: MongoDB is already running in background")
    print("💡 Django server should be restarted manually if needed")
    
    # Check if services are working
    mongodb_ok = check_mongodb_status()
    django_ok = check_django_server()
    
    return mongodb_ok and django_ok

def create_quick_test():
    """Create a quick test to verify everything works"""
    print("\n🧪 Creating Quick Test...")
    print("=" * 50)
    
    try:
        # Test MongoDB directly
        client = MongoClient('mongodb://localhost:27017/')
        db = client['plant_diseases']
        
        # Insert a test disease
        test_disease = {
            "name": "connection_test",
            "description": "Test disease to verify connection",
            "solutions": [{
                "type": "organic",
                "solution": "Test solution",
                "effectiveness": "High",
                "application": "Test application"
            }],
            "test_disease": True
        }
        
        # Insert and immediately remove
        result = db.diseases.insert_one(test_disease)
        print(f"✅ Test insert successful: {result.inserted_id}")
        
        # Remove test disease
        db.diseases.delete_one({"_id": result.inserted_id})
        print("✅ Test cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def provide_solutions():
    """Provide solutions for common issues"""
    print("\n🔧 Common Solutions:")
    print("=" * 50)
    
    print("1. 🔄 Restart MongoDB:")
    print("   mongod --dbpath \"C:\\data\\db\"")
    
    print("\n2. 🌐 Restart Django Server:")
    print("   python manage.py runserver")
    
    print("\n3. 🔍 Check Database View (No Login Required):")
    print("   http://127.0.0.1:8000/database/")
    
    print("\n4. 🧪 Test MongoDB Connection:")
    print("   python test_connection.py")
    
    print("\n5. 📊 Check Database Content:")
    print("   python check_mongodb_data.py")
    
    print("\n6. ➕ Add New Disease:")
    print("   python add_disease_manually.py")

def main():
    """Main diagnostic function"""
    print("🚀 Database Connection Diagnostic & Fix Tool")
    print("=" * 60)
    
    # Check MongoDB
    mongodb_ok = check_mongodb_status()
    
    # Check Django
    django_ok = check_django_server()
    
    # Test database page
    db_page_ok = test_database_page()
    
    # Quick test
    quick_test_ok = create_quick_test()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC RESULTS:")
    print(f"MongoDB Status: {'✅ OK' if mongodb_ok else '❌ FAILED'}")
    print(f"Django Server: {'✅ OK' if django_ok else '❌ FAILED'}")
    print(f"Database Page: {'✅ OK' if db_page_ok else '❌ FAILED'}")
    print(f"Quick Test: {'✅ OK' if quick_test_ok else '❌ FAILED'}")
    
    if all([mongodb_ok, django_ok, db_page_ok, quick_test_ok]):
        print("\n🎉 ALL SYSTEMS WORKING!")
        print("✅ Your database connection is fully functional")
        print("\n🌐 Available URLs:")
        print("• Main App: http://127.0.0.1:8000/")
        print("• Database View: http://127.0.0.1:8000/database/")
        print("• Add Disease: http://127.0.0.1:8000/add-disease/")
    else:
        print("\n⚠️  ISSUES DETECTED")
        provide_solutions()

if __name__ == "__main__":
    main()
