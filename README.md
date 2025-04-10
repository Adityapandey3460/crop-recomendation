🌾 Crop Prediction Model using ML
This project leverages Machine Learning to predict the most suitable crop based on key agricultural inputs like soil nutrients, humidity, pH, and temperature. It empowers farmers and planners to make informed crop decisions using environmental data and market trends.

🔍 Features:
Predicts the best crop using SGDRegressor. It also choose the best crop for current market trend.

Why use SGDRegressor:
It gives good accuracy in this type of data and also supports partial-fit to train the model in the new incoming data. Because of this we dont need to re-train the model on the whole data.

Takes user inputs for:

Nitrogen (N), Phosphorous (P), Potassium (K) [kg/ha]

Soil Humidity [%]

pH Value

Temperature [°C]

High accuracy and performance on labeled crop datasets.

🛠 Technologies:
Python, Scikit-learn, Pandas, NumPy

Jupyter Notebook / Python Script

Reasoning : From the distribution of the data we find out the best range values for which a crop can be grown. The used an LLM's api to show the reasoning to the user more clearly and descriptively.

Include more features (rainfall, soil type)

Deploy as a web or mobile application

📦 Requirements:
﻿asgiref==3.8.1
Django==5.2
gunicorn==23.0.0
joblib==1.4.2
numpy==2.2.4
packaging==24.2
pandas==2.2.3
python-dateutil==2.9.0.post0
pytz==2025.2
scikit-learn==1.5.0
scipy==1.15.2
six==1.17.0
sqlparse==0.5.3
threadpoolctl==3.6.0
tzdata==2025.2
requests

👥 Team:
Akash Mondal, Sudip Mondal, Aditya Pandey, Utsav Dinda


