"""
Simple MongoDB Setup and Connection
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from config.settings import MONGODB_URI, DATABASE_NAME, COLLECTION_NAME

class SimpleDatabase:
    def __init__(self):
        """Initialize database connection"""
        self.client = None
        self.db = None
        self.collection = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            print("🔄 Connecting to MongoDB...")
            self.client = MongoClient(MONGODB_URI)
            self.client.admin.command('ping')
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            print("✅ Connected to MongoDB successfully!")
            return True
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            return False
    
    def is_connected(self):
        """Check if database is connected"""
        try:
            if self.client:
                self.client.admin.command('ping')
                return True
        except:
            pass
        return False
    
    def get_all_diseases(self):
        """Get all diseases from database"""
        try:
            if not self.is_connected():
                self.connect()
            
            diseases = list(self.collection.find({}))
            return diseases
        except Exception as e:
            print(f"Error getting diseases: {e}")
            return []
    
    def search_diseases(self, query):
        """Search diseases by name"""
        try:
            if not self.is_connected():
                self.connect()
            
            # Case-insensitive search
            diseases = list(self.collection.find({
                "name": {"$regex": query, "$options": "i"}
            }))
            return diseases
        except Exception as e:
            print(f"Error searching diseases: {e}")
            return []
    
    def add_disease(self, disease_data):
        """Add a new disease to database"""
        try:
            if not self.is_connected():
                self.connect()
            
            result = self.collection.insert_one(disease_data)
            return result.inserted_id
        except Exception as e:
            print(f"Error adding disease: {e}")
            return None
    
    def get_disease_count(self):
        """Get total number of diseases"""
        try:
            if not self.is_connected():
                self.connect()
            
            return self.collection.count_documents({})
        except Exception as e:
            print(f"Error counting diseases: {e}")
            return 0

# Global database instance
db = SimpleDatabase()
