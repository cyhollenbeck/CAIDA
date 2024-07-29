
#current dbhelper.py

import sqlite3
import os
import json

class DBHelper:
    config_file = 'config.json'

    def __init__(self, db_name=None):
        print(f"Initializing DBHelper with db_name: {db_name}")
        if db_name is None:
            db_name = self.select_database()
        self.set_selected_db_name(db_name)
        self.db_name = db_name
        print(f"Selected database: {self.db_name}")
        self.create_db_and_table()

    def create_db_and_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS chat_pairs
                     (id INTEGER PRIMARY KEY, pattern TEXT, response TEXT)''')
        conn.commit()
        conn.close()

    def insert_chat_pair(self, pattern, response):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO chat_pairs (pattern, response) VALUES (?, ?)", (pattern, response))
        conn.commit()
        conn.close()

    def fetch_chat_pairs(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT pattern, response FROM chat_pairs")
        chat_pairs = c.fetchall()
        conn.close()
        return [[pair[0], [pair[1]]] for pair in chat_pairs]

    def list_db_files(self, directory):
        return [f for f in os.listdir(directory) if f.endswith('.db')]

    def select_database(self):
        directory = './datasets'
        db_files = self.list_db_files(directory)
        
        if not db_files:
            print("No .db files found in the /datasets directory.")
            create_new = input("Would you like to create a new database? (yes/no): ").strip().lower()
            if create_new == 'yes':
                db_name = input("Enter the name for the new database (without extension): ").strip() + '.db'
                return os.path.join(directory, db_name)
            else:
                print("No database selected. Exiting.")
                exit()
        
        print("Available databases:")
        for idx, db_file in enumerate(db_files, start=1):
            print(f"{idx}. {db_file}")
        print(f"{len(db_files) + 1}. Exit")
        
        while True:
            choice = input("Select a database by number, type 'new' to create a new one, or 'exit' to exit: ").strip().lower()
            
            if choice == 'new':
                db_name = input("Enter the name for the new database (without extension): ").strip() + '.db'
                return os.path.join(directory, db_name)
            elif choice == 'exit' or choice == str(len(db_files) + 1):
                print("Exiting.")
                exit()
            else:
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(db_files):
                        return os.path.join(directory, db_files[choice_idx])
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number, 'new', or 'exit'.")

    def get_selected_db_name(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            return config.get('selected_db_name')
        return None

    def set_selected_db_name(self, db_name):
        with open(self.config_file, 'w') as f:
            json.dump({'selected_db_name': db_name}, f)

    def list_txt_files(self, directory):
        return [f for f in os.listdir(directory) if f.endswith('.txt')]

    def select_text_file(self):
        directory = './txtdatasets'
        txt_files = self.list_txt_files(directory)
        
        if not txt_files:
            print("No .txt files found in the /txtdatasets directory.")
            manual_path = input("Enter the path to a text file: ").strip()
            return manual_path
        
        print("Available text files:")
        for idx, txt_file in enumerate(txt_files, start=1):
            print(f"{idx}. {txt_file}")
        print(f"{len(txt_files) + 1}. Exit")
        
        while True:
            choice = input("Select a text file by number, type 'manual' to enter a manual path, or 'exit' to exit: ").strip().lower()
            
            if choice == 'manual':
                manual_path = input("Enter the path to a text file: ").strip()
                return manual_path
            elif choice == 'exit' or choice == str(len(txt_files) + 1):
                print("Exiting.")
                exit()
            else:
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(txt_files):
                        return os.path.join(directory, txt_files[choice_idx])
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number, 'manual', or 'exit'.")

    def import_text_file(self):
        text_file_path = self.select_text_file()
        print(f"Importing from text file: {text_file_path}")
        
        with open(text_file_path, 'r') as file:
            lines = file.readlines()
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        for line in lines:
            pattern, response = line.strip().split('\t')
            c.execute("INSERT INTO chat_pairs (pattern, response) VALUES (?, ?)", (pattern, response))
        
        conn.commit()
        conn.close()
        print("Import completed.")