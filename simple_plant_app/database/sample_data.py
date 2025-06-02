"""
Sample Disease Data for Simple Plant Disease Solution
"""
from datetime import datetime

SAMPLE_DISEASES = [
    {
        "name": "powdery mildew",
        "description": "A fungal disease that appears as white powdery coating on leaves and stems",
        "solutions": [
            {
                "type": "organic",
                "solution": "Baking soda spray (1 tsp per quart water)",
                "effectiveness": "High",
                "application": "Spray weekly on affected areas"
            },
            {
                "type": "organic", 
                "solution": "Neem oil treatment",
                "effectiveness": "High",
                "application": "Apply every 2 weeks as preventive measure"
            },
            {
                "type": "inorganic",
                "solution": "Sulfur-based fungicide",
                "effectiveness": "Very High",
                "application": "Apply according to label instructions"
            }
        ],
        "added_date": datetime.now(),
        "sample_data": True
    },
    {
        "name": "blight",
        "description": "A plant disease causing brown spots and wilting of leaves and stems",
        "solutions": [
            {
                "type": "organic",
                "solution": "Copper sulfate spray",
                "effectiveness": "High",
                "application": "Apply every 7-10 days during humid conditions"
            },
            {
                "type": "inorganic",
                "solution": "Chlorothalonil fungicide",
                "effectiveness": "Very High",
                "application": "Apply every 14 days during growing season"
            }
        ],
        "added_date": datetime.now(),
        "sample_data": True
    },
    {
        "name": "aphid infestation",
        "description": "Small green or black insects clustering on stems and leaves, sucking plant juices",
        "solutions": [
            {
                "type": "organic",
                "solution": "Insecticidal soap spray",
                "effectiveness": "High",
                "application": "Spray directly on aphids, repeat every 3-5 days"
            },
            {
                "type": "inorganic",
                "solution": "Imidacloprid systemic insecticide",
                "effectiveness": "Very High",
                "application": "Apply as soil drench or foliar spray"
            }
        ],
        "added_date": datetime.now(),
        "sample_data": True
    },
    {
        "name": "black spot",
        "description": "Fungal disease causing black spots on leaves, common in roses and other plants",
        "solutions": [
            {
                "type": "organic",
                "solution": "Baking soda and oil spray",
                "effectiveness": "Medium",
                "application": "Mix 1 tsp baking soda + 1 tsp oil per quart water"
            },
            {
                "type": "inorganic",
                "solution": "Tebuconazole fungicide",
                "effectiveness": "High",
                "application": "Apply every 2-3 weeks during growing season"
            }
        ],
        "added_date": datetime.now(),
        "sample_data": True
    },
    {
        "name": "rust",
        "description": "A fungal disease causing orange-red pustules on leaf undersides",
        "solutions": [
            {
                "type": "organic",
                "solution": "Sulfur dust application",
                "effectiveness": "High",
                "application": "Dust leaves early morning when dew is present"
            },
            {
                "type": "inorganic",
                "solution": "Propiconazole systemic fungicide",
                "effectiveness": "Very High",
                "application": "Apply as preventive treatment every 21 days"
            }
        ],
        "added_date": datetime.now(),
        "sample_data": True
    }
]

def load_sample_data():
    """Load sample data into database"""
    from database.mongodb_setup import db
    
    print("🌱 Loading sample disease data...")
    
    # Check if data already exists
    existing_count = db.get_disease_count()
    if existing_count > 0:
        print(f"📊 Database already has {existing_count} diseases")
        return existing_count
    
    # Insert sample data
    inserted_count = 0
    for disease in SAMPLE_DISEASES:
        try:
            result = db.add_disease(disease)
            if result:
                inserted_count += 1
                print(f"✅ Added: {disease['name'].title()}")
        except Exception as e:
            print(f"❌ Error adding {disease['name']}: {e}")
    
    print(f"🎉 Loaded {inserted_count} sample diseases!")
    return inserted_count

if __name__ == "__main__":
    load_sample_data()
