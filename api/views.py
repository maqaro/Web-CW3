from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserForm

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            ))
        else:
            form = UserForm()
    return render(request, 'api/spa/register.html', {'form': form})

def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_spa')
        else:
            return render(request, 'api/spa/login.html', {'error': 'Invalid credentials'})
    return render(request, 'api/spa/login.html', {})