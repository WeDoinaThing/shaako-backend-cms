from django.shortcuts import render, redirect
from django.contrib import auth

from customuser.models import UserManager, User

def landing(request):
    if request.user.is_authenticated:
        if request.user.is_superadmin:
            return redirect("super_admin_home")
        else:
            return redirect("ngo_admin_home")

    else:
        print("Not Authenticated")
        return redirect("login")


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(
            email=email,
        )
        user.set_password(password)
        user.save()
        
    return redirect("login")


def home_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_authenticated:
                if user.is_superadmin:
                    print("Super Admins")
                    return redirect("super_admin_home")
                else:
                    print("NGO Admin")
                    return redirect("ngo_admin_home")
            else:
                print("Not Authenticated")

        else:
            print("Not Found")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    auth.logout(request)
    return redirect("/")