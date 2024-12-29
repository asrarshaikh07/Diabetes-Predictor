import numpy as np
from flask import Flask,request,jsonify,render_template
import pickle

# ['Glucose','BloodPressure','Insulin','BMI','DiabetesPedigreeFunction']
app=Flask(__name__)

model=pickle.load(open('random_forest_classifier.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    try:
        # for rendering results on html gui
        # Collect form data and convert to float
        Glucose = float(request.form['Glucose'])
        BloodPressure = float(request.form['BloodPressure'])
        Insulin = float(request.form['Insulin'])
        BMI = float(request.form['BMI'])
        DiabetesPedigreeFunction = float(request.form['DiabetesPedigreeFunction'])

        # Make prediction
        result = model.predict([[Glucose, BloodPressure, Insulin,BMI,DiabetesPedigreeFunction]])
        
        # Convert result to a human-readable format
        prediction = result[0]  # Assuming it returns [0] or [1], etc.
        class_labels = {0: "Congratulations , you dont have diabetes ",1: "Be Careful !! You have Diabetes "}
        class_name = class_labels.get((int(prediction)))
        # result = model.predict([[age, totchol, sysbp, diabp, bmi, heartrate, glucose]])
        print("Raw Prediction:", result)
        # Pass prediction to the template
        return render_template('index.html', result=class_name)
    
    except Exception as e: return render_template('index.html', result=f"An error occurred: {e}")
    
    except ValueError:
        # Handle any conversion errors or missing input
        return render_template('index.html', result="Invalid input. Please enter valid numbers for all fields.")

@app.route('/predict_api',methods=['POST'])
def predict_api():
    try:
            
        # for direct calls through api request

        data= request.get_json(force=True)
        prediction = model.predict([np.array(list(data.values()))])

        output = {'prediction':int(prediction[0])}
        return jsonify(output)
    except ValueError:
        # Handle any conversion errors
        return jsonify({'error': 'Invalid input. Ensure all values are numeric.'}), 400
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500 
    

# Add the new endpoints here
@app.route('/sample', methods=['GET'])
def sample():
    sample_data = {
        "Glucose": 45,
        "BloodPressure": 200,
        "Insulin": 120,
        "BMI": 25.5,
        "DiabetesPedigreeFunction": 72
    }
    return jsonify(sample_data)

@app.route('/explain', methods=['GET'])
def explain():
    explanation = {
       "Glucose": "Glucose Level",
        "BloodPressure": "BloodPressure Level",
        "Insulin": "Insulin Level",
        "BMI": "Body Mass Index",
        "DiabetesPedigreeFunction": "Diabetes Level"
    }
    return jsonify(explanation)

if __name__ == '__main__':
    app.run(debug=True)

    