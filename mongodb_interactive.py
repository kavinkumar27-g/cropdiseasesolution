#!/usr/bin/env python
"""
Interactive MongoDB Connection for AI Crop Diseases Solution
"""
from pymongo import MongoClient
import json
from datetime import datetime

class MongoDBManager:
    def __init__(self):
        """Initialize MongoDB connection"""
        try:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.client.admin.command('ping')
            self.db = self.client['plant_diseases']
            self.collection = self.db['diseases']
            print("✅ Connected to MongoDB successfully!")
            print(f"📊 Database: {self.db.name}")
            print(f"📁 Collection: {self.collection.name}")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            self.client = None
            self.db = None
            self.collection = None

    def show_connection_info(self):
        """Display connection information"""
        print("\n🔗 MongoDB Connection Information:")
        print("=" * 50)
        print(f"Host: localhost")
        print(f"Port: 27017")
        print(f"Database: plant_diseases")
        print(f"Collection: diseases")
        print(f"Connection String: mongodb://localhost:27017")

    def show_database_stats(self):
        """Show database statistics"""
        if self.collection is None:
            print("❌ No database connection")
            return
        
        print("\n📊 Database Statistics:")
        print("=" * 50)
        
        # Count documents
        total_docs = self.collection.count_documents({})
        print(f"Total diseases: {total_docs}")
        
        # Show collections
        collections = self.db.list_collection_names()
        print(f"Collections: {collections}")
        
        # Database size info
        stats = self.db.command("dbstats")
        print(f"Database size: {stats.get('dataSize', 0)} bytes")

    def list_all_diseases(self):
        """List all diseases in the database"""
        if self.collection is None:
            print("❌ No database connection")
            return
        
        print("\n🌿 All Diseases in Database:")
        print("=" * 50)
        
        diseases = list(self.collection.find({}))
        
        if not diseases:
            print("📝 No diseases found. Database is empty.")
            return
        
        for i, disease in enumerate(diseases, 1):
            print(f"\n{i}. {disease.get('name', 'Unknown').title()}")
            print(f"   Description: {disease.get('description', 'No description')}")
            
            solutions = disease.get('solutions', [])
            organic_count = len([s for s in solutions if s.get('type') == 'organic'])
            inorganic_count = len([s for s in solutions if s.get('type') == 'inorganic'])
            
            print(f"   Solutions: {organic_count} organic, {inorganic_count} inorganic")

    def search_disease(self, disease_name):
        """Search for a specific disease"""
        if self.collection is None:
            print("❌ No database connection")
            return
        
        print(f"\n🔍 Searching for: '{disease_name}'")
        print("=" * 50)
        
        # Case-insensitive search
        disease = self.collection.find_one(
            {"name": {"$regex": f".*{disease_name}.*", "$options": "i"}}
        )
        
        if not disease:
            print(f"❌ Disease '{disease_name}' not found")
            return
        
        print(f"✅ Found: {disease['name'].title()}")
        print(f"📝 Description: {disease.get('description', 'No description')}")
        
        solutions = disease.get('solutions', [])
        if solutions:
            print(f"\n💊 Solutions ({len(solutions)} total):")
            
            # Organic solutions
            organic_solutions = [s for s in solutions if s.get('type') == 'organic']
            if organic_solutions:
                print(f"\n🌱 Organic Solutions ({len(organic_solutions)}):")
                for i, sol in enumerate(organic_solutions, 1):
                    print(f"  {i}. {sol.get('solution', 'Unknown solution')}")
                    print(f"     Effectiveness: {sol.get('effectiveness', 'Unknown')}")
                    print(f"     Application: {sol.get('application', 'No instructions')}")
            
            # Inorganic solutions
            inorganic_solutions = [s for s in solutions if s.get('type') == 'inorganic']
            if inorganic_solutions:
                print(f"\n🧪 Inorganic Solutions ({len(inorganic_solutions)}):")
                for i, sol in enumerate(inorganic_solutions, 1):
                    print(f"  {i}. {sol.get('solution', 'Unknown solution')}")
                    print(f"     Effectiveness: {sol.get('effectiveness', 'Unknown')}")
                    print(f"     Application: {sol.get('application', 'No instructions')}")

    def add_sample_data(self):
        """Add comprehensive sample disease data"""
        if self.collection is None:
            print("❌ No database connection")
            return
        
        print("\n📝 Adding comprehensive sample data...")
        print("=" * 50)
        
        # Clear existing data
        self.collection.drop()
        
        sample_diseases = [
            {
                "name": "powdery mildew",
                "description": "A fungal disease that appears as white powdery coating on leaves and stems",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Baking soda spray (1 tbsp per gallon water)",
                        "effectiveness": "High",
                        "application": "Spray weekly on affected areas"
                    },
                    {
                        "type": "organic",
                        "solution": "Neem oil treatment",
                        "effectiveness": "High",
                        "application": "Apply every 7-14 days"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Sulfur-based fungicide",
                        "effectiveness": "Very High",
                        "application": "Apply as directed on label"
                    }
                ]
            },
            {
                "name": "blight",
                "description": "A plant disease causing brown spots and wilting of leaves and stems",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Copper sulfate spray",
                        "effectiveness": "High",
                        "application": "Apply every 7-10 days in dry weather"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Chlorothalonil fungicide",
                        "effectiveness": "Very High",
                        "application": "Apply every 7-14 days"
                    }
                ]
            },
            {
                "name": "rust",
                "description": "A fungal disease causing orange-red pustules on leaf undersides",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Sulfur dust application",
                        "effectiveness": "High",
                        "application": "Apply early morning when dew is present"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Propiconazole systemic fungicide",
                        "effectiveness": "Very High",
                        "application": "Apply at first sign of disease"
                    }
                ]
            },
            {
                "name": "aphid infestation",
                "description": "Small green or black insects clustering on stems and leaves",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Insecticidal soap spray",
                        "effectiveness": "High",
                        "application": "Spray every 2-3 days until controlled"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Imidacloprid systemic insecticide",
                        "effectiveness": "Very High",
                        "application": "Apply to soil around plant base"
                    }
                ]
            },
            {
                "name": "black spot",
                "description": "Fungal disease causing black spots on leaves, common in roses",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Baking soda and oil spray",
                        "effectiveness": "Medium",
                        "application": "Spray weekly during growing season"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Tebuconazole fungicide",
                        "effectiveness": "Very High",
                        "application": "Apply every 14 days"
                    }
                ]
            }
        ]
        
        # Insert sample data
        result = self.collection.insert_many(sample_diseases)
        print(f"✅ Added {len(result.inserted_ids)} diseases to database")
        
        # Show what was added
        for disease in sample_diseases:
            print(f"  • {disease['name'].title()}")

    def interactive_menu(self):
        """Interactive menu for MongoDB operations"""
        while True:
            print("\n🌾 AI Crop Diseases Solution - MongoDB Manager")
            print("=" * 60)
            print("1. 📊 Show connection info")
            print("2. 📈 Show database statistics")
            print("3. 📋 List all diseases")
            print("4. 🔍 Search for a disease")
            print("5. 📝 Add sample data")
            print("6. 🌐 Open web interface")
            print("7. 🧭 MongoDB Compass info")
            print("0. ❌ Exit")
            
            choice = input("\nEnter your choice (0-7): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                self.show_connection_info()
            elif choice == "2":
                self.show_database_stats()
            elif choice == "3":
                self.list_all_diseases()
            elif choice == "4":
                disease_name = input("Enter disease name to search: ").strip()
                if disease_name:
                    self.search_disease(disease_name)
            elif choice == "5":
                self.add_sample_data()
            elif choice == "6":
                print("\n🌐 Web Interface URLs:")
                print("• Main App: http://127.0.0.1:8000/")
                print("• Database View: http://127.0.0.1:8000/database/")
                print("• Reset Database: http://127.0.0.1:8000/reset-db/")
            elif choice == "7":
                print("\n🧭 MongoDB Compass Connection:")
                print("1. Download: https://www.mongodb.com/products/compass")
                print("2. Install and launch MongoDB Compass")
                print("3. Connect using: mongodb://localhost:27017")
                print("4. Browse 'plant_diseases' database")
            else:
                print("❌ Invalid choice. Please try again.")

def main():
    """Main function"""
    print("🚀 Starting MongoDB Interactive Manager...")
    
    # Create MongoDB manager
    mongo_manager = MongoDBManager()
    
    if mongo_manager.client:
        # Start interactive menu
        mongo_manager.interactive_menu()
    else:
        print("❌ Cannot start without MongoDB connection")
        print("💡 Make sure MongoDB is running: mongod --dbpath \"C:\\data\\db\"")

if __name__ == "__main__":
    main()
