from flask import Flask, render_template, request
import pickle
import numpy as np
import requests

api_key = "AIzaSyBh8NUavqlu9qadl7FjgP2Y1rMDpI0pJ8I"
cx = "c5bc3c5d3db9e4084"


app = Flask(__name__,
            static_folder="templates/assets")

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

        image_urls = fetch_image_urls(prediction[0])
        image_url = image_urls[0]
        print(image_url)

        # Display the predicted crop on the result page
        return render_template('result.html', prediction=prediction[0], image_url=image_url)
    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
