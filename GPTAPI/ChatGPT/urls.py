from django.urls import path
from . import views

urlpatterns = [
    path('ChatGPT/', views.ChatGPT, name='ChatGPT'),
]