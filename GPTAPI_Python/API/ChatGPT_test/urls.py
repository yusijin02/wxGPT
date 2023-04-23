from django.urls import path
from . import views

urlpatterns = [
    path('ChatGPT_test/', views.ChatGPT_test, name='ChatGPT_test'),
]