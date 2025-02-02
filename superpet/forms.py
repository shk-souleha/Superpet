from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User       #built-in model User given by django

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        #fields="__all__"
        fields=["username","first_name","last_name","email"]