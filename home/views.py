from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def index(request):
    return render(request, "index.html")

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optional auto-login
            return redirect('index')
    else:
        form = UserCreationForm()
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
        # Get data from the form
        nitrogen = request.POST.get('nitrogen')
        phosphorus = request.POST.get('phosphorus')
        potassium = request.POST.get('potassium')
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        ph = request.POST.get('ph')
        rainfall = request.POST.get('rainfall')

        # Handle the data and return recommendations
        # Here, you'll call your crop recommendation logic with the input data
        # Example: recommendations = recommend_crops(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)

        # For now, let's just send the values back for display purposes
        recommendations = f"Your input data: Nitrogen={nitrogen}, Phosphorus={phosphorus}, Potassium={potassium}, Temperature={temperature}, Humidity={humidity}, pH={ph}, Rainfall={rainfall}"
        print(recommendations)
        # Optionally, you could pass the recommendations to the template to display them
        return redirect('recommend')
    
    return render(request, "index.html")

def recommend_view(request):
    return render(request, "recommend.html")
