from django.shortcuts import render
from django.http import HttpResponse
from login.models import Profile

# Create your views here.

def index(response):

    return render(response, "main/index.html")
