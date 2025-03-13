import sqlite3 # 2 simple DBs made for this project, library & users
import re # regex for checking that inputs are done correctly
from getpass import getpass # hidden password input when user enters password
# Potentially add AES encryption? Make class on its own?

def setup_databases():
    # User DB - User details for signup/login
    connect_users = sqlite3.connect('users.db')
    conn_users = connect_users.cursor()
    conn_users.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT, dob DATE, phone_num TEXT, email_address TEXT NOT NULL, password TEXT NOT NULL, user_type TEXT)")
    connect_users.commit()
    connect_users.close()

    # Library DB - Actual library holding book info, item_id acts as accession number(?)
    connect_library = sqlite3.connect('library.db')
    conn_library = connect_library.cursor()
    conn_library.execute("CREATE TABLE IF NOT EXISTS books(item_id INT PRIMARY KEY, ISBN TEXT, title TEXT, author DATE, publisher TEXT, publication_date INT, edition TEXT, language TEXT, genre TEXT, available INTEGER DEFAULT 1)") # DB table for library items/books
    conn_library.execute("CREATE TABLE IF NOT EXISTS requests(request_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, item_id INT, request_type TEXT, status TEXT)") # DB table for requests = reservations, borrowed books
    connect_library.commit()
    connect_library.close()

setup_databases() # Creates DBs & tables

# User class - parent class for member/librarian/admin
class User: 
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password, user_type):
        self.user_id = user_id
        self.fullname = fullname
        self.dob = dob
        self.phone_num = phone_num
        self.email_address = email_address
        self.__password = password # PRIVATE ATTRIBUTE
        self.user_type = user_type
    
    @classmethod # Class method so it can be called without instatiating object of class (bound to class instead of object)
    def signup(cls): # ADD TRY EXCEPTS HERE FOR USER LOGIN DETAILS MEETING CONSTRAINTS
        conn_signupuser = sqlite3.connect('users.db') # to insert the details into the user table
        curs_signup_user = conn_signupuser.cursor()

        correct_signup = False # While loop, will become True when details are correctly put in
        while correct_signup == False:
            ## ENTERING ACCOUNT TYPE ##
            try: # Catch error when invalid choice for user account type not entered properly
                print("\n-    Signup Menu    -\n\nPlease enter the corresponding number for what type of user you are:\n1. Member \n2. Librarian \n3. Admin\n4. Exit signup menu\n")
                signup_choice = int(input("Enter choice: "))
                if signup_choice not in [1, 2, 3, 4]:
                    raise ValueError("Invalid choice. Please enter a valid option.")
                elif signup_choice == 1:
                    signup_choice = "Member" 
                elif signup_choice == 2: # Key so that only certified librarians can signup accounts, only done to show difference between member account & librarian/admin
                    key_lib = input("Enter librarian key: ")
                    if key_lib != "CertifiedLibrarianKey":
                        print("Invalid librarian key. Please enter the certified key.")
                    else:
                        signup_choice = "Librarian"
                elif signup_choice == 3: # Key so that only certified admins can signup accounts, only done to show difference between member account & librarian/admin
                    key_admin = input("Enter admin key: ")
                    if key_admin != "AdministratorsKey":
                        print("Invalid librarian key. Please enter the certified key.")
                    else:
                        signup_choice = "Admin"
                else:
                    break   
            except ValueError as e: # Anything that isnt an integer and invalid numbers raise error here
                print(f"Error: {e}")
                print("Invalid choice. Please enter a valid number and corresponding choice.")

            ## ENTERING ACCOUNT DETAILS ## # Kept getting UnboundLocalError: cannot access local variable 'users_phonenum' where it is not associated with a value if all detail inputs are not in separate loops
            while True: # FullName
                users_name = input("\nEnter full name: ")
                if any(char.isdigit() for char in users_name): # Checking for no numbers in name for valid entry
                    print("Invalid name. Please enter a valid name without numbers.")
                else:
                    break
            while True: # DOB
                users_dob = input("Please enter your date of birth in the format 'YYYY-MM-DD': ") 
                if not re.search(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$', users_dob): # Checks if date format is input correctly, raw strings used so that \ won't be used for escape, regex taken from: https://stackoverflow.com/questions/22061723/regex-date-validation-for-yyyy-mm-dd
                    print("Date of birth invalid. Please enter a valid date.")
                else:
                    break
            # PhoneNumber
            users_phonenum = input("Enter phone number: ") # Enter regex here? But layout is confusing
            while True:
                users_email = input("Enter email address: ")
                if not re.search(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$', users_email): # Checks if email address is formatted correctly, regex taken from: https://regexr.com/3e48o
                    print("Email address invalid. Please enter a valid email address.")
                else:
                    break
            users_password = getpass("Enter password: ")
            correct_signup = True
            
            ## PUTTING DETAILS INTO DATABASE TABLE: USERS ##
            try: # Checking for error that might be raised if email address is already used for another user's details
                curs_signup_user.execute("INSERT INTO users (fullname, dob, phone_num, email_address, password, user_type) VALUES (?, ?, ?, ?, ?, ?)", (users_name, users_dob, users_phonenum, users_email, users_password, signup_choice))
                conn_signupuser.commit()
                conn_signupuser.close()
                print("Signup successful! You can now login.") # ADD SMTH HERE LIKE 'Press any key to go back to login menu'(?)
                correct_signup = True 
            except sqlite3.IntegrityError:
                print("Error: Email already exists. Try again.")

    @classmethod # Class method so it can be called without instatiating object of class (bound to class instead of object)
    def login(cls):
        while True: # Loop to keep asking for valid credentials
            try:
                emailaddress = input("\nEnter your email address: ")
                password = getpass("Enter your password: ")

                if not re.search(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$', emailaddress): # Checks if email address is formatted correctly, regex taken from: https://regexr.com/3e48o
                    raise ValueError("Email address invalid. Please enter a valid email address.")
                
                conn_loginuser = sqlite3.connect('users.db')
                conn_loginuser.row_factory = sqlite3.Row # Changes the way details are accessed so that its treated similar to a dictionary instead by using keys (was a tuple if called normally, harder to read b/c of multiple columns)
                curs_login_user = conn_loginuser.cursor()
                curs_login_user.execute

                # Check database for the user's matching details
                curs_login_user.execute("SELECT * FROM users WHERE email_address = ? AND password = ?", (emailaddress, password))
                user_details = curs_login_user.fetchone()
                conn_loginuser.close()

                if user_details: # IF user_details are returned
                    # Access values using keys - similar to dictionary, uses names of columns (better for readability)
                    user_id = user_details['user_id']
                    fullname = user_details['fullname']
                    dob = user_details['dob']
                    phone_num = user_details['phone_num']
                    email_address = user_details['email_address']
                    password = user_details['password']
                    user_type = user_details['user_type']

                    if user_type == "Member": # Create user objects with the relevant login details before opening menu depending on account type
                        member_user = Member(user_id, fullname, dob, phone_num, email_address, password)
                        member_user.member_menu()
                    elif user_type == "Librarian":
                        librarian_user = Librarian(user_id, fullname, dob, phone_num, email_address, password)
                        librarian_user.librarian_menu()
                    elif user_type == "Admin":
                        admin_user = Admin(user_id, fullname, dob, phone_num, email_address, password)
                        admin_user.admin_menu()
                    break # Break out of loop when menu opens

                else:
                    print("Invalid login credentials, please try again.")
            
            except ValueError as e:
                # Invalid email format
                print(f"Error: {e}") # f string - string interpolation - to make it easier to read
            except Exception as e:
                # Unexpected errors caught here just in case
                print(f"An unexpected error occurred: {e}")

class Member(User):
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password):
        super().__init__(user_id, fullname, dob, phone_num, email_address, password, "Member")
        self.borrowed_books = []  # List of borrowed books to be viewed in view_details
        self.__reserved_books = []  # Private list of reserved books

    ## Parts of menu implemented HERE - members being able to search, borrow or return books and view their details ##
    def view_profile(self):
        print(f"\nMember ID: {self.user_id}\nName: {self.fullname}\nEmail: {self.email_address}\nBorrowed Books: {self.borrowed_books}\nReserved Books: {self.__reserved_books}")
    
    def search_books(self):
        while True: # Loop until user types 0 to go back
            print("""\n-    Search Books    -\n
                  Enter a title or author to search for books.
                  Type '0' to go back to the menu.\n""")
            
            user_search = input("Enter search term: ")
            if user_search == "0":
                print("Returning to menu...")
                break

            conn_library = sqlite3.connect('library.db')
            conn_library.row_factory = sqlite3.Row # Same as before usage, easier to access instead of remembering column nums.
            cursor = conn_library.cursor()

            try:
                cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f'%{user_search}%', f'%{user_search}%')) # f string: search DB table for any terms that match to title or author
                books = cursor.fetchall()
                if books: # if anything returned from DB table
                    print("\nSearch results:")
                    for item in books:
                        print(f"ISBN: {item['ISBN']}, Title: {item['title']}, Author: {item['author']}, Publisher: {item['publisher']}, Genre: {item['genre']}, Available: {'Yes' if item['available'] else 'No'}")
                else:
                    print("No books found matching your search.\n")
            except sqlite3.Error as e:
                print(f"Database error: {e}") # Database error: something wrong with columns or actual data itself
            except Exception as e:
                print(f"An unexpected error occurred: {e}") # Unexpected error: something random gone wrong? Precaution taken
            finally:
                conn_library.close() # close connection to DB when done
            
    def borrow_book(self):
        while True: # Loop to repeatedly ask for isbn unless they choose to go back to menu
            print("""\n-    Borrow a Book    -
                  Enter the ISBN of the book you want to borrow.
                  Type '0' to go back to the menu.\n""")
            isbn = input("Enter ISBN: ")
            if isbn == "0":
                print("Returning to the menu...")
                break

            conn_library =  sqlite3.connect('library.db')
            conn_library.row_factory = sqlite3.Row
            cursor = conn_library.cursor()

            try:
                # Show full details of book just in case it is the right one
                cursor.execute("SELECT * FROM books WHERE ISBN = ?", (isbn,))
                book = cursor.fetchone()

                if book: # if book returned, print whole details
                    print(f"\nBook Details:\nISBN: {book['ISBN']},\nTitle: {book['title']},\nAuthor: {book['author']},\nPublisher: {book['publisher']},\nPublication Date: {book['publication_date']},\nEdition: {book['edition']},\nLanguage: {book['language']},\nGenre: {book['genre']},\nAvailable: {'Yes' if book['available'] else 'No'}")
                    
                    # Prompt confirmation and check with user if its right book
                    confirm = input("\nDo you want to borrow this book? (Type 'yes' or '1' to confirm, or any other key to cancel): ").strip().lower()
                    if confirm in ['yes', '1']:  # takes input yes or 1 as agreement
                        if book['available']:  # Check if book is available
                            if len(self.borrowed_books) < 5:  # Check if member has borrowed less than 5 books SEE BRIEF CONSTRAINTS
                                # Update book status to unavailable
                                cursor.execute("UPDATE books SET available = 0 WHERE ISBN = ?", (isbn,))
                                
                                # Add  borrowed book to requests table AND link to user id = current user logged in
                                cursor.execute("""
                                    INSERT INTO requests (user_id, item_id, request_type, status)
                                    VALUES (?, ?, ?, ?)
                                """, (self.user_id, book['item_id'], "Borrow", "Borrowed"))
                                
                                # Add ISBN to member's borrowed list
                                self.borrowed_books.append(isbn)
                                conn_library.commit()
                                print(f"Book with ISBN {isbn} borrowed successfully.")
                            else:
                                print("You have reached the maximum limit of 5 borrowed books.")
                        else:
                            print("Book is not available for borrowing.")
                    else:
                        print("Borrowing cancelled. Please enter the ISBN again or enter another ISBN.")
                else:
                    print("Book with this ISBN does not exist.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                conn_library.close()


    def member_menu(self):
        while True:
            print("""\n-  Library Menu    -
                  
                  1. View Profile
                  2. Search for Books
                  3. Borrow a Book
                  4. Return a Book
                  5. Reserve a Book
                  6. Logout\n""")
            choice = input("Enter choice: ").strip()
            if choice == "1":  # View Profile
                self.view_profile()
            elif choice == "2":  # Search for Books
                self.search_books()
            elif choice == "3":  # Borrow a Book
                self.borrow_book()
            # elif choice == "4":  # Return a Book
            #     self.return_book()
            # elif choice == "5":  # Reserve a Book
            #     self.reserve_book()
            elif choice == "6":  # Logout
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

class Librarian(User):
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password):
        super().__init__(user_id, fullname, dob, phone_num, email_address, password, "Librarian")

    def view_profile(self):
        print(f"Librarian ID: {self.user_id}\nName: {self.fullname}\nEmail: {self.email_address}")

    ### TO BE IMPLEMENTED, WORK WITH THE LIBRARIAN MENU ###
    # def add_book(self):
    
    # def update_book(self):
    
    # def remove_book(self):
    
    # def generate_report(self):

    def librarian_menu(self):
        while True:
            print("""-  Library Menu    -
                  
                  1. View Profile
                  2. Add an Item to the Library
                  3. Update an item from the Library
                  4. Remove an item from the Library
                  5. Reserve from the Library
                  6. Logout and Exit\n""")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.view_profile()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

class Admin(User):
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password):
        super().__init__(user_id, fullname, dob, phone_num, email_address, password, "Admin")

    def admin_menu(self):
        while True:
            print("""-  Admin Menu    -
                  
                  1. View Profile
                  2. Manage Users
                  3. Generate Reports
                  4. Logout and Exit\n""")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.view_profile()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

## SLMS STARTING MENU ##
print("""\n-  Library Management System   -
      
    Please type the corresponding choice for what you would like to do:
    1. Signup
    2. Login
    3. Exit
    """)
# User signup/login
choice = input("Enter choice: ")
if choice == "1":
    User.signup()
elif choice == "2":
    User.login()
elif choice == "3":
    print("Exiting system...")
else:
    print("Invalid input. Please enter a valid choice.")