from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index'),
    path('profile/', views.profile_view, name='profile'),
    path('database/', views.view_database, name='database'),
    path('add-disease/', views.add_disease_form, name='add_disease'),
    path('search/', views.search_disease, name='search'),
    path('reset-db/', views.reset_database, name='reset_db'),
]
