from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
from bson import ObjectId
import logging
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection setup with error handling
try:
    # MongoDB connection with timeout and error handling
    client = MongoClient(
        'mongodb://localhost:27017/',
        serverSelectionTimeoutMS=5000,  # 5 second timeout
        connectTimeoutMS=10000,         # 10 second connection timeout
        socketTimeoutMS=20000           # 20 second socket timeout
    )

    # Test the connection
    client.admin.command('ping')
    logger.info("✅ Successfully connected to MongoDB!")

    db = client['plant_diseases']

except errors.ServerSelectionTimeoutError as e:
    logger.error(f"❌ MongoDB connection failed: {e}")
    logger.error("Please ensure MongoDB is running on localhost:27017")
    db = None
except Exception as e:
    logger.error(f"❌ Unexpected MongoDB error: {e}")
    db = None

def init_db():
    # Check if collections exist, if not create them
    if 'diseases' not in db.list_collection_names():
        db.create_collection('diseases')
    
    if 'solutions' not in db.list_collection_names():
        db.create_collection('solutions')
    
    # Insert sample data if collections are empty
    if db.diseases.count_documents({}) == 0:
        sample_data = [
            {
                "name": "powdery mildew",
                "description": "A fungal disease that appears as white powdery spots on leaves and stems",
                "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop&q=80",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Mix 1 tablespoon baking soda with 1 gallon of water",
                        "image": "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "High",
                        "application": "Spray on affected areas every 7-10 days"
                    },
                    {
                        "type": "organic",
                        "solution": "Apply milk spray (40% milk to 60% water)",
                        "image": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Medium",
                        "application": "Spray early morning or evening"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Apply potassium bicarbonate fungicides",
                        "image": "https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Very High",
                        "application": "Follow manufacturer's instructions"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Use synthetic fungicides containing myclobutanil",
                        "image": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Very High",
                        "application": "Professional application recommended"
                    }
                ]
            },
            {
                "name": "blight",
                "description": "A plant disease causing browning and death of plant tissues",
                "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop&q=80",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Apply copper-based fungicides",
                        "image": "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "High",
                        "application": "Apply during dry weather conditions"
                    },
                    {
                        "type": "organic",
                        "solution": "Use Bacillus subtilis biological fungicide",
                        "image": "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Medium",
                        "application": "Apply as preventive measure"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Apply chlorothalonil every 7-10 days",
                        "image": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Very High",
                        "application": "Regular scheduled applications"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Use mancozeb or maneb fungicides",
                        "image": "https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Very High",
                        "application": "Follow safety guidelines strictly"
                    }
                ]
            },
            {
                "name": "rust",
                "description": "A fungal disease causing orange or rust-colored spots on leaves",
                "image": "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop&q=80",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Apply sulfur dust or spray early in the season",
                        "image": "https://images.unsplash.com/photo-1574263867128-a3d5c1b1deae?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "High",
                        "application": "Early morning application preferred"
                    },
                    {
                        "type": "organic",
                        "solution": "Use neem oil every 7-14 days",
                        "image": "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Medium",
                        "application": "Avoid application during hot weather"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Apply myclobutanil or propiconazole fungicides",
                        "image": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Very High",
                        "application": "Professional consultation recommended"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Use tebuconazole for severe infections",
                        "image": "https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Very High",
                        "application": "Last resort for severe cases"
                    }
                ]
            },
            {
                "name": "aphid infestation",
                "description": "Small insects that feed on plant sap, causing yellowing and stunted growth",
                "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop&q=80",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Spray with insecticidal soap solution",
                        "image": "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "High",
                        "application": "Apply every 3-5 days until controlled"
                    },
                    {
                        "type": "organic",
                        "solution": "Release ladybugs as natural predators",
                        "image": "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Very High",
                        "application": "Release in early morning or evening"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Apply systemic insecticides like imidacloprid",
                        "image": "https://images.unsplash.com/photo-1576086213369-97a306d36557?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Very High",
                        "application": "Follow label instructions carefully"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Use pyrethroid-based contact insecticides",
                        "image": "https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "High",
                        "application": "Apply during cooler parts of the day"
                    }
                ]
            },
            {
                "name": "black spot",
                "description": "Fungal disease causing black spots on leaves, common in roses",
                "image": "https://images.unsplash.com/photo-1574263867128-a3d5c1b1deae?w=400&h=300&fit=crop&q=80",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Apply baking soda and oil spray",
                        "image": "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Medium",
                        "application": "Spray weekly during growing season"
                    },
                    {
                        "type": "organic",
                        "solution": "Use compost tea as foliar spray",
                        "image": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Medium",
                        "application": "Apply every 2 weeks"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Apply triazole fungicides",
                        "image": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "Very High",
                        "application": "Start applications early in season"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Use copper-based fungicides",
                        "image": "https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=300&h=200&fit=crop&q=80",
                        "effectiveness": "High",
                        "application": "Apply before symptoms appear"
                    }
                ]
            }
        ]

        db.diseases.insert_many(sample_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    disease_input = request.json.get('disease', '').lower()

    # MongoDB query with case-insensitive search
    disease = db.diseases.find_one(
        {"name": {"$regex": f".*{disease_input}.*", "$options": "i"}}
    )

    if not disease:
        return jsonify({"error": "Disease not found"}), 404

    # Organize solutions by type with enhanced data
    solutions = {"organic": [], "inorganic": []}
    for solution in disease.get('solutions', []):
        solution_data = {
            "solution": solution['solution'],
            "image": solution.get('image', ''),
            "effectiveness": solution.get('effectiveness', 'Unknown'),
            "application": solution.get('application', 'Follow standard guidelines')
        }
        solutions[solution['type']].append(solution_data)

    return jsonify({
        "disease": disease['name'],
        "description": disease.get('description', ''),
        "image": disease.get('image', ''),
        "solutions": solutions
    })

@app.route('/reset-db', methods=['POST'])
def reset_database():
    """Reset database with new image data structure"""
    try:
        # Drop existing collections
        db.diseases.drop()
        db.solutions.drop()

        # Reinitialize with new data
        init_db()

        return jsonify({"message": "Database reset successfully with image support!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)