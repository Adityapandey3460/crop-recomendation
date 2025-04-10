from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm  # Use the custom form
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import pickle
import numpy as np
import pandas as pd


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
    return redirect('login')

import random

# Load your pre-saved crop range dictionary from pickle
with open(r'model-training/crop_ranges_95.pkl', "rb") as f:
    crop_ranges_95 = pickle.load(f)

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
                f"✔ {param} value of {value} is ideal for {crop_name}, within the preferred range ({low}–{high}).",
                f"✅ Your {param} level ({value}) perfectly supports optimal growth of {crop_name}.",
                f"👍 Excellent! {param} is well balanced for {crop_name}, promoting strong yield."
            ]
        elif value < low:
            messages = [
                f"⚠ {param} value of {value} is lower than optimal for {crop_name}. Ideal range is {low}–{high}.",
                f"🔽 {param} is slightly deficient for {crop_name}. Consider increasing it toward {low}.",
                f"⚠ Insufficient {param} might slow down {crop_name} growth. Raise it closer to {low}–{high}."
            ]
        else:  # value > high
            messages = [
                f"⚠ {param} value of {value} is too high for {crop_name}. Recommended range is {low}–{high}.",
                f"🔺 Excess {param} may harm {crop_name}'s growth. Try reducing it below {high}.",
                f"⚡ Too much {param} can stress {crop_name}. Adjust to keep it within {low}–{high}."
            ]

        reasoning.append(random.choice(messages))

    return "\n".join(reasoning)

# Example user input
# user_input = {
#     "N": 90,
#     "P": 42,
#     "K": 43,
#     "temperature": 20.8,
#     "humidity": 82.0,
#     "ph": 6.5,
#     "rainfall": 202.9
# }

# predicted_crop = "apple"

# # Output reasoning
# print(f"\n🌱 Recommendation Reason for '{predicted_crop.upper()}':\n")
# print(generate_crop_reasoning(predicted_crop, user_input, crop_ranges_95))




# def index(request):
#     if request.method == 'POST':
#         nitrogen = request.POST.get('nitrogen')
#         phosphorus = request.POST.get('phosphorus')
#         potassium = request.POST.get('potassium')
#         temperature = request.POST.get('temperature')
#         humidity = request.POST.get('humidity')
#         ph = request.POST.get('ph')
#         rainfall = request.POST.get('rainfall')     
#         user_input = {
#             "N": nitrogen,
#             "P": phosphorus,
#             "K": potassium,
#             "temperature": temperature,
#             "humidity": humidity,
#             "ph": ph,
#             "rainfall": rainfall
#         }
#         print(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
#         data = np.array([nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall])
#         df = pd.DataFrame([data], columns=columns)
#         prediction = model.predict(df)
#         global crop
#         crop = label.inverse_transform([prediction])[0]
#         print(crop)
#         global reason
#         reason=generate_crop_reasoning(crop, user_input, crop_ranges_95)
#         print(generate_crop_reasoning(crop, user_input, crop_ranges_95))
#         return redirect('recommend')
#     return render(request, 'new.html')

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        nitrogen = float(request.POST.get('nitrogen'))
        phosphorus = float(request.POST.get('phosphorus'))
        potassium = float(request.POST.get('potassium'))
        temperature = float(request.POST.get('temperature'))
        humidity = float(request.POST.get('humidity'))
        ph = float(request.POST.get('ph'))
        rainfall = float(request.POST.get('rainfall'))

        user_input = {
            "Nitrogen": nitrogen,
            "Phosphorus": phosphorus,
            "Potassium": potassium,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }

        print(user_input)
        
        model = pickle.load(open(r'model-training/model.pkl', 'rb'))
        label = pickle.load(open(r'model-training/label.pkl', 'rb'))
        columns = pickle.load(open(r'model-training/columns.pkl', 'rb'))
        df = pd.DataFrame([list(user_input.values())], columns=list(user_input.keys()))

        df.rename(columns={
            'Nitrogen': 'N',
            'Phosphorus': 'P',
            'Potassium': 'K'
        }, inplace=True)

        prediction = model.predict_proba(df)
        safe_scores = np.nan_to_num(prediction, nan=-np.inf)
        top3_indices = np.argsort(safe_scores, axis=1)[:, -3:][:, ::-1]
        print("Top 3 class indices for each sample:\n", top3_indices)
        class_names = label.classes_
        top3_class_names = [[class_names[i] for i in row] for row in top3_indices]
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(BASE_DIR, 'models-traning', 'crop_trend_ranking.pkl')
        with open(r"model-training/crop_trend_ranking.pkl", "rb") as f:
            trend_df = pickle.load(f)
        
            filtered = trend_df[trend_df["Crop"].isin(top3_class_names[0])]

            filtered_sorted = filtered.sort_values(by="TrendScore", ascending=False)
        
        print("📊 Final Top 3 Sorted by Market Trend:")
        print(filtered_sorted)
        print("Top 3 predicted classes per sample:\n", top3_class_names)
        reason =  generate_crop_reasoning
        global crops
        crops = [
            {'crop': filtered_sorted['Crop'].iloc[0], 'confidence':95, 'reason':reason(filtered_sorted['Crop'].iloc[0], user_input, crop_ranges_95)}, 
            {'crop': filtered_sorted['Crop'].iloc[1], 'confidence':65, 'reason':reason(filtered_sorted['Crop'].iloc[1], user_input, crop_ranges_95)}, {'crop':filtered_sorted['Crop'].iloc[2], 'confidence':25, 'reason':reason(filtered_sorted['Crop'].iloc[2], user_input, crop_ranges_95)}
        ]
    
        print(crops)
        return redirect('recommend')

    return render(request, 'index.html')

    

def recommend_view(request):
    return render(request, "recommend.html", {'crops': crops})

import requests

token = "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"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {
    "Authorization": f"Bearer {token}"
}

def simplify_text(text):
    prompt = f"{text}\n\nGive a simplified and informative version of the above text, no need to mention problems—just suggest what to do within 100 words."
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 300
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        result = response.json()
        output = result[0]["generated_text"]
        output = output.replace("Give a simplified and informative version of the above text, no need to mention problems—just suggest what to do within 100 words.", "")
        output =  output.replace(text, "")
        output = output.strip()
        print(output)
        return output
    
    except Exception as e:
        print("Error:", response.status_code, response.text)
        return None
    



import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import os

def model_train():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(BASE_DIR, 'models', 'model.pkl')
    classes_path = os.path.join(BASE_DIR, 'models', 'classes.pkl')
    label_path = os.path.join(BASE_DIR, 'models', 'label.pkl')
    data = fetch_data_as_dataframe()
    data = data.drop(columns='id')
    print('data base :', data.columns)
    if data.shape[0] > 2:
        if not os.path.exists(model_path):
            print("⚠️ Model file not found!")
            return

        model = pickle.load(open(model_path, 'rb'))
        classes = pickle.load(open(classes_path, 'rb'))
        label = pickle.load(open(label_path, 'rb'))
        data['label'] = label.transform(data['label'])
        x_train, x_test, y_train, y_test = train_test_split(
                data.drop(columns=['label']),
                data['label'],
                test_size=0.1,
                random_state=42
            )
        
        model.partial_fit(x_train, y_train, classes=np.unique(data['label']))

        sample = x_test.iloc[0].values.reshape(1, -1)
        probs = model.predict_proba(sample)
        print("Prediction probabilities:", probs)

        pickle.dump(model, open(os.path.join(BASE_DIR, 'models', 'model1.pkl'), 'wb'))

import sqlite3

def insert_user(N, P, K, temperature, humidity, ph, rainfall, label):
    conn = sqlite3.connect('mydata3.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            N REAL,
            P REAL,
            K REAL,
            temperature REAL,
            humidity REAL,
            ph REAL,
            rainfall REAL,
            label TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO users (N, P, K, temperature, humidity, ph, rainfall, label)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (N, P, K, temperature, humidity, ph, rainfall, label))

    conn.commit()
    conn.close()
    print("User data added successfully.")

def fetch_data_as_dataframe():
    conn = sqlite3.connect('mydata3.db')
    
    df = pd.read_sql_query("SELECT * FROM users", conn)
    
    conn.close()
    return df
