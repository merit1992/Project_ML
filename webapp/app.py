from flask import Flask, render_template, request
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Load the model
model = joblib.load('model.joblib')
vectorizer = model['vectorizer']
classifiers = {'Naive Bayes': model['nb_classifier'], 'Ensemble Model': model['ensemble_classifier']}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        form_data = {
            'Username': request.form['username'],
            'First Name': request.form['first_name'],
            'Last Name': request.form['last_name'],
            'Email': request.form['email'],
            'House Address': request.form['house_address'],
        }

        # Initialize an empty list to store results for each field
        results = []

        # Iterate over form fields
        for field, value in form_data.items():
            # Create a text string for the vectorizer
            text = value

            # Transform text using vectorizer
            vector = vectorizer.transform([text])

            # Predict using the selected classifier
            prediction = classifiers[request.form['classifier']].predict(vector)[0]

            # Check for SQL injection
            if prediction == 1:
                results.append(f"SQL Injection Detected in {field}: \n\n {value}")
            else:
                results.append(f"No SQL Injection Detected in {field}")
    
    
        return render_template('index.html', results=results, classifiers=classifiers)
    # print(classifiers)
    return render_template('index.html', classifiers=classifiers)

if __name__ == '__main__':
    app.run(debug=True)
