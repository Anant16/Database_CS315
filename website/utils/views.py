# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.shortcuts import render

# # Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render


def registration(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registration/success.html')
    return render(request, 'registration/registration.html', {'form': form})


