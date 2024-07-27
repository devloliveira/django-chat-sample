from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from . import views


urlpatterns =[
    path('home/', views.HomeView.as_view()),
    path('', views.ChatIndexView.as_view()),
    path('room/<str:room_name>', views.ChatRoomView.as_view()),
    path('connection/request/<int:user_id>', views.ConnectionRequestView.as_view()),
    path('connection/accept/<int:author_id>', views.ConnectionAcceptView.as_view()),
    path('connection/reject/<int:author_id>', views.ConnectionRejectView.as_view()),
]