from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    # Call the classifier
    with open(path, 'rb') as f:
        res = requests.post('http://localhost:5001/classify', files={'file': f})
    
    if res.status_code == 200:
        return jsonify(res.json())
    else:
        return jsonify({'error': 'Classifier error'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
