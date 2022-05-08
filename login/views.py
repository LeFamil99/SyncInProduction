from django.shortcuts import render

def login (response): 

    return render(response, "login/log-in.html")
