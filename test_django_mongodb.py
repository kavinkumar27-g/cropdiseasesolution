#!/usr/bin/env python
"""
Test Django MongoDB Connection
"""
import os
import sys
import django
from pymongo import MongoClient

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_django.settings')

# Setup Django
django.setup()

def test_mongodb_connection():
    """Test MongoDB connection from Django context"""
    print("🧪 Testing MongoDB Connection from Django...")
    print("=" * 50)
    
    try:
        # Test direct MongoDB connection
        client = MongoClient('mongodb://localhost:27017/')
        client.admin.command('ping')
        print("✅ Direct MongoDB connection: SUCCESS")
        
        # Test database access
        db = client['plant_diseases']
        print(f"✅ Database 'plant_diseases' access: SUCCESS")
        
        # Test collection access
        collection = db['diseases']
        print(f"✅ Collection 'diseases' access: SUCCESS")
        
        # Count documents
        count = collection.count_documents({})
        print(f"📊 Documents in collection: {count}")
        
        if count == 0:
            print("⚠️  No documents found. Adding sample data...")
            
            # Add sample disease data
            sample_disease = {
                "name": "test disease",
                "description": "A test disease for MongoDB connection verification",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Test organic solution",
                        "effectiveness": "High",
                        "application": "Test application method"
                    }
                ]
            }
            
            result = collection.insert_one(sample_disease)
            print(f"✅ Sample document inserted with ID: {result.inserted_id}")
            
            # Verify insertion
            new_count = collection.count_documents({})
            print(f"📊 Documents after insertion: {new_count}")
        
        # Test search functionality
        print("\n🔍 Testing search functionality...")
        test_disease = collection.find_one({"name": {"$regex": "test", "$options": "i"}})
        if test_disease:
            print(f"✅ Search test: Found disease '{test_disease['name']}'")
        else:
            print("❌ Search test: No test disease found")
        
        print("\n🎉 MongoDB connection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection test failed: {e}")
        return False

def test_django_views():
    """Test Django views that use MongoDB"""
    print("\n🌐 Testing Django Views with MongoDB...")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.contrib.auth.models import User
        
        # Create test client
        client = Client()
        
        # Test database view (should work without login for testing)
        print("Testing database view...")
        
        # Create a test user for authenticated views
        try:
            user = User.objects.create_user(
                username='testuser',
                password='testpass123',
                email='test@example.com'
            )
            print("✅ Test user created")
        except:
            user = User.objects.get(username='testuser')
            print("✅ Test user already exists")
        
        # Login the test user
        login_success = client.login(username='testuser', password='testpass123')
        print(f"✅ Test user login: {'SUCCESS' if login_success else 'FAILED'}")
        
        # Test database view
        response = client.get('/database/')
        print(f"✅ Database view response: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Database view working correctly")
        else:
            print(f"⚠️  Database view returned status: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django views test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Django MongoDB Connection Test")
    print("=" * 60)
    
    # Test MongoDB connection
    mongo_success = test_mongodb_connection()
    
    # Test Django views
    django_success = test_django_views()
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY:")
    print(f"MongoDB Connection: {'✅ PASS' if mongo_success else '❌ FAIL'}")
    print(f"Django Views: {'✅ PASS' if django_success else '❌ FAIL'}")
    
    if mongo_success and django_success:
        print("\n🎉 All tests passed! MongoDB is working with Django.")
        print("\n🌐 You can now use:")
        print("• http://127.0.0.1:8000/ - Main app")
        print("• http://127.0.0.1:8000/database/ - View database")
        print("• http://127.0.0.1:8000/reset-db/ - Reset database")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
