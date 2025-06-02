#!/usr/bin/env python
"""
Simple Plant Disease Solution - Startup Script
"""
import os
import sys
import subprocess
import time

def check_mongodb():
    """Check if MongoDB is running"""
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("✅ MongoDB is running")
        return True
    except Exception:
        print("❌ MongoDB is not running")
        return False

def start_mongodb():
    """Start MongoDB if not running"""
    if check_mongodb():
        return True
    
    print("🔄 Starting MongoDB...")
    try:
        # Try to start MongoDB
        subprocess.Popen(['mongod', '--dbpath', 'C:\\data\\db'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait a moment for MongoDB to start
        time.sleep(3)
        
        if check_mongodb():
            print("✅ MongoDB started successfully")
            return True
        else:
            print("❌ Failed to start MongoDB")
            return False
    except Exception as e:
        print(f"❌ Error starting MongoDB: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Checking dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed")
        return True
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_app():
    """Run the Flask application"""
    print("🌱 Starting Simple Plant Disease Solution...")
    
    # Change to the web directory
    os.chdir('web')
    
    # Run the Flask app
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main startup function"""
    print("🚀 Simple Plant Disease Solution - Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("❌ Please run this script from the simple_plant_app directory")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Start MongoDB
    if not start_mongodb():
        print("💡 Please start MongoDB manually:")
        print("   mongod --dbpath \"C:\\data\\db\"")
        return
    
    # Run the application
    run_app()

if __name__ == "__main__":
    main()
