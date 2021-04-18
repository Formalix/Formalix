from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.

        
    else:
        pass
        # Return an 'invalid login' error message.
        

def logout_user(request):
    logout(request)






# Create your views here.


