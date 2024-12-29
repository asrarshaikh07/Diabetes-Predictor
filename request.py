import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={
    'Glucose':150, 
    'BloodPressure':80, 
    'Insulin':150,
    'BMI':50,
    'DiabetesPedigreeFunction':0.888
    })

print(r.json())