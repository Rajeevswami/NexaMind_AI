from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import RegisterForm

def register(request):
    if request.user.is_authenticated: return redirect("dashboard:home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard:home")
    return render(request, "accounts/register.html", {"form": form})

