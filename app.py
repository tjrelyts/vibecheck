import hashlib
import hmac
import subprocess
from flask import Flask, render_template, request, jsonify
import os
import pickle

print ("Hello World")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY')

if SECRET_KEY is None:
    print("Error: SECRET_KEY is not set!")
    exit(1)

model_path = os.path.join(BASE_DIR, 'data/model.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'data/vectorizer.pkl')

app = Flask(__name__)

with open(model_path, 'rb') as f:
    model = pickle.load(f)

with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

def verify_signature(payload, signature):
    # 'sha1=' is prefixed to the signature sent by GitHub
    secret = SECRET_KEY.encode()
    hash_object = hmac.new(secret, payload, hashlib.sha1)
    expected_signature = 'sha1=' + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def analyze(str):
    if not str:
        print("DEBUG: None")
        return "none", "bg-dark"
    
    vec = vectorizer.transform([str])
    y_pred = model.predict(vec)

    if y_pred[0] == 2:
        print("DEBUG: Negative")
        return "negative", "bg-danger"
    elif y_pred[0] == 1:
        print("DEBUG: Positive")
        return "positive", "bg-success"
    else:
        print("DEBUG: Neutral")
        return "neutral", "bg-dark"
    
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    msg = request.json.get('msg')
    sentiment, body_color = analyze(msg)
    return jsonify({'sentiment': sentiment, 'body_color': body_color})

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('base.html')

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.get_data()  # Raw payload data
    signature = request.headers.get('X-Hub-Signature')

    # Verify the signature
    if not verify_signature(data, signature):
        return jsonify({"message": "Invalid signature"}), 400

    # Continue with the deployment process if the signature is valid
    payload = request.get_json()

    if payload['ref'] == 'refs/heads/main':
        print("Deploying latest changes from the repository...")
        
        subprocess.call(['git', 'pull', 'origin', 'main'], cwd=BASE_DIR)
        subprocess.call(['pip', 'install', '-r', os.path.join(BASE_DIR, 'requirements.txt')])
        subprocess.call(['touch', os.path.join(BASE_DIR, 'yourproject.wsgi')])

        return jsonify({"message": "Deployment triggered!"}), 200
    else:
        return jsonify({"message": "Not from the 'main' branch."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)