"""
Simple Plant Disease Solution - Configuration
"""

# MongoDB Configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DATABASE_NAME = 'simple_plant_diseases'
COLLECTION_NAME = 'diseases'

# Flask Configuration
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000
FLASK_DEBUG = True

# Application Settings
APP_NAME = 'Simple Plant Disease Solution'
APP_VERSION = '1.0.0'

# Database Connection String
MONGODB_URI = f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}/'
