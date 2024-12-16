from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('olympics.urls')),  # All olympics-related routes
]
