from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import User
from django.http import HttpResponse

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            return HttpResponse(
                '<div class="alert alert-error">Username already exists</div>'
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        login(request, user)

        response = HttpResponse()
        response["HX-Redirect"] = "/dashboard/"
        return response

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = HttpResponse()
            response["HX-Redirect"] = "/dashboard/"
            return response
        else:
            return HttpResponse(
                '<div class="alert alert-error">Invalid username or password</div>'
            )

    return render(request, "login.html")
