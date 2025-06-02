from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserProfile, UserSession
import time

class UserTrackingMiddleware:
    """
    Middleware to track user visits and time spent on the website
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request before view
        if request.user.is_authenticated:
            self.process_request(request)
        
        response = self.get_response(request)
        
        # Process response after view
        if request.user.is_authenticated:
            self.process_response(request, response)
        
        return response

    def process_request(self, request):
        """Track session start and page visits"""
        try:
            # Get or create user profile
            profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'total_visits': 0,
                    'total_time_spent': 0,
                    'last_visit': timezone.now()
                }
            )
            
            # Check if this is a new session (no session or session expired)
            session_key = f"user_session_{request.user.id}"
            
            if session_key not in request.session:
                # New session - increment visit count
                profile.total_visits += 1
                profile.last_visit = timezone.now()
                profile.save()
                
                # Create new session record
                user_session = UserSession.objects.create(
                    user=request.user,
                    session_start=timezone.now(),
                    pages_visited=1
                )
                
                # Store session info
                request.session[session_key] = {
                    'session_id': user_session.id,
                    'start_time': time.time(),
                    'last_activity': time.time(),
                    'pages_visited': 1
                }
            else:
                # Existing session - update page count
                session_data = request.session[session_key]
                session_data['pages_visited'] += 1
                session_data['last_activity'] = time.time()
                request.session[session_key] = session_data
                
                # Update session record
                try:
                    user_session = UserSession.objects.get(id=session_data['session_id'])
                    user_session.pages_visited = session_data['pages_visited']
                    user_session.save()
                except UserSession.DoesNotExist:
                    pass
                    
        except Exception as e:
            # Log error but don't break the request
            print(f"UserTrackingMiddleware error in process_request: {e}")

    def process_response(self, request, response):
        """Update session duration"""
        try:
            session_key = f"user_session_{request.user.id}"
            
            if session_key in request.session:
                session_data = request.session[session_key]
                current_time = time.time()
                
                # Calculate session duration
                session_duration = int(current_time - session_data['start_time'])
                
                # Update session record
                try:
                    user_session = UserSession.objects.get(id=session_data['session_id'])
                    user_session.duration = session_duration
                    user_session.save()
                    
                    # Update user profile total time
                    profile = UserProfile.objects.get(user=request.user)
                    # Calculate the difference from last recorded session duration
                    last_recorded_duration = getattr(user_session, '_last_duration', 0)
                    time_diff = session_duration - last_recorded_duration

                    if time_diff > 0 and time_diff < 300:  # Only add reasonable time differences (less than 5 minutes)
                        profile.total_time_spent += time_diff
                        profile.save()
                        user_session._last_duration = session_duration
                            
                except (UserSession.DoesNotExist, UserProfile.DoesNotExist):
                    pass
                    
        except Exception as e:
            # Log error but don't break the response
            print(f"UserTrackingMiddleware error in process_response: {e}")
        
        return response
