#!/usr/bin/env python
"""
Check MongoDB Data vs Web Display
"""
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

def check_mongodb_data():
    """Check what's actually in MongoDB"""
    print("🔍 Checking MongoDB Data...")
    print("=" * 50)
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['plant_diseases']
        collection = db['diseases']
        
        # Get all diseases
        diseases = list(collection.find({}))
        total_count = len(diseases)
        
        print(f"📊 Total documents in MongoDB: {total_count}")
        print("\n📋 All diseases in MongoDB:")
        
        for i, disease in enumerate(diseases, 1):
            name = disease.get('name', 'Unknown')
            solutions_count = len(disease.get('solutions', []))
            added_manually = disease.get('added_manually', False)
            
            print(f"{i:2d}. {name.title()}")
            print(f"    Solutions: {solutions_count}")
            print(f"    Manual: {'Yes' if added_manually else 'No'}")
            print(f"    ID: {disease.get('_id', 'No ID')}")
        
        return diseases
        
    except Exception as e:
        print(f"❌ Error checking MongoDB: {e}")
        return []

def check_web_display():
    """Check what's displayed on the web page"""
    print("\n🌐 Checking Web Display...")
    print("=" * 50)
    
    try:
        url = "http://127.0.0.1:8000/database/"
        response = requests.get(url)
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for disease cards or disease names
            disease_elements = soup.find_all(class_="disease-card")
            if not disease_elements:
                # Try alternative selectors
                disease_elements = soup.find_all(text=lambda text: text and any(
                    keyword in text.lower() for keyword in ['mildew', 'blight', 'rust', 'aphid', 'spot', 'tomato']
                ))
            
            print(f"📋 Diseases found on webpage: {len(disease_elements)}")
            
            # Check for error messages
            error_text = soup.get_text()
            if "Database connection failed" in error_text:
                print("❌ Database connection failed message found")
            elif "No diseases found" in error_text:
                print("⚠️  'No diseases found' message displayed")
            else:
                print("✅ No error messages found")
            
            # Show some content from the page
            page_text = soup.get_text()[:500]
            print(f"\n📄 Page content preview:")
            print(page_text[:200] + "..." if len(page_text) > 200 else page_text)
            
            return len(disease_elements)
        else:
            print(f"❌ Web page failed to load: {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ Error checking web display: {e}")
        return 0

def check_django_view():
    """Check Django view directly"""
    print("\n🐍 Checking Django View Logic...")
    print("=" * 50)
    
    try:
        # Import Django components
        import os
        import sys
        import django
        
        # Add project to path
        sys.path.append('.')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_django.settings')
        django.setup()
        
        # Import the view
        from plants.views import db
        
        if db is None:
            print("❌ Django db connection is None")
            return False
        
        # Test direct database query from Django
        diseases = list(db.diseases.find({}))
        print(f"✅ Django can access {len(diseases)} diseases")
        
        # Show first few diseases
        for i, disease in enumerate(diseases[:5], 1):
            print(f"  {i}. {disease.get('name', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking Django view: {e}")
        return False

def compare_data():
    """Compare MongoDB data with web display"""
    print("\n🔄 Data Comparison Analysis...")
    print("=" * 60)
    
    # Check MongoDB
    mongodb_diseases = check_mongodb_data()
    mongodb_count = len(mongodb_diseases)
    
    # Check web display
    web_count = check_web_display()
    
    # Check Django view
    django_working = check_django_view()
    
    print("\n" + "=" * 60)
    print("📊 COMPARISON RESULTS:")
    print(f"MongoDB Documents: {mongodb_count}")
    print(f"Web Display Count: {web_count}")
    print(f"Django Connection: {'✅ Working' if django_working else '❌ Failed'}")
    
    if mongodb_count > web_count:
        print(f"\n⚠️  ISSUE FOUND: {mongodb_count - web_count} diseases missing from web display!")
        print("\n🔧 Possible causes:")
        print("1. Django view not fetching all documents")
        print("2. Template not rendering all diseases")
        print("3. JavaScript/CSS hiding some elements")
        print("4. Database query filtering results")
        print("5. Pagination limiting display")
    elif mongodb_count == web_count:
        print("\n✅ Data counts match - no missing diseases")
    else:
        print(f"\n🤔 Unexpected: Web shows more than MongoDB ({web_count} > {mongodb_count})")

def main():
    """Main function"""
    print("🧪 MongoDB vs Web Display Diagnostic Tool")
    print("=" * 60)
    
    compare_data()
    
    print("\n🔧 TROUBLESHOOTING STEPS:")
    print("1. Check server logs for errors")
    print("2. Verify Django database connection")
    print("3. Test database view directly")
    print("4. Check template rendering")
    print("5. Inspect browser developer tools")

if __name__ == "__main__":
    main()
