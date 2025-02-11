from flask import Flask, render_template, request, jsonify
import os
import pickle

app = Flask(__name__)

with open(os.path.abspath('./data/model.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.abspath('./data/vectorizer.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)