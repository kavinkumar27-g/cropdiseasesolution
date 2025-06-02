from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum, Count
from .models import UserProfile, UserSession
import json
from pymongo import MongoClient
import logging

# MongoDB connection
logger = logging.getLogger(__name__)

try:
    print("🔄 Attempting MongoDB connection...")
    client = MongoClient('mongodb://localhost:27017/')
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
    logger.info("✅ Successfully connected to MongoDB!")
    db = client['plant_diseases']
    print(f"📊 Database: {db.name}")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    logger.error(f"❌ MongoDB connection failed: {e}")
    db = None

def login_view(request):
    """Render the login page"""
    if request.user.is_authenticated:
        return redirect('plants:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('plants:index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please enter both username and password.')

    return render(request, 'plants/login.html')

def signup_view(request):
    """Render the signup page"""
    if request.user.is_authenticated:
        return redirect('plants:index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validation
        errors = []

        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists.')

        if not email:
            errors.append('Email is required.')
        else:
            try:
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    errors.append('Email already exists.')
            except ValidationError:
                errors.append('Please enter a valid email address.')

        if not first_name:
            errors.append('First name is required.')

        if not password:
            errors.append('Password is required.')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long.')

        if password != confirm_password:
            errors.append('Passwords do not match.')

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Create user
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                messages.success(request, f'Account created successfully! Welcome, {first_name}!')

                # Auto-login the user
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('plants:index')
                else:
                    return redirect('plants:login')

            except Exception as e:
                messages.error(request, 'An error occurred while creating your account. Please try again.')

    return render(request, 'plants/signup.html')

def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('plants:login')

@login_required
def index(request):
    """Render the main page"""
    return render(request, 'plants/index.html')

@login_required
def profile_view(request):
    """User profile page with visit statistics"""
    try:
        # Helper function to format duration
        def format_duration(seconds):
            if seconds == 0:
                return "0s"
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60

            if hours > 0:
                return f"{hours}h {minutes}m {secs}s"
            elif minutes > 0:
                return f"{minutes}m {secs}s"
            else:
                return f"{secs}s"

        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'total_visits': 0,
                'total_time_spent': 0,
                'last_visit': timezone.now()
            }
        )

        # Get user sessions and format duration
        sessions = UserSession.objects.filter(user=request.user).order_by('-session_start')[:10]
        formatted_sessions = []
        for session in sessions:
            # Calculate relative time
            time_diff = timezone.now() - session.session_start
            if time_diff.days > 0:
                relative_time = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
            elif time_diff.seconds > 3600:
                hours = time_diff.seconds // 3600
                relative_time = f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif time_diff.seconds > 60:
                minutes = time_diff.seconds // 60
                relative_time = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                relative_time = "Just now"

            session_dict = {
                'session_start': session.session_start,
                'duration': session.duration,
                'duration_formatted': format_duration(session.duration) if session.duration > 0 else "Active",
                'pages_visited': session.pages_visited,
                'relative_time': relative_time,
                'is_recent': time_diff.days < 1,  # Mark as recent if within 24 hours
            }
            formatted_sessions.append(session_dict)

        # Calculate statistics
        total_sessions = UserSession.objects.filter(user=request.user).count()
        avg_session_duration = UserSession.objects.filter(
            user=request.user,
            duration__gt=0
        ).aggregate(avg_duration=Sum('duration'))['avg_duration'] or 0

        if total_sessions > 0 and avg_session_duration:
            avg_session_duration = avg_session_duration // total_sessions
        else:
            avg_session_duration = 0

        # Get recent activity (last 7 days)
        week_ago = timezone.now() - timezone.timedelta(days=7)
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timezone.timedelta(days=1)

        # Recent sessions (last 7 days)
        recent_sessions = UserSession.objects.filter(
            user=request.user,
            session_start__gte=week_ago
        ).count()

        # Recent time spent (last 7 days)
        recent_time = UserSession.objects.filter(
            user=request.user,
            session_start__gte=week_ago
        ).aggregate(total_time=Sum('duration'))['total_time'] or 0

        # Today's activity
        today_sessions = UserSession.objects.filter(
            user=request.user,
            session_start__gte=today
        ).count()

        today_time = UserSession.objects.filter(
            user=request.user,
            session_start__gte=today
        ).aggregate(total_time=Sum('duration'))['total_time'] or 0

        # Yesterday's activity
        yesterday_sessions = UserSession.objects.filter(
            user=request.user,
            session_start__gte=yesterday,
            session_start__lt=today
        ).count()

        yesterday_time = UserSession.objects.filter(
            user=request.user,
            session_start__gte=yesterday,
            session_start__lt=today
        ).aggregate(total_time=Sum('duration'))['total_time'] or 0

        # Activity by day (last 7 days)
        daily_activity = []
        for i in range(7):
            day_start = today - timezone.timedelta(days=i)
            day_end = day_start + timezone.timedelta(days=1)

            day_sessions = UserSession.objects.filter(
                user=request.user,
                session_start__gte=day_start,
                session_start__lt=day_end
            ).count()

            day_time = UserSession.objects.filter(
                user=request.user,
                session_start__gte=day_start,
                session_start__lt=day_end
            ).aggregate(total_time=Sum('duration'))['total_time'] or 0

            if i == 0:
                day_name = "Today"
            elif i == 1:
                day_name = "Yesterday"
            else:
                day_name = day_start.strftime("%A")

            daily_activity.append({
                'day_name': day_name,
                'date': day_start.strftime("%b %d"),
                'sessions': day_sessions,
                'time_spent': format_duration(day_time),
                'has_activity': day_sessions > 0
            })

        # Calculate additional user stats
        days_since_joined = (timezone.now() - request.user.date_joined).days

        context = {
            'profile': profile,
            'sessions': formatted_sessions,
            'total_sessions': total_sessions,
            'avg_session_duration': format_duration(avg_session_duration),
            'total_time_formatted': profile.get_total_time_formatted(),
            'recent_sessions': recent_sessions,
            'recent_time_formatted': format_duration(recent_time),
            'member_since': request.user.date_joined,
            'days_since_joined': days_since_joined,
            'user_full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            # Enhanced recent activity data
            'today_sessions': today_sessions,
            'today_time_formatted': format_duration(today_time),
            'yesterday_sessions': yesterday_sessions,
            'yesterday_time_formatted': format_duration(yesterday_time),
            'daily_activity': daily_activity,
            'has_recent_activity': recent_sessions > 0,
        }

        return render(request, 'plants/profile.html', context)

    except Exception as e:
        messages.error(request, f'Error loading profile: {str(e)}')
        return redirect('plants:index')

def view_database(request):
    """View MongoDB database content"""
    try:
        if db is None:
            # Try to reconnect to MongoDB
            try:
                from pymongo import MongoClient
                client = MongoClient('mongodb://localhost:27017/')
                client.admin.command('ping')
                db_temp = client['plant_diseases']
                diseases = list(db_temp.diseases.find({}))

                # Convert ObjectId to string and rename for template compatibility
                for disease in diseases:
                    if '_id' in disease:
                        disease['id'] = str(disease['_id'])
                        del disease['_id']

                context = {
                    'diseases': diseases,
                    'total_diseases': len(diseases),
                    'database_name': 'plant_diseases',
                    'collection_name': 'diseases'
                }
                return render(request, 'plants/database.html', context)

            except Exception as reconnect_error:
                context = {
                    'error': f"Database connection failed: {reconnect_error}",
                    'diseases': [],
                    'total_diseases': 0,
                    'database_name': 'plant_diseases',
                    'collection_name': 'diseases'
                }
                return render(request, 'plants/database.html', context)

        # Get all diseases from MongoDB
        diseases = list(db.diseases.find({}))

        # Convert ObjectId to string and rename for template compatibility
        for disease in diseases:
            if '_id' in disease:
                disease['id'] = str(disease['_id'])
                del disease['_id']

        context = {
            'diseases': diseases,
            'total_diseases': len(diseases),
            'database_name': 'plant_diseases',
            'collection_name': 'diseases'
        }

        return render(request, 'plants/database.html', context)

    except Exception as e:
        context = {
            'error': str(e),
            'diseases': [],
            'total_diseases': 0,
            'database_name': 'plant_diseases',
            'collection_name': 'diseases'
        }
        return render(request, 'plants/database.html', context)

def add_disease_form(request):
    """Display form to add new disease"""
    if request.method == 'GET':
        return render(request, 'plants/add_disease.html')

    elif request.method == 'POST':
        try:
            # Get form data
            disease_name = request.POST.get('disease_name', '').strip().lower()
            description = request.POST.get('description', '').strip()

            if not disease_name:
                messages.error(request, 'Disease name is required')
                return render(request, 'plants/add_disease.html')

            # Check if disease already exists
            if db and db.diseases.find_one({"name": disease_name}):
                messages.error(request, f'Disease "{disease_name}" already exists')
                return render(request, 'plants/add_disease.html')

            # Get solutions
            solutions = []
            solution_count = int(request.POST.get('solution_count', 0))

            for i in range(solution_count):
                sol_type = request.POST.get(f'solution_type_{i}', '').strip()
                sol_text = request.POST.get(f'solution_text_{i}', '').strip()
                effectiveness = request.POST.get(f'effectiveness_{i}', '').strip()
                application = request.POST.get(f'application_{i}', '').strip()

                if sol_type and sol_text:
                    solutions.append({
                        'type': sol_type,
                        'solution': sol_text,
                        'effectiveness': effectiveness or 'Medium',
                        'application': application or 'Apply as directed'
                    })

            if not solutions:
                solutions.append({
                    'type': 'organic',
                    'solution': 'Consult agricultural expert for treatment options',
                    'effectiveness': 'Medium',
                    'application': 'Follow expert recommendations'
                })

            # Create disease document
            disease_doc = {
                'name': disease_name,
                'description': description or f'A plant disease: {disease_name}',
                'solutions': solutions,
                'added_date': timezone.now(),
                'added_manually': True
            }

            # Insert into database
            if db:
                result = db.diseases.insert_one(disease_doc)
                messages.success(request, f'Disease "{disease_name}" added successfully!')
                return redirect('plants:view_database')
            else:
                messages.error(request, 'Database connection failed')
                return render(request, 'plants/add_disease.html')

        except Exception as e:
            messages.error(request, f'Error adding disease: {str(e)}')
            return render(request, 'plants/add_disease.html')



@csrf_exempt
@require_http_methods(["POST"])
def search_disease(request):
    """Search for disease solutions"""
    try:
        if db is None:
            return JsonResponse({"error": "Database connection failed"}, status=500)

        data = json.loads(request.body)
        disease_input = data.get('disease', '').lower()

        if not disease_input:
            return JsonResponse({"error": "Please enter a disease name"}, status=400)

        # Search for disease (case-insensitive) using MongoDB
        disease = db.diseases.find_one(
            {"name": {"$regex": f".*{disease_input}.*", "$options": "i"}}
        )

        if not disease:
            return JsonResponse({"error": "Disease not found"}, status=404)

        # Organize solutions by type
        solutions = {"organic": [], "inorganic": []}
        for solution in disease.get('solutions', []):
            solution_data = {
                "solution": solution['solution'],
                "effectiveness": solution.get('effectiveness', 'Unknown'),
                "application": solution.get('application', 'Follow standard guidelines')
            }
            solutions[solution['type']].append(solution_data)

        return JsonResponse({
            "disease": disease['name'],
            "description": disease.get('description', ''),
            "solutions": solutions
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def reset_database(request):
    """Reset database with sample data"""
    try:
        if db is None:
            return JsonResponse({"error": "Database connection failed"}, status=500)

        # Clear existing data
        db.diseases.drop()

        # Sample data - text only, no images
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
                    },
                    {
                        "type": "inorganic",
                        "solution": "Systemic fungicide (myclobutanil)",
                        "effectiveness": "Very High",
                        "application": "Professional application recommended"
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
                        "type": "organic",
                        "solution": "Bacillus subtilis biological control",
                        "effectiveness": "Medium",
                        "application": "Apply as preventive treatment"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Chlorothalonil fungicide",
                        "effectiveness": "Very High",
                        "application": "Apply every 7-14 days"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Mancozeb fungicide",
                        "effectiveness": "Very High",
                        "application": "Use with protective equipment"
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
                        "type": "organic",
                        "solution": "Neem oil spray treatment",
                        "effectiveness": "Medium",
                        "application": "Apply in cool weather, avoid hot sun"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Propiconazole systemic fungicide",
                        "effectiveness": "Very High",
                        "application": "Apply at first sign of disease"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Tebuconazole for severe cases",
                        "effectiveness": "Very High",
                        "application": "Professional application only"
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
                        "type": "organic",
                        "solution": "Ladybug biological control",
                        "effectiveness": "Very High",
                        "application": "Release 1500 per garden in evening"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Imidacloprid systemic insecticide",
                        "effectiveness": "Very High",
                        "application": "Soil drench or foliar spray"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Pyrethrin contact spray",
                        "effectiveness": "High",
                        "application": "Apply in early morning or evening"
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
                        "type": "organic",
                        "solution": "Copper fungicide spray",
                        "effectiveness": "High",
                        "application": "Apply every 7-14 days"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Trifloxystrobin fungicide",
                        "effectiveness": "Very High",
                        "application": "Apply at first sign of disease"
                    }
                ]
            },
            {
                "name": "downy mildew",
                "description": "Fungal disease causing yellow patches and fuzzy growth on leaf undersides",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Improve air circulation and reduce humidity",
                        "effectiveness": "Medium",
                        "application": "Space plants properly, prune for airflow"
                    },
                    {
                        "type": "organic",
                        "solution": "Copper hydroxide spray",
                        "effectiveness": "High",
                        "application": "Apply in early morning"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Metalaxyl systemic fungicide",
                        "effectiveness": "Very High",
                        "application": "Soil drench and foliar spray"
                    }
                ]
            },
            {
                "name": "spider mites",
                "description": "Tiny pests causing stippled leaves and fine webbing",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Predatory mites release",
                        "effectiveness": "Very High",
                        "application": "Release when mites first detected"
                    },
                    {
                        "type": "organic",
                        "solution": "Neem oil and water spray",
                        "effectiveness": "High",
                        "application": "Spray undersides of leaves weekly"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Abamectin miticide",
                        "effectiveness": "Very High",
                        "application": "Apply with spreader-sticker"
                    }
                ]
            },
            {
                "name": "leaf spot",
                "description": "Fungal or bacterial disease causing circular spots on leaves",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Remove affected leaves and improve air circulation",
                        "effectiveness": "Medium",
                        "application": "Prune infected parts and dispose properly"
                    },
                    {
                        "type": "organic",
                        "solution": "Copper-based organic fungicide",
                        "effectiveness": "High",
                        "application": "Apply every 10-14 days"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Chlorothalonil fungicide spray",
                        "effectiveness": "Very High",
                        "application": "Apply according to label directions"
                    }
                ]
            },
            {
                "name": "anthracnose",
                "description": "Fungal disease causing dark, sunken lesions on leaves and fruits",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Copper sulfate spray treatment",
                        "effectiveness": "High",
                        "application": "Apply during cool, wet weather"
                    },
                    {
                        "type": "organic",
                        "solution": "Bacillus subtilis biological fungicide",
                        "effectiveness": "Medium",
                        "application": "Apply as preventive treatment"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Azoxystrobin systemic fungicide",
                        "effectiveness": "Very High",
                        "application": "Apply at first sign of disease"
                    }
                ]
            },
            {
                "name": "fusarium wilt",
                "description": "Soil-borne fungal disease causing yellowing and wilting of plants",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Soil solarization and crop rotation",
                        "effectiveness": "Medium",
                        "application": "Cover soil with plastic for 6-8 weeks in summer"
                    },
                    {
                        "type": "organic",
                        "solution": "Trichoderma biological control",
                        "effectiveness": "High",
                        "application": "Apply to soil before planting"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Benomyl systemic fungicide",
                        "effectiveness": "High",
                        "application": "Soil drench treatment"
                    }
                ]
            },
            {
                "name": "bacterial canker",
                "description": "Bacterial infection causing sunken, dark lesions on stems and branches",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Copper hydroxide spray",
                        "effectiveness": "High",
                        "application": "Apply during dormant season"
                    },
                    {
                        "type": "organic",
                        "solution": "Prune infected branches and sterilize tools",
                        "effectiveness": "Medium",
                        "application": "Cut 6 inches below infected area"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Streptomycin antibiotic spray",
                        "effectiveness": "Very High",
                        "application": "Apply during bloom period"
                    }
                ]
            },
            {
                "name": "scale insects",
                "description": "Small, hard-shelled insects that attach to stems and leaves",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Horticultural oil spray",
                        "effectiveness": "High",
                        "application": "Apply during dormant season"
                    },
                    {
                        "type": "organic",
                        "solution": "Beneficial parasitic wasps release",
                        "effectiveness": "Very High",
                        "application": "Release when scales are detected"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Systemic insecticide (imidacloprid)",
                        "effectiveness": "Very High",
                        "application": "Soil application in spring"
                    }
                ]
            },
            {
                "name": "thrips",
                "description": "Tiny insects causing silvery streaks and black spots on leaves",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Blue sticky traps",
                        "effectiveness": "Medium",
                        "application": "Place traps around affected plants"
                    },
                    {
                        "type": "organic",
                        "solution": "Predatory mites (Amblyseius cucumeris)",
                        "effectiveness": "High",
                        "application": "Release in greenhouse or garden"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Spinosad insecticide spray",
                        "effectiveness": "Very High",
                        "application": "Apply in evening to avoid bee exposure"
                    }
                ]
            },
            {
                "name": "whitefly",
                "description": "Small white flying insects that cluster on leaf undersides",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Yellow sticky traps",
                        "effectiveness": "Medium",
                        "application": "Place traps near affected plants"
                    },
                    {
                        "type": "organic",
                        "solution": "Encarsia formosa parasitic wasp",
                        "effectiveness": "Very High",
                        "application": "Release in greenhouse environments"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Acetamiprid systemic insecticide",
                        "effectiveness": "Very High",
                        "application": "Apply as soil drench or foliar spray"
                    }
                ]
            },
            {
                "name": "root rot",
                "description": "Fungal disease affecting plant roots, causing yellowing and wilting",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Improve drainage and reduce watering",
                        "effectiveness": "High",
                        "application": "Ensure proper soil drainage"
                    },
                    {
                        "type": "organic",
                        "solution": "Mycorrhizal fungi inoculant",
                        "effectiveness": "Medium",
                        "application": "Apply to soil around roots"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Metalaxyl fungicide soil drench",
                        "effectiveness": "Very High",
                        "application": "Apply to soil around affected plants"
                    }
                ]
            },
            {
                "name": "fire blight",
                "description": "Bacterial disease causing blackened, burnt appearance in branches",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Prune infected branches during dry weather",
                        "effectiveness": "High",
                        "application": "Cut 12 inches below infected area"
                    },
                    {
                        "type": "organic",
                        "solution": "Copper sulfate spray",
                        "effectiveness": "Medium",
                        "application": "Apply during dormant season"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Streptomycin antibiotic spray",
                        "effectiveness": "Very High",
                        "application": "Apply during bloom period"
                    }
                ]
            },
            {
                "name": "mosaic virus",
                "description": "Viral disease causing mottled yellow and green patterns on leaves",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Remove infected plants immediately",
                        "effectiveness": "High",
                        "application": "Destroy infected plants to prevent spread"
                    },
                    {
                        "type": "organic",
                        "solution": "Control aphid vectors with beneficial insects",
                        "effectiveness": "Medium",
                        "application": "Release ladybugs and lacewings"
                    },
                    {
                        "type": "inorganic",
                        "solution": "No chemical cure - focus on prevention",
                        "effectiveness": "Low",
                        "application": "Use virus-resistant plant varieties"
                    }
                ]
            },
            {
                "name": "clubroot",
                "description": "Soil-borne disease causing swollen, distorted roots in brassicas",
                "solutions": [
                    {
                        "type": "organic",
                        "solution": "Lime application to raise soil pH",
                        "effectiveness": "High",
                        "application": "Apply lime to achieve pH 7.2 or higher"
                    },
                    {
                        "type": "organic",
                        "solution": "Long crop rotation (7+ years)",
                        "effectiveness": "Very High",
                        "application": "Avoid brassicas for 7-10 years"
                    },
                    {
                        "type": "inorganic",
                        "solution": "Fluazinam fungicide soil treatment",
                        "effectiveness": "High",
                        "application": "Apply before planting susceptible crops"
                    }
                ]
            }
        ]

        # Insert data into MongoDB
        db.diseases.insert_many(sample_diseases)

        return JsonResponse({"message": "Database reset successfully with Django and MongoDB!"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
