from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']



        Profile.objects.create(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        return render(request,'signup.html')
    else:
        return render(request,'signup.html')
