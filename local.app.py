# current local.app.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'your_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

from flask import Flask, request, jsonify, render_template
from chathelper import CustomChat
from helpermain import main  # Import the main function from helpermain.py

app = Flask(__name__)

# Initialize the database helper using the main function from helpermain.py
db_helper = None

def initialize_db_helper():
    global db_helper
    if db_helper is None:
        db_helper = main()

initialize_db_helper()
chat_pairs = db_helper.fetch_chat_pairs()
chatbot = CustomChat(chat_pairs, reflections={}, db_helper=db_helper)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['messageText']
    response = chatbot.respond(user_input)
    if response:
        return jsonify({'answer': response})
    else:
        return jsonify({'answer': "Sorry, I don't know how to respond to that. Can you teach me?", 'learn': True})

@app.route('/teach', methods=['POST'])
def teach():
    pattern = request.form['pattern']
    response = request.form['response']
    db_helper.insert_chat_pair(pattern, response)
    chatbot.reload_chat_pairs()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Disable auto-reload