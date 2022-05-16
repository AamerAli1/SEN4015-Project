from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method != "POST":
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            new_user = authenticate(username=username, password=password ,email= email)
            new_user.is_active = False
            new_user.save()
            return redirect('product_catalog_app:waitingPage')


    context = {'form': form}
    return render(request, 'registration/register.html', context)