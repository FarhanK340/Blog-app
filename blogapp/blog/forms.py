from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'thumbnail', 'content']
        
        
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-class'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-class'})
    )
    

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')