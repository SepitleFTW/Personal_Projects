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

            #log user in and send them to settings

            #create profile object for the new user
            user_model = User.objects.get(username=username)
            new_profile = User.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect("singup")

        return render(request,'signup.html')
    else:
        return render(request,'signup.html')
