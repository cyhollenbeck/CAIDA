import os
from flask import Flask, request, jsonify, render_template
from chathelper import CustomChat
from helpermain import main  # Import the main function from helpermain.py

basedir = os.path.abspath(os.path.dirname(__file__))

# Construct the PostgreSQL connection string from environment variables
db_name = os.getenv('DB_NAME', 'caida')
db_user = os.getenv('DB_USER', 'caida')
db_password = os.getenv('DB_PASSWORD', 'Sn@rPHM3AndYou!!')
db_host = os.getenv('DB_HOST', 'caida-postgre-flex.postgres.database.azure.com')
db_port = os.getenv('DB_PORT', '5432')

database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

class Config:
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database helper using the main function from helpermain.py
db_helper = None

def initialize_db_helper():
    global db_helper
    try:
        if db_helper is None:
            db_helper = main()
    except Exception as e:
        app.logger.error(f"Error initializing db_helper: {e}")

initialize_db_helper()

try:
    chat_pairs = db_helper.fetch_chat_pairs()
    chatbot = CustomChat(chat_pairs, reflections={}, db_helper=db_helper)
except Exception as e:
    app.logger.error(f"Error initializing chatbot: {e}")

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_input = request.form['message']
        response = chatbot.respond(user_input)
        return jsonify({'response': response})
    except Exception as e:
        app.logger.error(f"Error in /ask route: {e}")
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)