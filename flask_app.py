from flask import Flask, render_template, request, jsonify
import os
import pickle

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
    if request.method != 'POST':
        return 'OK'
    else:
        abort_code = 418
        # Do initial validations on required headers
        if 'X-Github-Event' not in request.headers:
            abort(abort_code)
        if 'X-Github-Delivery' not in request.headers:
            abort(abort_code)
        if 'X-Hub-Signature' not in request.headers:
            abort(abort_code)
        if not request.is_json:
            abort(abort_code)
        if 'User-Agent' not in request.headers:
            abort(abort_code)
        ua = request.headers.get('User-Agent')
        if not ua.startswith('GitHub-Hookshot/'):
            abort(abort_code)

        event = request.headers.get('X-GitHub-Event')
        if event == "ping":
            return json.dumps({'msg': 'Hi!'})
        if event != "push":
            return json.dumps({'msg': "Wrong event type"})

        x_hub_signature = request.headers.get('X-Hub-Signature')
        # webhook content type should be application/json for request.data to have the payload
        # request.data is empty in case of x-www-form-urlencoded
        if not is_valid_signature(x_hub_signature, request.data, w_secret):
            print('Deploy signature failed: {sig}'.format(sig=x_hub_signature))
            abort(abort_code)

        payload = request.get_json()
        if payload is None:
            print('Deploy payload is empty: {payload}'.format(
                payload=payload))
            abort(abort_code)

        if payload['ref'] != 'refs/heads/master':
            return json.dumps({'msg': 'Not master; ignoring'})

        repo = git.Repo('/var/www/sites/mysite')
        origin = repo.remotes.origin

        pull_info = origin.pull()

        if len(pull_info) == 0:
            return json.dumps({'msg': "Didn't pull any information from remote!"})
        if pull_info[0].flags > 128:
            return json.dumps({'msg': "Didn't pull any information from remote!"})

        commit_hash = pull_info[0].commit.hexsha
        build_commit = f'build_commit = "{commit_hash}"'
        print(f'{build_commit}')
        return 'Updated PythonAnywhere server to commit {commit}'.format(commit=commit_hash)


if __name__ == '__main__':
    app.run(debug=True, port=8000)