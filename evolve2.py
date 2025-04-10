import sqlite3
import pandas as pd

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

if __name__ == "__main__":
    try:
        N = float(input("Enter Nitrogen (N) level: "))
        P = float(input("Enter Phosphorus (P) level: "))
        K = float(input("Enter Potassium (K) level: "))
        temperature = float(input("Enter Temperature (°C): "))
        humidity = float(input("Enter Humidity (%): "))
        ph = float(input("Enter pH level: "))
        rainfall = float(input("Enter Rainfall (mm): "))
        label = input("Enter your label: ")

        insert_user(N, P, K, temperature, humidity, ph, rainfall, label)

        data_df = fetch_data_as_dataframe()
        print("\nStored Data:")
        print(data_df)

    except ValueError:
        print("Invalid input. Please enter numeric values where required.")
