#!/usr/bin/env python3
"""
Project Cleanup Script for AI Crop Diseases Solution
Removes unnecessary files and cleans up the project structure
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Remove unnecessary files from the project"""
    
    print("🧹 AI Crop Diseases Solution - Project Cleanup")
    print("=" * 50)
    
    # Files to delete
    files_to_delete = [
        "templates/index.html",  # Duplicate template
        "app.py",               # Old Flask application
        "db.sqlite3",           # Unused SQLite database
        "plant_diseases.db",    # Old database file
    ]
    
    # Directories to delete
    dirs_to_delete = [
        "plants/__pycache__",
        "plant_django/__pycache__",
    ]
    
    deleted_files = []
    deleted_dirs = []
    errors = []
    
    # Delete files
    print("\n🗑️ Removing unnecessary files...")
    for file_path in files_to_delete:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                deleted_files.append(file_path)
                print(f"✅ Deleted: {file_path}")
            else:
                print(f"⚠️ Not found: {file_path}")
        except Exception as e:
            errors.append(f"❌ Error deleting {file_path}: {e}")
            print(f"❌ Error deleting {file_path}: {e}")
    
    # Delete directories
    print("\n🗂️ Removing cache directories...")
    for dir_path in dirs_to_delete:
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                deleted_dirs.append(dir_path)
                print(f"✅ Deleted directory: {dir_path}")
            else:
                print(f"⚠️ Not found: {dir_path}")
        except Exception as e:
            errors.append(f"❌ Error deleting {dir_path}: {e}")
            print(f"❌ Error deleting {dir_path}: {e}")
    
    # Summary
    print("\n📊 Cleanup Summary:")
    print("-" * 30)
    print(f"✅ Files deleted: {len(deleted_files)}")
    print(f"✅ Directories deleted: {len(deleted_dirs)}")
    print(f"❌ Errors: {len(errors)}")
    
    if deleted_files:
        print(f"\n🗑️ Deleted Files:")
        for file in deleted_files:
            print(f"  - {file}")
    
    if deleted_dirs:
        print(f"\n🗂️ Deleted Directories:")
        for dir in deleted_dirs:
            print(f"  - {dir}")
    
    if errors:
        print(f"\n❌ Errors:")
        for error in errors:
            print(f"  - {error}")
    
    print(f"\n🎉 Project cleanup completed!")
    print(f"📁 Your project is now clean and ready for presentation.")

def show_remaining_structure():
    """Show the clean project structure"""
    
    print("\n📁 Clean Project Structure:")
    print("=" * 40)
    
    essential_files = [
        "📁 AI Crop Diseases Solution/",
        "├── 🔧 manage.py",
        "├── 📦 requirements.txt",
        "├── 📁 plant_django/",
        "│   ├── ⚙️ settings.py",
        "│   ├── 🌐 urls.py",
        "│   ├── 🚀 wsgi.py",
        "│   └── 📄 asgi.py",
        "├── 📁 plants/",
        "│   ├── 🎯 views.py",
        "│   ├── 🌐 urls.py",
        "│   ├── 📊 models.py",
        "│   ├── ⚙️ admin.py",
        "│   ├── 📱 apps.py",
        "│   ├── 🧪 tests.py",
        "│   ├── 📁 templates/plants/",
        "│   │   ├── 🏠 index.html",
        "│   │   ├── 🔐 login.html",
        "│   │   ├── 📝 signup.html",
        "│   │   └── 🗄️ database.html",
        "│   ├── 📁 migrations/",
        "│   └── 📁 management/",
        "├── 📚 Documentation/",
        "│   ├── 📖 PROJECT_EXPLANATION.md",
        "│   ├── 🔐 AUTHENTICATION_GUIDE.md",
        "│   ├── 🧭 COMPASS_VISUAL_GUIDE.md",
        "│   ├── 📊 DISEASE_DATABASE_SUMMARY.md",
        "│   ├── 🔧 MONGODB_COMPASS_SETUP.md",
        "│   └── 📚 MONGODB_DATABASE_GUIDE.md",
        "└── 🧪 test_mongodb_connection.py"
    ]
    
    for item in essential_files:
        print(item)

if __name__ == "__main__":
    # Run cleanup
    cleanup_project()
    
    # Show clean structure
    show_remaining_structure()
    
    print(f"\n💡 Next Steps:")
    print("1. Review PROJECT_EXPLANATION.md for detailed file explanations")
    print("2. Present the clean project structure to your senior")
    print("3. Highlight the professional architecture and documentation")
    print("4. Demonstrate the working application features")
    
    print(f"\n🌾 Your AI Crop Diseases Solution is ready for presentation! ✨")
