from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
import pickle
import numpy as np
import pandas as pd
import random

# Load ML model and supporting data
model = pickle.load(open(r'model-training/model.pkl', 'rb'))
label = pickle.load(open(r'model-training/label.pkl', 'rb'))
columns = pickle.load(open(r'model-training/columns.pkl', 'rb'))

with open(r'model-training/crop_ranges_95.pkl', "rb") as f:
    crop_ranges_95 = pickle.load(f)


# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')


# Generate reasoning for crop recommendation
def generate_crop_reasoning(crop_name, user_input, crop_ranges):
    reasoning = []

    crop_range = crop_ranges.get(crop_name)
    if not crop_range:
        return f"❌ No range data found for '{crop_name}'. Please check crop name or dataset."

    for feature, value in user_input.items():
        if feature not in crop_range:
            continue

        low, high = crop_range[feature]
        param = feature.upper()

        if low <= value <= high:
            messages = [
                f"✔️ {param} value of {value} is ideal for {crop_name}, within the preferred range ({low}–{high}).",
                f"✅ Your {param} level ({value}) perfectly supports optimal growth of {crop_name}.",
                f"👍 Excellent! {param} is well balanced for {crop_name}, promoting strong yield."
            ]
        elif value < low:
            messages = [
                f"⚠️ {param} value of {value} is lower than optimal for {crop_name}. Ideal range is {low}–{high}.",
                f"🔽 {param} is slightly deficient for {crop_name}. Consider increasing it toward {low}.",
                f"⚠️ Insufficient {param} might slow down {crop_name} growth. Raise it closer to {low}–{high}."
            ]
        else:  # value > high
            messages = [
                f"⚠️ {param} value of {value} is too high for {crop_name}. Recommended range is {low}–{high}.",
                f"🔺 Excess {param} may harm {crop_name}'s growth. Try reducing it below {high}.",
                f"⚡ Too much {param} can stress {crop_name}. Adjust to keep it within {low}–{high}."
            ]

        reasoning.append(random.choice(messages))

    return "\n".join(reasoning)


# Index view for crop prediction
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        try:
            user_input = {
                "Nitrogen": float(request.POST.get('nitrogen')),
                "Phosphorus": float(request.POST.get('phosphorus')),
                "Potassium": float(request.POST.get('potassium')),
                "temperature": float(request.POST.get('temperature')),
                "humidity": float(request.POST.get('humidity')),
                "ph": float(request.POST.get('ph')),
                "rainfall": float(request.POST.get('rainfall')),
            }

            df = pd.DataFrame([list(user_input.values())], columns=list(user_input.keys()))
            prediction = model.predict(df)
            crop = prediction[0]
            reason = generate_crop_reasoning(crop, user_input, crop_ranges_95)

            return redirect(f'recommend/?crop={crop}&reason={reason}')

        except Exception as e:
            messages.error(request, f"Something went wrong: {e}")

    return render(request, 'index.html')


# Recommend result page
def recommend_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    crop = request.GET.get('crop', '')
    reason = request.GET.get('reason', '')
    return render(request, 'recommend.html', {'crop': crop, 'reason': reason})