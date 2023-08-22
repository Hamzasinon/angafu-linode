from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .utils import is_admin, is_manager
from .form import *

def connecte (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request,("Nom utilisateur incorrect ou Mot de passe incorrect"))
            return redirect('connecte')
    else:
        return render(request,'connecte.html')
    
def deconnecte(request):
    logout(request)
    messages.success(request,("Vous êtes deconnecte"))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Utilisateur créé avec succès')
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})

@user_passes_test(is_admin)
def admin_view(request):
    # Votre code pour la vue admin
    pass

@user_passes_test(is_manager)
def manager_view(request):
    # Votre code pour la vue manager
    pass

def access_denied(request):
    return HttpResponseForbidden("Accès refusé.")
