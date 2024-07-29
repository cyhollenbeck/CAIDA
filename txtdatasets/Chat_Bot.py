import nltk
from nltk.tokenize import word_tokenize
import json

# Ensure 'punkt' resource is downloaded
nltk.download('punkt')

class ChatBot:
    def __init__(self, knowledge_base_file='knowledge_base.json'):
        self.knowledge_base_file = knowledge_base_file
        try:
            with open(self.knowledge_base_file, 'r') as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            self.knowledge_base = {}

    def learn_and_respond(self, user_input):
        response = self.find_response(user_input)
        if response is None:
            response = input(f"I don't have a response. Please teach me a response for '{user_input}': ")
            self.teach_response(user_input, response)

        # Save the updated knowledge base to JSON file
        self.save_knowledge_base()

        return response

    def find_response(self, user_input):
        for question in self.knowledge_base.get('questions', []):
            if question['question'].lower() == user_input.lower():
                return question['response']
        return None

    def teach_response(self, user_input, response):
        new_question = {'question': user_input.lower(), 'response': response}
        if 'questions' not in self.knowledge_base:
            self.knowledge_base['questions'] = []
        self.knowledge_base['questions'].append(new_question)

    def save_knowledge_base(self):
        with open(self.knowledge_base_file, 'w') as f:
            json.dump(self.knowledge_base, f, indent=4)  # Indent for pretty formatting

    def chat(self):
        print("Welcome! Let's chat. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                self.save_knowledge_base()
                print("Exiting...")
                break
            else:
                response = self.learn_and_respond(user_input)
                print(f"Bot: {response}")

if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.chat()
