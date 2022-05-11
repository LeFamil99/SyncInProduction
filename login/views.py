from django.shortcuts import render
from .forms import SignUpForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class Signup(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class Signin(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
