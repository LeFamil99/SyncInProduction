from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Permet de générer un formulaire de création de compte inclus dans django 
# avec des option personnalisées
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Entrer une adresse valide')

    # L'array fields détermine quels champs inclure dans le formulaire
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]