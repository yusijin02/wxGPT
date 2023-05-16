from django.urls import path
from . import views

urlpatterns = [
    path('ChatGPT_post/', views.ChatGPT_post, name='ChatGPT_post'),
]