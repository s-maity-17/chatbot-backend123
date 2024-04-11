from flask import Flask, request, jsonify
from chat_bot import generate_data_store
from flask_cors import CORS
from datetime import datetime
app = Flask(__name__)
CORS(app)

# REST: Home page
@app.route('/')
def home():
    return 'Welcome to Chat bot!!'

@app.post("/chat-bot")
def process_text():
    if request:
        input = request.get_json()
        question = input['question']
        
        if question is None:
            return jsonify({'error': 'Question parameters are required'})
        resp = generate_data_store(question)
        current_time = datetime.now()
        return jsonify({'answer': resp, 'delivered_at': current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
