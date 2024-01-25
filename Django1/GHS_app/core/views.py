from django.shortcuts import render, redirect
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

        if User.objects.filter(email=email).exists():
            messages.info(request, "This email is already in use")
            return redirect("signup")

        elif User.objects.filter(username=username).exists():
            messages.info(request, "This Username is already in use")
            return redirect("signup")

        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            #

        return render(request,'signup.html')
    else:
        return render(request,'signup.html')
