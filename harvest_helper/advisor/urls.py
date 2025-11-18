# advisor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.get_recommendation, name='get_recommendation'),
    path('chat/', views.ai_chat_helper, name='ai_chat_helper'), # <-- ADD THIS LINE
]
