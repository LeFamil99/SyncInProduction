from django.shortcuts import render
from .forms import SignUpForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

# Crée la vue et gère les requêtes HTTP de la page pour créer un compte
class Signup(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# Crée la vue et gère les requêtes HTTP de la page pour se connecter
class Signin(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
