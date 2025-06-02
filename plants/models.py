from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# We'll use PyMongo directly for MongoDB operations
# These models are just for Django admin if needed

class Disease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_visits = models.IntegerField(default=0)
    total_time_spent = models.IntegerField(default=0)  # in seconds
    last_visit = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_total_time_formatted(self):
        """Return total time in human readable format"""
        hours = self.total_time_spent // 3600
        minutes = (self.total_time_spent % 3600) // 60
        seconds = self.total_time_spent % 60

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)  # in seconds
    pages_visited = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.session_start.strftime('%Y-%m-%d %H:%M')}"
