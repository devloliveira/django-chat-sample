import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from urllib.parse import parse_qs
from django.contrib.auth import authenticate, login, logout


from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(help_text="Username")
    password = forms.CharField(help_text="Username")


class HomeView(View):

    def get(self, request):
        if not getattr(request.user, 'is_authenticated', False):
            return redirect('/login/')
        return redirect('/chat/')


class LoginView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        if not getattr(request.user, 'is_authenticated', False):
            return render(request, 'registration/login.html', {'form': LoginForm()})
        return redirect('/chat/')

    def post(self, request):
        request_data = None

        if request.POST:
            request_data = request.POST
        elif request.body:
            request_data = json.loads(request.body)

        form = LoginForm(request_data)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, 'Login sucessful!')
                return HttpResponse(status=200)
            else:
                # messages.error(request, 'Username or password invalid')
                # return render(request, 'registration/login.html', context, status=401)
                return HttpResponse(status=401)
        else:
            return HttpResponse(status=401)


class LogoutView(View):
    http_method_names = ['get']
    def get(self, request):
        logout(request)
        return redirect('/login/')
