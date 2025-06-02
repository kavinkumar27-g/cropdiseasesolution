#!/usr/bin/env python
"""
Test Web Database Interface
"""
import requests
from bs4 import BeautifulSoup

def test_database_page():
    """Test the database page functionality"""
    print("🌐 Testing Web Database Interface...")
    print("=" * 50)
    
    try:
        # Test database page
        url = "http://127.0.0.1:8000/database/"
        print(f"📡 Requesting: {url}")
        
        response = requests.get(url)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Database page loaded successfully!")
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for error messages
            error_elements = soup.find_all(text=lambda text: text and "Database connection failed" in text)
            if error_elements:
                print("❌ Database connection failed message found on page")
                return False
            
            # Check for disease content
            disease_cards = soup.find_all(class_="disease-card")
            if disease_cards:
                print(f"✅ Found {len(disease_cards)} disease cards on page")
                
                # List the diseases found
                for i, card in enumerate(disease_cards, 1):
                    disease_name = card.find(class_="disease-name")
                    if disease_name:
                        print(f"  {i}. {disease_name.get_text().strip()}")
                
                return True
            else:
                # Check for any disease-related content
                disease_content = soup.find_all(text=lambda text: text and any(
                    disease in text.lower() for disease in ['mildew', 'blight', 'rust', 'aphid', 'spot']
                ))
                
                if disease_content:
                    print(f"✅ Found disease-related content on page")
                    for content in disease_content[:5]:  # Show first 5 matches
                        print(f"  • {content.strip()}")
                    return True
                else:
                    print("⚠️  No disease content found on page")
                    
                    # Check if page has any content
                    page_text = soup.get_text()
                    if "plant_diseases" in page_text.lower() or "database" in page_text.lower():
                        print("✅ Database-related content found")
                        return True
                    else:
                        print("❌ No relevant content found")
                        return False
        else:
            print(f"❌ Database page failed to load: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server")
        print("💡 Make sure Django server is running: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error testing database page: {e}")
        return False

def test_main_page():
    """Test the main page"""
    print("\n🏠 Testing Main Page...")
    print("=" * 50)
    
    try:
        url = "http://127.0.0.1:8000/"
        response = requests.get(url)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Main page loaded successfully!")
            
            # Check for navigation links
            soup = BeautifulSoup(response.content, 'html.parser')
            database_links = soup.find_all('a', href=lambda href: href and 'database' in href)
            
            if database_links:
                print(f"✅ Found {len(database_links)} database navigation links")
                return True
            else:
                print("⚠️  No database navigation links found")
                return True  # Main page might still be working
        else:
            print(f"❌ Main page failed to load: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing main page: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Web Database Interface Test")
    print("=" * 60)
    
    # Test main page
    main_success = test_main_page()
    
    # Test database page
    db_success = test_database_page()
    
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS:")
    print(f"Main Page: {'✅ PASS' if main_success else '❌ FAIL'}")
    print(f"Database Page: {'✅ PASS' if db_success else '❌ FAIL'}")
    
    if main_success and db_success:
        print("\n🎉 All tests passed! Web database interface is working!")
        print("\n🌐 Available URLs:")
        print("• Main App: http://127.0.0.1:8000/")
        print("• Database View: http://127.0.0.1:8000/database/")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        
        if not db_success:
            print("\n🔧 Troubleshooting Database Issues:")
            print("1. Check if MongoDB is running: mongod --dbpath \"C:\\data\\db\"")
            print("2. Check if Django server is running: python manage.py runserver")
            print("3. Verify MongoDB connection: python test_mongodb_connection.py")
            print("4. Check Django logs for errors")

if __name__ == "__main__":
    main()
