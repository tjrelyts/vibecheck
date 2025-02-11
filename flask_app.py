from flask import Flask, render_template, request, jsonify
import os
import pickle
#test
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, 'data/model.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'data/vectorizer.pkl')

app = Flask(__name__)

with open(model_path, 'rb') as f:
    model = pickle.load(f)

with open(vectorizer_path, 'rb') as f:
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

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('path/to/git_repo')
        origin = repo.remotes.origin
    origin.pull()

if __name__ == '__main__':
    app.run(debug=True, port=8000)