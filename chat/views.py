from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q

from django import forms
from .models import UserConnection, STATUS


class HomeView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request):
        all_users = User.objects.filter(
            ~Q(username=request.user.username),
            Q(is_active=True)
        )
        context = {
            'all_users': all_users
        }

        return render(
            request,
            'home.html',
            context=context
        )


class ConnectionRequestView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, user_id):
        target_user = User.objects.filter(Q(id=user_id)).first()
        connection = UserConnection.get_connection(request.user, target_user)

        if connection:
            return HttpResponse('Connection already exists', status=409)
        else:
            UserConnection.objects.create(author=request.user, target_user=target_user)
            return HttpResponse(status=200)


class ConnectionAcceptView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, author_id):
        author = User.objects.filter(Q(id=author_id)).first()
        connection = UserConnection.get_connection(request.user, author, status='p')

        if connection:
            connection.status = 'a'
            connection.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse('No pending connection not found', status=404)


class ConnectionRejectView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, author_id):
        author = User.objects.filter(Q(id=author_id)).first()
        connection = UserConnection.get_connection(request.user, author, status='p')

        if connection:
            connection.status = 'r'
            connection.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse('No pending connection not found', status=404)



class ChatIndexView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request):
        context = {
            'contacts_data': [],
            'current_user': request.user,
        }

        all_users = User.objects.filter(
            ~Q(id = request.user.id)
        )

        for user in all_users:
            context['contacts_data'].append({
                'contact': user,
                'connection': UserConnection.get_connection(request.user, user),
            })
        return render(request, 'index.html', context=context)


class ChatRoomView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request, room_name: str):
        return render(request, 'room.html', {
            'current_user': request.user,
            'room_name': room_name
        })
