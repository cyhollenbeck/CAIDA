# current chathelper.py

from nltk.chat.util import Chat
import re

class CustomChat(Chat):
    def __init__(self, pairs, reflections={}, db_helper=None):
        # Ensure pairs are raw patterns (strings)
        raw_pairs = [(pattern.pattern if isinstance(pattern, re.Pattern) else pattern, response) for pattern, response in pairs]
        super().__init__(raw_pairs, reflections)
        self.db_helper = db_helper

    def respond(self, user_input):
        # Check for variations of the question about the database
        db_question_patterns = [
            r".*\bwhat\b.*\bdatabase\b.*\busing\b.*",
            r".*\bwhat\b.*\bdb\b.*",
            r".*\bwhich\b.*\bdatabase\b.*",
            r".*\bwhich\b.*\bdb\b.*"
        ]
        
        for pattern in db_question_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                if self.db_helper:
                    return f"I am currently using the database: {self.db_helper.db_name}"
                else:
                    return "I am not connected to any database."

        for pattern, responses in self._pairs:
            if re.match(pattern, user_input):
                return responses[0]
        return None

    def reload_chat_pairs(self):
        if self.db_helper:
            new_pairs = self.db_helper.fetch_chat_pairs()
            self._pairs = [(pattern, response) for pattern, response in new_pairs]
        else:
            print("Database helper is not available.")

    def converse(self):
        while True:
            user_input = input("You: ")
            if user_input:
                if user_input.lower() == "quit":
                    print("Goodbye!")
                    break
                response = self.respond(user_input)
                print(f"Debug: Responded with {response}")  # Debug print
                if response:
                    print("Bot:", response)
                else:
                    print("I don't know how to respond to that. Can you teach me?")
                    print("What should I have said?")
                    user_response = input("Your response: ")
                    if user_response.strip() != "":
                        if self.db_helper:
                            self.db_helper.insert_chat_pair(user_input, user_response)
                            print("Thank you! I've learned something new.")
                            self.reload_chat_pairs()  # Reload and recompile chat pairs from the database   
                        else:
                            print("Database helper is not available.")
                    else:
                        print("No response provided. Let's try something else.")