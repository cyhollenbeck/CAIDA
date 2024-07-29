# current helpermain.py

from dbhelper import DBHelper

db_helper_instance = None

def main():
    global db_helper_instance
    if db_helper_instance is None:
        print("Choose an option:")
        print("1. Select a database with no import")
        print("2. Select a database and perform an import")
        print("3. Exit")
        
        while True:
            choice = input("Enter 1, 2, or 3: ").strip()
            if choice == '1':
                db_helper_instance = DBHelper()  # This will prompt for the database selection
                return db_helper_instance
            elif choice == '2':
                db_helper_instance = DBHelper()  # This will prompt for the database selection
                db_helper_instance.import_text_file()
                return db_helper_instance
            elif choice == '3':
                print("Exiting the application.")
                exit(0)
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    return db_helper_instance

if __name__ == "__main__":
    db_helper = main()