import psycopg2
import os
import json

class DBHelper:
    config_file = 'config.json'

    def __init__(self, db_name=None):
        print(f"Initializing DBHelper with db_name: {db_name}")
        if db_name is None:
            db_name = self.get_selected_db_name()
        self.set_selected_db_name(db_name)
        self.db_name = db_name
        print(f"Selected database: {self.db_name}")
        self.create_db_and_table()

    def create_db_and_table(self):
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS chat_pairs
                         (id SERIAL PRIMARY KEY, pattern TEXT, response TEXT)''')
            conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

    def insert_chat_pair(self, pattern, response):
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("INSERT INTO chat_pairs (pattern, response) VALUES (%s, %s)", (pattern, response))
            conn.commit()
        except Exception as e:
            print(f"Error inserting chat pair: {e}")
        finally:
            conn.close()

    def fetch_chat_pairs(self):
        try:
            conn = self.connect()
            c = conn.cursor()
            c.execute("SELECT pattern, response FROM chat_pairs")
            chat_pairs = c.fetchall()
            return [[pair[0], [pair[1]]] for pair in chat_pairs]
        except Exception as e:
            print(f"Error fetching chat pairs: {e}")
            return []
        finally:
            conn.close()

    def connect(self):
        try:
            return psycopg2.connect(
                dbname=self.db_name,
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def get_selected_db_name(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            return config.get('selected_db_name', os.getenv('DB_NAME'))
        return os.getenv('DB_NAME')

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
        
        try:
            conn = self.connect()
            c = conn.cursor()
            
            for line in lines:
                pattern, response = line.strip().split('\t')
                c.execute("INSERT INTO chat_pairs (pattern, response) VALUES (%s, %s)", (pattern, response))
            
            conn.commit()
            print("Import completed.")
        except Exception as e:
            print(f"Error importing text file: {e}")
        finally:
            conn.close()