#!/usr/bin/env python
"""
Migrate Disease Data to Correct Format
Convert old schema to new schema for web display
"""
from pymongo import MongoClient
from datetime import datetime

def migrate_disease_data():
    """Convert old schema diseases to new schema"""
    print("🔄 Migrating Disease Data to Correct Format...")
    print("=" * 60)
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['plant_diseases']
        collection = db['diseases']
        
        # Find diseases with old schema
        old_schema_diseases = list(collection.find({
            "disease_name": {"$exists": True},
            "name": {"$exists": False}
        }))
        
        print(f"📊 Found {len(old_schema_diseases)} diseases to migrate")
        
        migrated_count = 0
        
        for disease in old_schema_diseases:
            try:
                # Extract data from old schema
                disease_name = disease.get('disease_name', '').lower()
                recommended_treatment = disease.get('recommended_treatment', '')
                fertilisers = disease.get('fertilisers', '')
                pesticides = disease.get('pesticides', '')
                
                # Create description based on disease name
                descriptions = {
                    'anthracnose': 'A fungal disease causing dark, sunken lesions on fruits, leaves, and stems',
                    'downy mildew': 'A fungal disease causing yellow spots on upper leaf surfaces with fuzzy growth underneath',
                    'bacterial wilt': 'A bacterial disease causing sudden wilting and death of plants',
                    'early blight': 'A fungal disease causing brown spots with concentric rings on leaves',
                    'late blight': 'A devastating fungal disease causing dark, water-soaked lesions on leaves and fruits',
                    'black rot': 'A fungal disease causing black, circular lesions on leaves and fruits',
                    'root rot': 'A fungal disease affecting plant roots, causing yellowing and wilting',
                    'sooty mold': 'A fungal disease causing black, sooty coating on leaves and stems',
                    'canker': 'A fungal disease causing sunken, dead areas on stems and branches',
                    'mosaic virus': 'A viral disease causing mottled yellow and green patterns on leaves'
                }
                
                description = descriptions.get(disease_name, f'A plant disease: {disease_name}')
                
                # Create solutions array
                solutions = []
                
                # Add organic solution (fertilizers)
                if fertilisers and fertilisers.strip():
                    organic_solution = {
                        'type': 'organic',
                        'solution': f'Apply {fertilisers.lower()}',
                        'effectiveness': 'Medium',
                        'application': 'Apply as soil amendment or foliar feed'
                    }
                    solutions.append(organic_solution)
                
                # Add inorganic solution (pesticides)
                if pesticides and pesticides.strip():
                    inorganic_solution = {
                        'type': 'inorganic',
                        'solution': pesticides,
                        'effectiveness': 'High',
                        'application': 'Apply according to label instructions'
                    }
                    solutions.append(inorganic_solution)
                
                # Add general treatment if available
                if recommended_treatment and recommended_treatment.strip():
                    general_solution = {
                        'type': 'organic',
                        'solution': recommended_treatment,
                        'effectiveness': 'High',
                        'application': 'Follow recommended practices'
                    }
                    solutions.append(general_solution)
                
                # Ensure at least one solution
                if not solutions:
                    solutions.append({
                        'type': 'organic',
                        'solution': 'Consult agricultural expert for treatment options',
                        'effectiveness': 'Medium',
                        'application': 'Follow expert recommendations'
                    })
                
                # Create new document with correct schema
                new_document = {
                    'name': disease_name,
                    'description': description,
                    'solutions': solutions,
                    'migrated_from_old_schema': True,
                    'migration_date': datetime.now(),
                    'original_data': {
                        'disease_name': disease.get('disease_name'),
                        'recommended_treatment': disease.get('recommended_treatment'),
                        'fertilisers': disease.get('fertilisers'),
                        'pesticides': disease.get('pesticides')
                    }
                }
                
                # Replace the old document
                result = collection.replace_one(
                    {'_id': disease['_id']},
                    new_document
                )
                
                if result.modified_count > 0:
                    migrated_count += 1
                    print(f"✅ Migrated: {disease_name.title()}")
                    print(f"   Solutions: {len(solutions)}")
                    print(f"   Description: {description[:50]}...")
                
            except Exception as e:
                print(f"❌ Error migrating {disease.get('disease_name', 'Unknown')}: {e}")
        
        print(f"\n🎉 Migration Complete!")
        print(f"✅ Successfully migrated {migrated_count} diseases")
        
        # Show final statistics
        total_diseases = collection.count_documents({})
        valid_diseases = collection.count_documents({
            'name': {'$exists': True, '$ne': ''},
            'solutions': {'$exists': True, '$not': {'$size': 0}}
        })
        
        print(f"\n📊 Final Database Statistics:")
        print(f"Total diseases: {total_diseases}")
        print(f"Valid diseases: {valid_diseases}")
        print(f"Migrated diseases: {migrated_count}")
        
        return migrated_count
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return 0

def show_all_diseases():
    """Show all diseases after migration"""
    print("\n📋 All Diseases After Migration:")
    print("=" * 60)
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['plant_diseases']
        collection = db['diseases']
        
        diseases = list(collection.find({}).sort('name', 1))
        
        for i, disease in enumerate(diseases, 1):
            name = disease.get('name', 'Unknown').title()
            solutions = disease.get('solutions', [])
            migrated = disease.get('migrated_from_old_schema', False)
            manual = disease.get('added_manually', False)
            
            organic_count = len([s for s in solutions if s.get('type') == 'organic'])
            inorganic_count = len([s for s in solutions if s.get('type') == 'inorganic'])
            
            print(f"{i:2d}. {name}")
            print(f"    💊 {len(solutions)} solutions ({organic_count} organic, {inorganic_count} inorganic)")
            
            if migrated:
                print(f"    🔄 Migrated from old schema")
            elif manual:
                print(f"    ✏️  Added manually")
            else:
                print(f"    📦 Sample data")
        
        return len(diseases)
        
    except Exception as e:
        print(f"❌ Error showing diseases: {e}")
        return 0

def main():
    """Main migration function"""
    print("🚀 Disease Data Migration Tool")
    print("=" * 60)
    
    # Perform migration
    migrated_count = migrate_disease_data()
    
    if migrated_count > 0:
        # Show all diseases
        total_count = show_all_diseases()
        
        print(f"\n🎉 SUCCESS! Your additional {migrated_count} diseases are now ready!")
        print(f"📊 Total diseases available: {total_count}")
        
        print(f"\n🌐 Test your web interface:")
        print(f"• Database View: http://127.0.0.1:8000/database/")
        print(f"• Search: http://127.0.0.1:8000/")
        
        print(f"\n🔍 You can now search for:")
        disease_names = [
            'Anthracnose', 'Downy Mildew', 'Bacterial Wilt', 'Early Blight', 'Late Blight',
            'Black Rot', 'Root Rot', 'Sooty Mold', 'Canker', 'Mosaic Virus'
        ]
        for name in disease_names:
            print(f"  • {name}")
    else:
        print(f"\n⚠️  No diseases were migrated. Check if data is already in correct format.")

if __name__ == "__main__":
    main()
