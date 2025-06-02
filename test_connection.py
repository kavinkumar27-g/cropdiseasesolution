#!/usr/bin/env python
"""
Quick MongoDB Connection Test
"""
from pymongo import MongoClient

try:
    print("🔄 Testing MongoDB connection...")
    client = MongoClient('mongodb://localhost:27017/')
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    db = client['plant_diseases']
    count = db.diseases.count_documents({})
    print(f"📊 Found {count} diseases in database")
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
