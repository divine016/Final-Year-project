from flask import Flask, request, render_template, redirect, url_for
import joblib
import os

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# Load the trained model
phish_model_path = 'phishingrm.pkl'
if os.path.exists(phish_model_path):
    with open(phish_model_path, 'rb') as model_file:
        phish_model_ls = joblib.load(model_file)
else:
    raise FileNotFoundError(f"The model file {phish_model_path} does not exist")

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/learn')
def learn():
    return render_template('learn.html')
@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['urlInput']
    X_predict = []
    X_predict.append(str(url))
    y_Predict = phish_model_ls.predict(X_predict)
    redirect_to = None
    
    if y_Predict == 'bad':
        result = "Is a Phishing Site"
        result_class = "result-phishing"
        redirect_to = url_for('learn')
    else:
        result = "This is a Good Site"
        result_class = "result-legit"
    
    return render_template('index.html', url=url, redirect_to=redirect_to, result=result, result_class=result_class)

if __name__ == '__main__':
    app.run(debug=True)