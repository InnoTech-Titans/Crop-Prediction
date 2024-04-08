from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import requests
from flask import jsonify
import random
from flask_sqlalchemy import SQLAlchemy

api_key = "AIzaSyDVxTej4dwhhFTaGRFHYHeuFwwxYBWaWE8"
cx = "c5bc3c5d3db9e4084"


app = Flask(__name__,
            static_folder="templates/assets")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store_values.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    ph = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    predicted_crop = db.Column(db.String)

def fetch_image_urls(query):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": cx,
        "key": api_key,
        "searchType": "image",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract image URLs from the response
    image_urls = [item["link"] for item in data.get("items", [])]

    return image_urls

def read_data():
    csv_file_path = 'tt.csv'
    df = pd.read_csv(csv_file_path)
    ch_values = df[['CH1', 'CH2', 'CH3', 'CH4', 'CH5']]
    ch_values_array = ch_values.values
    final_data = ch_values_array[0]

    return final_data

@app.route('/get_values', methods=['GET'])
def get_values():
    # Call the read_data function to get values
    data = read_data()

    data = [item.item() if isinstance(item, np.int64) else item for item in data]

    ph_value, rainfall_value = generate_random()
    # with app.app_context():
    #     new_value = Value(nitrogen=data[0], phosphorus=data[1], potassium=data[2],
    #                     temperature=data[3], humidity=data[4], ph=ph_value,
    #                     rainfall=rainfall_value, predicted_crop=prediction[0])
    #     db.session.add(new_value)
    #     db.session.commit()

    # Prepare the response in JSON format
    response = {
        'Nitrogen': data[0],
        'Phosphorus': data[1],
        'Potassium': data[2],
        'Temperature': data[3],
        'Humidity': data[4],
        'Ph': ph_value,
        'Rainfall': rainfall_value
    }

    return jsonify(response)

def generate_random():
    ph_value = random.uniform(4.5, 8.0)
    rainfall_value = random.uniform(0.0, 200.0)
    ph_ans = round(ph_value, 2)
    rainfall_ans = round(rainfall_value, 2)
    return ph_ans, rainfall_ans

def load_model(modelfile):
	loaded_model = pickle.load(open(modelfile, 'rb'))
	return loaded_model


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        user_name = request.form['contact_name']
        user_email = request.form['contact_email']
        user_message = request.form['contact_message']
        
    
    return render_template('index.html')



# Define the prediction route
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        # Get input values from the form
        features = [float(request.form['Nitrogen_value']),
                    float(request.form['Phosphorus_value']),
                    float(request.form['Potassium_value']),
                    float(request.form['Temperature_value']),
                    float(request.form['Humidity_value']),
                    float(request.form['Ph_value']),
                    float(request.form['Rainfall_value'])]
        single_pred = np.array(features).reshape(1,-1)


        # Make a prediction using the loaded model
        loaded_model = load_model('model.pkl')
        prediction = loaded_model.predict(single_pred)
        print(prediction[0])

        random_value = gen_random()

        with app.app_context():
            new_value = Value(nitrogen=features[0], phosphorus=features[1], potassium=features[2],
                              temperature=features[3], humidity=features[4], ph=features[5],
                              rainfall=features[6], predicted_crop=prediction[0])
            db.session.add(new_value)
            db.session.commit()        

        image_urls = fetch_image_urls(prediction[0])
        image_url = image_urls[0]
        print(image_url)

        # Display the predicted crop on the result page
        return render_template('result.html', prediction=prediction[0], image_url=image_url, random_value=random_value)
    return render_template('form.html')

def gen_random():
    answer = round(random.uniform(1, 50))
    return answer


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
