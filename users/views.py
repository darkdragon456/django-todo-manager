from django.shortcuts import render, redirect
from .forms import customRegistrationForm
from django.contrib import messages
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        register_form = customRegistrationForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'User created successfully')
            return redirect('todolist')

    else:
        register_form = customRegistrationForm()

    return render(request, 'register.html', {
        'register_form': register_form
    })


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')