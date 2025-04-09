from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm  # Use the custom form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import pickle
import numpy as np
import pandas as pd

model = pickle.load(open(r'model-training/model.pkl', 'rb'))
label = pickle.load(open(r'model-training/label.pkl', 'rb'))
columns = pickle.load(open(r'model-training/columns.pkl', 'rb'))


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optional: auto-login after signup
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    if request.method == 'POST':
        nitrogen = request.POST.get('nitrogen')
        phosphorus = request.POST.get('phosphorus')
        potassium = request.POST.get('potassium')
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        ph = request.POST.get('ph')
        rainfall = request.POST.get('rainfall')     
        print(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
        data = np.array([nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall])
        df = pd.DataFrame([data], columns=columns)
        prediction = model.predict(df)
        crop = label.inverse_transform([prediction])[0]
        reason = 'Sudip is a good boy'
        print(crop)
        return redirect(f'recommend/?crop={crop}&reason={reason}')
    return render(request, 'new.html')

def recommend_view(request):
    crop = request.GET.get('crop', '')
    reason = request.GET.get('reason', '')
    return render(request, 'recommend.html', {'crop': crop, 'reason': reason})
