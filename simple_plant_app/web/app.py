"""
Simple Flask Web Application for Plant Disease Solution
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
from database.mongodb_setup import db
from config.settings import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, APP_NAME

app = Flask(__name__)
app.secret_key = 'simple_plant_disease_solution_key'

@app.route('/')
def index():
    """Home page with search functionality"""
    return render_template('index.html', app_name=APP_NAME)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search for diseases"""
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            diseases = db.search_diseases(query)
            return render_template('search.html', 
                                 diseases=diseases, 
                                 query=query,
                                 app_name=APP_NAME)
    
    return render_template('search.html', 
                         diseases=[], 
                         query='',
                         app_name=APP_NAME)

@app.route('/database')
def database():
    """View all diseases in database"""
    diseases = db.get_all_diseases()
    total_count = len(diseases)
    
    # Count solution types
    organic_count = 0
    inorganic_count = 0
    
    for disease in diseases:
        solutions = disease.get('solutions', [])
        for solution in solutions:
            if solution.get('type') == 'organic':
                organic_count += 1
            elif solution.get('type') == 'inorganic':
                inorganic_count += 1
    
    return render_template('database.html',
                         diseases=diseases,
                         total_count=total_count,
                         organic_count=organic_count,
                         inorganic_count=inorganic_count,
                         app_name=APP_NAME)

@app.route('/add-disease', methods=['GET', 'POST'])
def add_disease():
    """Add new disease to database"""
    if request.method == 'POST':
        try:
            # Get form data
            disease_name = request.form.get('disease_name', '').strip().lower()
            description = request.form.get('description', '').strip()
            
            if not disease_name:
                flash('Disease name is required', 'error')
                return render_template('add_disease.html', app_name=APP_NAME)
            
            # Get solutions
            solutions = []
            solution_types = request.form.getlist('solution_type')
            solution_texts = request.form.getlist('solution_text')
            effectiveness_levels = request.form.getlist('effectiveness')
            applications = request.form.getlist('application')
            
            for i in range(len(solution_types)):
                if solution_types[i] and solution_texts[i]:
                    solutions.append({
                        'type': solution_types[i],
                        'solution': solution_texts[i],
                        'effectiveness': effectiveness_levels[i] if i < len(effectiveness_levels) else 'Medium',
                        'application': applications[i] if i < len(applications) else 'Apply as directed'
                    })
            
            if not solutions:
                solutions.append({
                    'type': 'organic',
                    'solution': 'Consult agricultural expert for treatment options',
                    'effectiveness': 'Medium',
                    'application': 'Follow expert recommendations'
                })
            
            # Create disease document
            disease_data = {
                'name': disease_name,
                'description': description or f'A plant disease: {disease_name}',
                'solutions': solutions,
                'added_date': datetime.now(),
                'added_manually': True
            }
            
            # Add to database
            result = db.add_disease(disease_data)
            if result:
                flash(f'Disease "{disease_name}" added successfully!', 'success')
                return redirect(url_for('database'))
            else:
                flash('Error adding disease to database', 'error')
                
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('add_disease.html', app_name=APP_NAME)

@app.route('/api/diseases')
def api_diseases():
    """API endpoint to get all diseases"""
    diseases = db.get_all_diseases()
    
    # Convert ObjectId to string for JSON serialization
    for disease in diseases:
        disease['_id'] = str(disease['_id'])
    
    return jsonify({
        'diseases': diseases,
        'count': len(diseases)
    })

@app.route('/api/search/<query>')
def api_search(query):
    """API endpoint to search diseases"""
    diseases = db.search_diseases(query)
    
    # Convert ObjectId to string for JSON serialization
    for disease in diseases:
        disease['_id'] = str(disease['_id'])
    
    return jsonify({
        'diseases': diseases,
        'query': query,
        'count': len(diseases)
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    db_connected = db.is_connected()
    disease_count = db.get_disease_count()
    
    return jsonify({
        'status': 'healthy' if db_connected else 'unhealthy',
        'database_connected': db_connected,
        'disease_count': disease_count,
        'app_name': APP_NAME
    })

if __name__ == '__main__':
    print(f"🌱 Starting {APP_NAME}...")
    print(f"🌐 Server: http://{FLASK_HOST}:{FLASK_PORT}")
    
    # Load sample data if database is empty
    if db.get_disease_count() == 0:
        from database.sample_data import load_sample_data
        load_sample_data()
    
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
