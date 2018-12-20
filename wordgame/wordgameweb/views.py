from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    return render(request, 'wordgameweb/login.html')



#takes user to home page, if they are logged in
@login_required
def home(request):
    return render(request, 'wordgameweb/home.html')