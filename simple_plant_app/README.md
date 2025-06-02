# 🌱 Simple Plant Disease Solution

A simplified version of the AI Crop Diseases Solution with clean, easy-to-understand code.

## 📁 Folder Structure

```
simple_plant_app/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── run_app.py               # Simple startup script
├── database/
│   ├── mongodb_setup.py     # MongoDB connection and setup
│   ├── sample_data.py       # Sample disease data
│   └── database_manager.py  # Simple database operations
├── web/
│   ├── app.py               # Simple Flask web application
│   ├── templates/           # HTML templates
│   │   ├── index.html       # Home page
│   │   ├── search.html      # Search page
│   │   ├── database.html    # Database view
│   │   └── add_disease.html # Add disease form
│   └── static/              # CSS and JavaScript
│       ├── style.css        # Simple styling
│       └── script.js        # Basic JavaScript
├── tools/
│   ├── add_disease.py       # Command-line tool to add diseases
│   ├── search_disease.py    # Command-line search tool
│   └── backup_database.py   # Database backup tool
└── config/
    └── settings.py          # Simple configuration
```

## 🚀 Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start MongoDB:**
   ```bash
   mongod --dbpath "C:\data\db"
   ```

3. **Run the Application:**
   ```bash
   python run_app.py
   ```

4. **Open Browser:**
   ```
   http://localhost:5000
   ```

## ✨ Features

- **Simple Web Interface** - Clean, easy-to-use design
- **Disease Search** - Find diseases by name
- **Database View** - Browse all diseases
- **Add Diseases** - Simple form to add new diseases
- **Command Line Tools** - Scripts for database management
- **MongoDB Integration** - Reliable data storage

## 🎯 Key Simplifications

- **Flask instead of Django** - Simpler web framework
- **Minimal dependencies** - Only essential packages
- **Clear file organization** - Easy to understand structure
- **Simple configuration** - One settings file
- **Basic styling** - Clean, professional appearance
- **Straightforward code** - Easy to read and modify
