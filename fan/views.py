from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
import qrcodefunctions as q
import os

from .models import Creator

from .forms import CreateAccountForm, LoginForm

def homeView(request):
    context = {"name": "Arjun & Josh"}
    return render(request, "home.html", context)

def createAccountView(request):
    # TODO: only works for admins
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            new_user = User(username = request.POST["email"], password = request.POST["password"])
            new_user.save()
            print(new_user)
            print("account created")
            return render(request, "createAccount_success.html")
        # TODO handle invalid account information
    
    form = CreateAccountForm()
    context = {"form": form}
    return render(request, "createAccount_form.html", context)

def loginView(request):
    context = {}
    if request.method == 'POST':
        print(request.POST['email'])
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        # TODO message about account login success status, you are logged in or please create an account
        if user is not None:
            print("logged in")
            login(request, user)
            return render(request, "login_success.html")
        else:
            print("login failed, try again")


    form = LoginForm()
    context = {"form": form}
    return render(request, "login_form.html", context)

def qrView(request, id):
    q.make_website_link_qr(id)
    context = {"filename": str(id)}
    return render(request, "qr.html", context)


def creatorDashboardView(request):
    user = request.user
    creator = Creator.objects.filter(user=user)
    print(creator)

    context = {"username": str(user)}
    return render(request, "creator_dashboard.html", context)
