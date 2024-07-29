import os
os.system('cls' if os.name == 'nt' else 'clear')

from helper import DBHelper, CustomChat  # Import DBHelper and CustomChat classes

def chat():
    db_helper = DBHelper()  # No need to pass db_path, uses default 'chatpairs.db'
    chat_pairs = db_helper.fetch_chat_pairs()  # Use the fetch_chat_pairs method from the instance
    print("Hi! I'm Caida. How can I help you?")
    chatbot = CustomChat(chat_pairs, reflections={}, db_helper=db_helper)  # Use CustomChat with db_helper
    chatbot.converse()
    
if __name__ == "__main__":
    chat()