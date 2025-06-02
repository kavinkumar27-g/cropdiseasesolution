#!/usr/bin/env python
"""
Manual Disease Addition Tool for AI Crop Diseases Solution
"""
from pymongo import MongoClient
import json
from datetime import datetime

class DiseaseManager:
    def __init__(self):
        """Initialize MongoDB connection"""
        try:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.client.admin.command('ping')
            self.db = self.client['plant_diseases']
            self.collection = self.db['diseases']
            print("✅ Connected to MongoDB successfully!")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            self.client = None
            self.db = None
            self.collection = None

    def add_disease_interactive(self):
        """Interactive disease addition"""
        if self.collection is None:
            print("❌ No database connection")
            return False

        print("\n🌱 Add New Disease to Database")
        print("=" * 50)

        # Get disease name
        disease_name = input("Enter disease name: ").strip()
        if not disease_name:
            print("❌ Disease name is required")
            return False

        # Check if disease already exists
        existing = self.collection.find_one({"name": {"$regex": f"^{disease_name}$", "$options": "i"}})
        if existing:
            print(f"⚠️  Disease '{disease_name}' already exists!")
            overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != 'y':
                return False

        # Get disease description
        description = input("Enter disease description: ").strip()
        if not description:
            description = f"A plant disease affecting crops: {disease_name}"

        # Add solutions
        solutions = []
        print(f"\n💊 Adding solutions for '{disease_name}'")
        print("Enter solutions (press Enter with empty solution to finish)")

        while True:
            print(f"\n--- Solution #{len(solutions) + 1} ---")
            
            # Solution type
            while True:
                sol_type = input("Solution type (organic/inorganic): ").strip().lower()
                if sol_type in ['organic', 'inorganic']:
                    break
                print("❌ Please enter 'organic' or 'inorganic'")

            # Solution description
            solution_text = input("Solution description: ").strip()
            if not solution_text:
                break

            # Effectiveness
            while True:
                effectiveness = input("Effectiveness (Low/Medium/High/Very High): ").strip().title()
                if effectiveness in ['Low', 'Medium', 'High', 'Very High']:
                    break
                print("❌ Please enter: Low, Medium, High, or Very High")

            # Application method
            application = input("Application method: ").strip()
            if not application:
                application = "Apply as directed"

            # Add solution
            solution = {
                "type": sol_type,
                "solution": solution_text,
                "effectiveness": effectiveness,
                "application": application
            }
            solutions.append(solution)

            # Ask for more solutions
            more = input("\nAdd another solution? (y/n): ").strip().lower()
            if more != 'y':
                break

        if not solutions:
            print("⚠️  No solutions added. Adding default solution...")
            solutions.append({
                "type": "organic",
                "solution": "Consult agricultural expert for treatment options",
                "effectiveness": "Medium",
                "application": "Follow expert recommendations"
            })

        # Create disease document
        disease_doc = {
            "name": disease_name.lower(),
            "description": description,
            "solutions": solutions,
            "added_date": datetime.now(),
            "added_manually": True
        }

        # Insert or update disease
        try:
            if existing:
                result = self.collection.replace_one(
                    {"name": {"$regex": f"^{disease_name}$", "$options": "i"}},
                    disease_doc
                )
                print(f"✅ Updated disease '{disease_name}' successfully!")
            else:
                result = self.collection.insert_one(disease_doc)
                print(f"✅ Added disease '{disease_name}' successfully!")
                print(f"📄 Document ID: {result.inserted_id}")

            # Show summary
            print(f"\n📋 Disease Summary:")
            print(f"Name: {disease_name}")
            print(f"Description: {description}")
            print(f"Solutions: {len(solutions)} total")
            
            organic_count = len([s for s in solutions if s['type'] == 'organic'])
            inorganic_count = len([s for s in solutions if s['type'] == 'inorganic'])
            print(f"  • {organic_count} organic solutions")
            print(f"  • {inorganic_count} inorganic solutions")

            return True

        except Exception as e:
            print(f"❌ Error adding disease: {e}")
            return False

    def add_disease_from_dict(self, disease_data):
        """Add disease from dictionary data"""
        if self.collection is None:
            print("❌ No database connection")
            return False

        try:
            # Add metadata
            disease_data['added_date'] = datetime.now()
            disease_data['added_manually'] = True

            result = self.collection.insert_one(disease_data)
            print(f"✅ Added disease '{disease_data['name']}' successfully!")
            print(f"📄 Document ID: {result.inserted_id}")
            return True

        except Exception as e:
            print(f"❌ Error adding disease: {e}")
            return False

    def list_all_diseases(self):
        """List all diseases in database"""
        if self.collection is None:
            print("❌ No database connection")
            return

        print("\n📋 All Diseases in Database:")
        print("=" * 50)

        diseases = list(self.collection.find({}))
        if not diseases:
            print("📝 No diseases found in database")
            return

        for i, disease in enumerate(diseases, 1):
            print(f"\n{i}. {disease['name'].title()}")
            print(f"   Description: {disease.get('description', 'No description')}")
            
            solutions = disease.get('solutions', [])
            organic_count = len([s for s in solutions if s.get('type') == 'organic'])
            inorganic_count = len([s for s in solutions if s.get('type') == 'inorganic'])
            
            print(f"   Solutions: {len(solutions)} total ({organic_count} organic, {inorganic_count} inorganic)")
            
            if disease.get('added_manually'):
                print(f"   ✏️  Added manually on {disease.get('added_date', 'Unknown date')}")

    def delete_disease(self):
        """Delete a disease from database"""
        if self.collection is None:
            print("❌ No database connection")
            return

        disease_name = input("Enter disease name to delete: ").strip()
        if not disease_name:
            print("❌ Disease name is required")
            return

        # Find disease
        disease = self.collection.find_one({"name": {"$regex": f"^{disease_name}$", "$options": "i"}})
        if not disease:
            print(f"❌ Disease '{disease_name}' not found")
            return

        # Confirm deletion
        print(f"\n⚠️  Found disease: {disease['name'].title()}")
        print(f"Description: {disease.get('description', 'No description')}")
        confirm = input("Are you sure you want to delete this disease? (y/n): ").strip().lower()
        
        if confirm == 'y':
            result = self.collection.delete_one({"_id": disease["_id"]})
            if result.deleted_count > 0:
                print(f"✅ Deleted disease '{disease['name']}' successfully!")
            else:
                print(f"❌ Failed to delete disease")
        else:
            print("❌ Deletion cancelled")

    def interactive_menu(self):
        """Interactive menu for disease management"""
        while True:
            print("\n🌾 AI Crop Diseases Solution - Disease Manager")
            print("=" * 60)
            print("1. ➕ Add new disease")
            print("2. 📋 List all diseases")
            print("3. 🗑️  Delete a disease")
            print("4. 📊 Database statistics")
            print("5. 🌐 Open web interface")
            print("6. 📝 Add sample diseases")
            print("0. ❌ Exit")
            
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                self.add_disease_interactive()
            elif choice == "2":
                self.list_all_diseases()
            elif choice == "3":
                self.delete_disease()
            elif choice == "4":
                self.show_database_stats()
            elif choice == "5":
                print("\n🌐 Web Interface URLs:")
                print("• Main App: http://127.0.0.1:8000/")
                print("• Database View: http://127.0.0.1:8000/database/")
            elif choice == "6":
                self.add_sample_diseases()
            else:
                print("❌ Invalid choice. Please try again.")

    def show_database_stats(self):
        """Show database statistics"""
        if self.collection is None:
            print("❌ No database connection")
            return

        print("\n📊 Database Statistics:")
        print("=" * 50)
        
        total_diseases = self.collection.count_documents({})
        manual_diseases = self.collection.count_documents({"added_manually": True})
        
        print(f"Total diseases: {total_diseases}")
        print(f"Manually added: {manual_diseases}")
        print(f"Sample diseases: {total_diseases - manual_diseases}")

    def add_sample_diseases(self):
        """Add some sample diseases"""
        sample_diseases = [
            {
                "name": "downy mildew",
                "description": "A fungal disease causing yellow spots on upper leaf surfaces and fuzzy growth underneath",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Copper-based fungicide spray",
                        "effectiveness": "High",
                        "application": "Apply every 7-10 days during humid conditions"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Metalaxyl systemic fungicide",
                        "effectiveness": "Very High",
                        "application": "Apply as soil drench or foliar spray"
                    }
                ]
            },
            {
                "name": "leaf spot",
                "description": "Circular brown or black spots on leaves, often with yellow halos",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Neem oil and baking soda mixture",
                        "effectiveness": "Medium",
                        "application": "Spray weekly on affected areas"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Chlorothalonil broad-spectrum fungicide",
                        "effectiveness": "High",
                        "application": "Apply every 14 days during growing season"
                    }
                ]
            }
        ]

        added_count = 0
        for disease in sample_diseases:
            if self.add_disease_from_dict(disease):
                added_count += 1

        print(f"\n✅ Added {added_count} sample diseases to database!")

def main():
    """Main function"""
    print("🚀 Starting Disease Manager...")
    
    # Create disease manager
    disease_manager = DiseaseManager()
    
    if disease_manager.client:
        # Start interactive menu
        disease_manager.interactive_menu()
    else:
        print("❌ Cannot start without MongoDB connection")
        print("💡 Make sure MongoDB is running: mongod --dbpath \"C:\\data\\db\"")

if __name__ == "__main__":
    main()
