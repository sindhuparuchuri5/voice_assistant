# server.py
from flask import Flask, render_template, request, jsonify
from assistant import ask_question

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    required = request.form.get('required', True)
    is_last_question = request.form.get('is_last_question', False)

    response = ask_question(question, required, is_last_question)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
