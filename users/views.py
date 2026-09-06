from django.shortcuts import redirect, render
from . forms import CustomUserCreationForm
from django.http import HttpResponse
from django.contrib import messages

from users.forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        registration_form = CustomUserCreationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect("todolist")   
    else:
        registration_form = CustomUserCreationForm()
    return render(request, "register.html", {"form": registration_form})


