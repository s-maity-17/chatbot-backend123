from flask import Flask, request, jsonify
from chat_bot import generate_data_store

app = Flask(__name__)

# REST: Home page
@app.route('/')
def home():
    return 'Welcome to Chant bot!!'

@app.post("/chat-bot")
def process_text():
    if request:
        input = request.get_json()
        question = input['question']
        
        if question is None:
            return jsonify({'error': 'Question parameters are required'})
        resp = generate_data_store(question)
        return jsonify({'answer': resp})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
