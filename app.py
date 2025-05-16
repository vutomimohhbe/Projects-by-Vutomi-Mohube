from flask import Flask, request, render_template, redirect, url_for, session
import joblib
import numpy as np
import re
from collections import Counter
import math

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Load the model and vectorizer
svm_model = joblib.load('svm_phishing_model.joblib')
vectorizer = joblib.load('tfidf_vectorizer.joblib')

# Function to detect gibberish
def is_gibberish(text, threshold=0.9):
    letters = re.sub(r'[^a-zA-Z]', '', text.lower())
    if not letters:
        return True
    length = len(letters)
    freq = Counter(letters)
    entropy = -sum((count/length) * math.log2(count/length) for count in freq.values())
    return entropy > 6 or len(set(letters)) / len(letters) > threshold

@app.route('/', methods=['GET', 'POST'])
def declaration():
    if request.method == 'POST':
        if request.form.get('agree'):
            session['agreed_to_declaration'] = True
            return redirect(url_for('index'))
        else:
            return render_template('declaration.html', error="You must agree to the declaration to proceed.")
    return render_template('declaration.html')

@app.route('/form', methods=['GET', 'POST'])
def index():
    if not session.get('agreed_to_declaration'):
        return redirect(url_for('declaration'))

    result = None
    decision_rule = None

    if request.method == 'POST':
        email_text = request.form.get('email_text')
        if 'email_file' in request.files and request.files['email_file'].filename != '':
            email_file = request.files['email_file']
            email_text = email_file.read().decode('utf-8', errors='ignore')

        if email_text:
            if is_gibberish(email_text):
                result = "Input appears to be gibberish. Please provide a meaningful email text."
            else:
                email_tfidf = vectorizer.transform([email_text])
                prediction = svm_model.predict(email_tfidf)[0]
                decision_score = svm_model.decision_function(email_tfidf)[0]

                # Calibrate confidence score to boost clear cases
                # Scale decision score to map to a more intuitive range (e.g., >80% for clear cases)
                confidence = 1 / (1 + np.exp(-decision_score * 2))  # Multiply decision score by 2 to sharpen confidence
                confidence = max(50, min(95, confidence * 100))  # Ensure confidence is between 50% and 95%

                label = "Phishing" if prediction == 1 else "Legitimate"
                result = f"This email is {label} (Confidence: {confidence:.2f}%)"

                feature_names = vectorizer.get_feature_names_out()
                coef = svm_model.coef_[0]
                tfidf_scores = email_tfidf.toarray()[0]
                contributions = coef * tfidf_scores
                top_positive_indices = np.argsort(contributions)[-5:][::-1]
                top_negative_indices = np.argsort(contributions)[:5]

                phishing_indicators = [(feature_names[i], contributions[i]) for i in top_positive_indices if tfidf_scores[i] > 0]
                legitimate_indicators = [(feature_names[i], contributions[i]) for i in top_negative_indices if tfidf_scores[i] > 0]

                if not phishing_indicators and not legitimate_indicators:
                    top_phishing_words = [(feature_names[i], coef[i]) for i in np.argsort(coef)[-5:][::-1]]
                    top_legitimate_words = [(feature_names[i], coef[i]) for i in np.argsort(coef)[:5]]
                    message = "No recognizable words matched our analysis. Decision based on general patterns."
                    decision_rule = {
                        "message": message,
                        "phishing_indicators": top_phishing_words,
                        "legitimate_indicators": top_legitimate_words,
                        "general_rule": True
                    }
                else:
                    explanation = f"Classified as {label.lower()} due to stronger {label.lower()} indicators."
                    decision_rule = {
                        "explanation": explanation,
                        "phishing_indicators": phishing_indicators,
                        "legitimate_indicators": legitimate_indicators,
                        "general_rule": False
                    }

    return render_template('index.html', result=result, decision_rule=decision_rule)

if __name__ == '__main__':
    app.run(debug=True)