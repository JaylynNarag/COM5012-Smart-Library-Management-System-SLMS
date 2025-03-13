### PSEUDOCODE ###
# FUNCTION setup_databases
#     CONNECT to 'users.db'
#     CREATE TABLE users IF NOT EXISTS
#     COMMIT and CLOSE connection

#     CONNECT to 'library.db'
#     CREATE TABLE books IF NOT EXISTS
#     CREATE TABLE requests IF NOT EXISTS
#     COMMIT and CLOSE connection
# END FUNCTION

# User Class

# CLASS User
#     FUNCTION __init__(user_id, fullname, dob, phone_num, email_address, password, user_type)
#         SET user attributes
#     END FUNCTION

#     FUNCTION signup
#         CONNECT to 'users.db'
#         WHILE correct_signup is False
#             TRY
#                 PROMPT user for account type
#                 IF invalid choice THEN raise ValueError
#                 SET signup_choice based on input
#             CATCH ValueError
#                 PRINT error message
#             END TRY

#             PROMPT user for account details (name, dob, phone number, email, password)
#             VALIDATE inputs
#             IF valid THEN correct_signup = True
#         END WHILE

#         TRY
#             INSERT user details into users table
#             COMMIT and CLOSE connection
#             PRINT signup successful
#         CATCH IntegrityError
#             PRINT email already exists
#         END TRY
#     END FUNCTION
# END CLASS

# Member Class

# CLASS Member EXTENDS User
#     FUNCTION __init__(user_id, fullname, dob, phone_num, email_address, password)
#         CALL super().__init__
#         SET borrowed_books and reserved_books
#     END FUNCTION

#     FUNCTION fetch_borrowed_books
#         CONNECT to 'library.db'
#         FETCH borrowed books for the member
#         RETURN borrowed_books list
#     END FUNCTION

#     FUNCTION fetch_reserved_books
#         CONNECT to 'library.db'
#         FETCH reserved books for the member
#         RETURN reserved_books list
#     END FUNCTION

#     FUNCTION view_profile
#         PRINT member details
#         PRINT borrowed books
#         PRINT reserved books
#     END FUNCTION
# END CLASS

# Librarian Class

# CLASS Librarian EXTENDS User
#     FUNCTION __init__(user_id, fullname, dob, phone_num, email_address, password)
#         CALL super().__init__
#     END FUNCTION

#     FUNCTION view_profile
#         PRINT librarian details
#     END FUNCTION
# END CLASS

# Admin Class

# CLASS Admin EXTENDS User
#     FUNCTION __init__(user_id, fullname, dob, phone_num, email_address, password)
#         CALL super().__init__
#         SET borrowing_limit and late_penalty_per_day
#     END FUNCTION

#     FUNCTION view_profile
#         PRINT admin details
#     END FUNCTION
# END CLASS

# LibrarySystem Class

# CLASS LibrarySystem
#     FUNCTION __init__
#         SET current_user to None
#     END FUNCTION

#     FUNCTION main_menu
#         PRINT main menu options
#         PROMPT user for choice
#         IF choice is '1' THEN CALL User.signup
#         IF choice is '2' THEN CALL self.login
#         IF choice is '3' THEN PRINT exiting system
#         ELSE PRINT invalid input
#     END FUNCTION

#     FUNCTION login
#         WHILE True
#             TRY
#                 PROMPT user for email and password
#                 VALIDATE email format
#                 CONNECT to 'users.db'
#                 FETCH user details from users table
#                 IF user details found THEN
#                     CREATE user object based on user_type
#                     SET current_user to user object
#                     CALL corresponding menu function
#                     BREAK loop
#                 ELSE
#                     PRINT invalid login credentials
#             CATCH ValueError
#                 PRINT error message
#             CATCH Exception
#                 PRINT unexpected error
#             END TRY
#         END WHILE
#     END FUNCTION

#     FUNCTION member_menu
#         WHILE True
#             PRINT member menu options
#             PROMPT user for choice
#             CALL corresponding function based on choice
#             IF choice is '6' THEN BREAK loop
#         END WHILE
#     END FUNCTION

#     FUNCTION librarian_menu
#         WHILE True
#             PRINT librarian menu options
#             PROMPT user for choice
#             CALL corresponding function based on choice
#             IF choice is '7' THEN BREAK loop
#         END WHILE
#     END FUNCTION

#     FUNCTION admin_menu
#         WHILE True
#             PRINT admin menu options
#             PROMPT user for choice
#             CALL corresponding function based on choice
#             IF choice is '4' THEN BREAK loop
#         END WHILE
#     END FUNCTION

#     FUNCTION search_books
#         WHILE True
#             PRINT search books menu
#             PROMPT user for search term
#             IF user_search is '0' THEN BREAK loop
#             CONNECT to 'library.db'
#             FETCH books matching search term
#             PRINT search results
#         END WHILE
#     END FUNCTION

#     FUNCTION borrow_book
#         WHILE True
#             PRINT borrow book menu
#             PROMPT user for ISBN
#             IF isbn is '0' THEN BREAK loop
#             CONNECT to 'library.db'
#             FETCH book details by ISBN
#             PRINT book details
#             PROMPT user for confirmation
#             IF confirmed THEN
#                 CHECK availability and borrowing limit
#                 UPDATE book status to unavailable
#                 INSERT borrowing request into requests table
#                 REFRESH borrowed_books list
#                 COMMIT and CLOSE connection
#                 PRINT book borrowed successfully
#             ELSE
#                 PRINT borrowing cancelled
#         END WHILE
#     END FUNCTION

#     FUNCTION return_book
#         WHILE True
#             PRINT borrowed books
#             PROMPT user for ISBN to return
#             IF isbn_or_return is '0' THEN BREAK loop
#             CONNECT to 'library.db'
#             CHECK if book is borrowed by user
#             UPDATE book status to available
#             DELETE borrowing request from requests table
#             REFRESH borrowed_books list
#             COMMIT and CLOSE connection
#             PRINT book returned successfully
#         END WHILE
#     END FUNCTION

#     FUNCTION reserve_book
#         WHILE True
#             PRINT reserve book menu
#             PROMPT user for ISBN
#             IF isbn is '0' THEN BREAK loop
#             CONNECT to 'library.db'
#             FETCH book details by ISBN
#             PRINT book details
#             IF book is unavailable THEN
#                 PROMPT user for confirmation
#                 IF confirmed THEN
#                     INSERT reservation request into requests table
#                     COMMIT and CLOSE connection
#                     PRINT reservation request submitted
#                 ELSE
#                     PRINT reservation cancelled
#             ELSE
#                 PRINT book is available for borrowing
#         END WHILE
#     END FUNCTION

#     FUNCTION add_book
#         PROMPT librarian for book details
#         CONNECT to 'library.db'
#         INSERT book into books table
#         COMMIT and CLOSE connection
#         PRINT book added successfully
#     END FUNCTION

#     FUNCTION update_book
#         PROMPT librarian for ISBN
#         CONNECT to 'library.db'
#         FETCH book details by ISBN
#         PRINT current book details
#         PROMPT librarian for updated details
#         UPDATE book in books table
#         COMMIT and CLOSE connection
#         PRINT book updated successfully
#     END FUNCTION

#     FUNCTION remove_book
#         PROMPT librarian for ISBN
#         CONNECT to 'library.db'
#         FETCH book details by ISBN
#         PRINT book details
#         PROMPT librarian for confirmation
#         IF confirmed THEN
#             DELETE book from books table
#             COMMIT and CLOSE connection
#             PRINT book removed successfully
#         ELSE
#             PRINT book removal cancelled
#     END FUNCTION

#     FUNCTION handle_requests
#         CONNECT to 'library.db'
#         FETCH pending requests
#         PRINT pending requests
#         PROMPT librarian for request ID to handle
#         FETCH request details by request ID
#         PROMPT librarian for action (approve/reject)
#         UPDATE request status in requests table
#         COMMIT and CLOSE connection
#         PRINT request handled successfully
#     END FUNCTION

#     FUNCTION generate_overdue_report
#         CONNECT to 'library.db'
#         CONNECT to 'users.db'
#         FETCH overdue books from library.db
#         PRINT overdue books report
#         FETCH user details from users.db for each overdue book
#         PRINT book details with user fullname
#     END FUNCTION

#     FUNCTION manage_users
#         WHILE True
#             PRINT manage users menu
#             PROMPT admin for choice
#             CALL corresponding function based on choice
#             IF choice is '5' THEN BREAK loop
#         END WHILE
#     END FUNCTION

#     FUNCTION view_all_users
#         CONNECT to 'users.db'
#         FETCH all users from users table
#         PRINT user details
#     END FUNCTION

#     FUNCTION add_user
#         PROMPT admin for user details
#         CONNECT to 'users.db'
#         INSERT user into users table
#         COMMIT and CLOSE connection
#         PRINT user added successfully
#     END FUNCTION

#     FUNCTION update_user
#         PROMPT admin for user ID
#         CONNECT to 'users.db'
#         FETCH user details by user ID
#         PRINT current user details
#         PROMPT admin for updated details
#         UPDATE user in users table
#         COMMIT and CLOSE connection
#         PRINT user updated successfully
#     END FUNCTION

#     FUNCTION delete_user
#         PROMPT admin for user ID
#         CONNECT to 'users.db'
#         FETCH user details by user ID
#         PRINT user details
#         PROMPT admin for confirmation
#         IF confirmed THEN
#             DELETE user from users table
#             COMMIT and CLOSE connection
#             PRINT user deleted successfully
#         ELSE
#             PRINT user deletion cancelled
#     END FUNCTION

#     FUNCTION set_library_rules
#         PRINT current library rules
#         PROMPT admin for new borrowing limit and late penalty
#         UPDATE borrowing_limit and late_penalty_per_day
#         PRINT library rules updated successfully
#     END FUNCTION
# END CLASS

# Main Program

# CREATE instance of LibrarySystem
# CALL main_menu on library_system instance

from abc import ABC, abstractmethod # For abstract method view_profile, forces implementation for all subclasses
import sqlite3 # DB & tables
import re # RegEx for validation of certain inputs
from getpass import getpass # Hide password when user inputs
from datetime import datetime, timedelta # Mostly for due date
# Potentially add AES encryption? Make class on its own?

def setup_databases():
    # User DB - User details for signup/login
    connect_users = sqlite3.connect('users.db') # Users DB - ALL user details stored here
    conn_users = connect_users.cursor()
    conn_users.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT, dob DATE, phone_num TEXT, email_address TEXT NOT NULL, password TEXT NOT NULL, user_type TEXT)")
    connect_users.commit()
    connect_users.close()

    # Library DB - Actual library holding book info, item_id acts as accession number(?), also includes requests table for borrowing and reservations
    connect_library = sqlite3.connect('library.db')
    conn_library = connect_library.cursor()
    conn_library.execute("CREATE TABLE IF NOT EXISTS books(item_id INT PRIMARY KEY, ISBN TEXT, title TEXT, author DATE, publisher TEXT, publication_date INT, edition TEXT, language TEXT, genre TEXT, available INTEGER DEFAULT 1)")
    conn_library.execute("CREATE TABLE IF NOT EXISTS requests(request_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, item_id INT, request_type TEXT, status TEXT, due_date DATE)")
    connect_library.commit()
    connect_library.close()

setup_databases() # Call to create DB files and tables

class User(ABC): # Abstract Base Class for abstract method
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password, user_type):
        self.user_id = user_id
        self.fullname = fullname
        self.dob = dob
        self._phone_num = phone_num  # Protected attribute (encapsulation)
        self.email_address = email_address # Was originally meant to be protected but was needed outside of class
        self.__password = password  # Private attribute (encapsulation)
        self.user_type = user_type

    @classmethod # Class method so it can be called without instatiating object of class (bound to class instead of object)
    def signup(cls):
        conn_signupuser = sqlite3.connect('users.db') # to insert the details into the user table
        curs_signup_user = conn_signupuser.cursor()

        correct_signup = False
        while not correct_signup:
            ## ENTERING ACCOUNT TYPE ##
            try:
                print("\n-    Signup Menu    -\n\nPlease enter the corresponding number for what type of user you are:\n1. Member \n2. Librarian \n3. Admin\n4. Exit signup menu\n")
                signup_choice = int(input("Enter choice: "))
                if signup_choice not in [1, 2, 3, 4]:
                    raise ValueError("Invalid choice. Please enter a valid option.")
                elif signup_choice == 1:
                    signup_choice = "Member"
                elif signup_choice == 2:
                    key_lib = input("Enter librarian key: ") # Key so that only certified librarians can signup accounts, only done to show difference between member account & librarian/admin
                    if key_lib != "CertifiedLibrarianKey": # Just to differentiate logins from member b/c they are too similar
                        print("Invalid librarian key. Please enter the certified key.")
                    else:
                        signup_choice = "Librarian"
                elif signup_choice == 3:
                    key_admin = input("Enter admin key: ")
                    if key_admin != "AdministratorsKey":
                        print("Invalid librarian key. Please enter the certified key.")
                    else:
                        signup_choice = "Admin"
                else:
                    break
            except ValueError as e: # Anything that isnt an integer and invalid numbers raise error here
                print(f"Error: {e}") # f string - string interpolation - makes code easier to read
                print("Invalid choice. Please enter a valid number and corresponding choice.")

            ## ENTERING ACCOUNT DETAILS ## # Kept getting UnboundLocalError: cannot access local variable 'users_phonenum' where it is not associated with a value if all detail inputs are not in separate loops
            while True:
                users_name = input("\nEnter full name: ")
                if any(char.isdigit() for char in users_name): # Checking for no numbers in name for valid entry
                    print("Invalid name. Please enter a valid name without numbers.")
                else:
                    break
            while True:
                users_dob = input("Please enter your date of birth in the format 'YYYY-MM-DD': ")
                # Checks if date format is input correctly, raw strings used so that \ won't be used for escape, regex taken from: https://stackoverflow.com/questions/22061723/regex-date-validation-for-yyyy-mm-dd
                if not re.search(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$', users_dob): 
                    print("Date of birth invalid. Please enter a valid date.")
                else:
                    break
            users_phonenum = input("Enter phone number: ") # Enter regex here? But layout is confusing
            while True:
                users_email = input("Enter email address: ")
                # Checks if email address is formatted correctly, regex taken from: https://regexr.com/3e48o
                if not re.search(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$', users_email):
                    print("Email address invalid. Please enter a valid email address.")
                else:
                    break
            users_password = getpass("Enter password: ")
            correct_signup = True

            ## PUTTING DETAILS INTO DATABASE TABLE: USERS ##
            try:
                curs_signup_user.execute("INSERT INTO users (fullname, dob, phone_num, email_address, password, user_type) VALUES (?, ?, ?, ?, ?, ?)", (users_name, users_dob, users_phonenum, users_email, users_password, signup_choice))
                conn_signupuser.commit()
                conn_signupuser.close()
                print("Signup successful! You can now login.")
                correct_signup = True
            except sqlite3.IntegrityError: #Checking for error that might be raised if email address is already used for another user's details
                print("Error: Email already exists. Try again.")

    @classmethod # Class method so it can be called without instatiating object of class, repeatedly making objects for classes would have resulted in longer code
    def login(cls):
        while True:
            try:
                emailaddress = input("\nEnter your email address: ")
                password = getpass("Enter your password: ")

                if not re.search(r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$', emailaddress):
                    raise ValueError("Email address invalid. Please enter a valid email address.")

                conn_loginuser = sqlite3.connect('users.db')
                conn_loginuser.row_factory = sqlite3.Row # Changes the way details are accessed so that its treated similar to a dictionary instead by using keys (was a tuple if called normally, harder to read b/c of multiple columns)
                curs_login_user = conn_loginuser.cursor()

                # Check database for the user's matching detailss
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

                    library_system = LibrarySystem() # Call librarysystem class for the menus
                    if user_type == "Member":
                        user = Member(user_id, fullname, dob, phone_num, email_address, password)
                        # Check and display notifications
                        notifications = user.check_notifications()
                        if notifications:
                            print("\nNotifications:")
                            for notification in notifications:
                                print(f"- {notification}")
                        library_system.member_menu(user)
                    elif user_type == "Librarian":
                        user = Librarian(user_id, fullname, dob, phone_num, email_address, password)
                        library_system.librarian_menu(user)
                    elif user_type == "Admin":
                        user = Admin(user_id, fullname, dob, phone_num, email_address, password)
                        library_system.admin_menu(user)
                    break

                else:
                    print("Invalid login credentials, please try again.")

            except ValueError as e:
                # Invalid email format
                print(f"Error: {e}")
            except Exception as e:
                # Unexpected errors caught here just in case
                print(f"An unexpected error occurred: {e}")
    
    # Polymorphism - view profile will be overridden in all child classes with different implementations depending on the user
    @abstractmethod # Abstraction - Abstract method: FORCE implementation of view profile in child classes, will show different user details
    def view_profile(self):
        pass

class Member(User):
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password):
        super().__init__(user_id, fullname, dob, phone_num, email_address, password, "Member")
        self.borrowed_books = self.fetch_borrowed_books() # List of borrowed books to be viewed in view_details
        self.__reserved_books = self.fetch_reserved_books()  # Private attribute

    # Getter for reserved books - Encapsulation
    def get_reserved_books(self):
        return self.__reserved_books

    # Setter for reserved books (with validation) - Encapsulation
    def set_reserved_books(self, new_reserved_books):
        if not isinstance(new_reserved_books, list):
            raise ValueError("Reserved books must be a list.")
        self.__reserved_books = new_reserved_books

    def fetch_borrowed_books(self): # Gets borrowed books to display in user details
        borrowed_books = []
        conn_library = sqlite3.connect('library.db')
        conn_library.row_factory = sqlite3.Row
        cursor = conn_library.cursor()

        try: # Gets all borrowed books from that user and displays them
            cursor.execute("SELECT books.ISBN, books.title, books.author, requests.due_date FROM requests JOIN books ON requests.item_id = books.item_id WHERE requests.user_id = ? AND requests.request_type = 'Borrow' AND requests.status = 'Borrowed'", (self.user_id,))
            books = cursor.fetchall()

            for book in books: # Adds borrowed books from table to list
                borrowed_books.append({'ISBN': book['ISBN'], 'title': book['title'], 'author': book['author'], 'due_date': book['due_date']})
        
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            conn_library.close()
        return borrowed_books

    def fetch_reserved_books(self): # Gets reservations to display for user
        reserved_books = []
        conn_library = sqlite3.connect('library.db')
        conn_library.row_factory = sqlite3.Row
        cursor = conn_library.cursor()

        try:
            cursor.execute("""
                SELECT books.ISBN, books.title, books.author
                FROM requests
                JOIN books ON requests.item_id = books.item_id
                WHERE requests.user_id = ? AND requests.request_type = 'Reserve' AND requests.status = 'Approved'
            """, (self.user_id,))
            books = cursor.fetchall()

            for book in books:
                reserved_books.append({'ISBN': book['ISBN'], 'title': book['title'], 'author': book['author']})
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}") 
        finally:
            conn_library.close()
        return reserved_books

    def view_profile(self):
        print(f"\nMember ID: {self.user_id}\nName: {self.fullname}\nEmail: {self.email_address}\nBorrowed Books:")
        for book in self.borrowed_books:
            print(f"ISBN: {book['ISBN']}, Title: {book['title']}, Author: {book['author']}, Due Date: {book['due_date']}")
        
        self._Member__reserved_books = self.fetch_reserved_books()  # Refresh reserved books
        print("\nReserved Books:")
        for book in self._Member__reserved_books:
            print(f"ISBN: {book['ISBN']}, Title: {book['title']}, Author: {book['author']}")

    def check_notifications(self):
        notifications = []
        conn_library = sqlite3.connect('library.db')
        conn_library.row_factory = sqlite3.Row
        cursor = conn_library.cursor()

        try:
            # Check for due dates and overdue books
            cursor.execute("""
                SELECT books.title, requests.due_date
                FROM requests
                JOIN books ON requests.item_id = books.item_id
                WHERE requests.user_id = ? AND requests.request_type = 'Borrow' AND requests.status = 'Borrowed'
            """, (self.user_id,))
            borrowed_books = cursor.fetchall()

            current_date = datetime.now().date()
            for book in borrowed_books:
                due_date = datetime.strptime(book['due_date'], '%Y-%m-%d').date()
                if due_date == current_date:
                    notifications.append(f"Reminder: The book '{book['title']}' is due today.")
                elif due_date < current_date:
                    notifications.append(f"Overdue: The book '{book['title']}' is overdue. Please return it as soon as possible.")

            # Check for approved reservations
            cursor.execute("""
                SELECT books.title
                FROM requests
                JOIN books ON requests.item_id = books.item_id
                WHERE requests.user_id = ? AND requests.request_type = 'Reserve' AND requests.status = 'Approved'
            """, (self.user_id,))
            approved_reservations = cursor.fetchall()

            for reservation in approved_reservations:
                notifications.append(f"Notification: Your reservation for the book '{reservation['title']}' has been approved.")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            conn_library.close()

        return notifications

class Librarian(User):
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password):
        super().__init__(user_id, fullname, dob, phone_num, email_address, password, "Librarian")

    def view_profile(self):
        print(f"\nLibrarian ID: {self.user_id}\nName: {self.fullname}\nEmail: {self.email_address}")
        print(f"Account Type: {self.user_type}")

class Admin(User):
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password):
        super().__init__(user_id, fullname, dob, phone_num, email_address, password, "Admin")
        self.borrowing_limit = 5  # Constraints/rules that the admin can change
        self.late_penalty_per_day = 1

    def view_profile(self):
        print(f"\nAdmin ID: {self.user_id}\nName: {self.fullname}\nEmail: {self.email_address}")
        print(f"Account Type: {self.user_type}")

class LibrarySystem:
    ## MEMBER MENU - ALL METHODS THAT MANIPULATE MEMBER MENU HERE ##
    def member_menu(self, user):
        while True:
            print("""\n-  Library Menu    -
                  
                  1. View Profile
                  2. Search for Books
                  3. Borrow a Book
                  4. Return a Book
                  5. Reserve a Book
                  6. Logout\n""")
            choice = input("Enter choice: ")
            if choice == "1":
                user.view_profile() # Polymorphism - duck typing used here, uses expected properties
            elif choice == "2":
                self.search_books(user)
            elif choice == "3":
                self.borrow_book(user)
            elif choice == "4":
                self.return_book(user)
            elif choice == "5":
                self.reserve_book(user)
            elif choice == "6":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def search_books(self, user):
        while True:
            print("""\n-    Search Books    -\n
                  Enter a title or author to search for books.
                  Type '0' to go back to the menu.\n""")
            user_search = input("Enter search term: ")
            if user_search == "0":
                print("Returning to menu...")
                break

            conn_library = sqlite3.connect('library.db')
            conn_library.row_factory = sqlite3.Row
            cursor = conn_library.cursor()

            try:
                cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f'%{user_search}%', f'%{user_search}%'))
                books = cursor.fetchall()
                if books:
                    print("\nSearch results:")
                    for item in books:
                        print(f"ISBN: {item['ISBN']}, Title: {item['title']}, Author: {item['author']}, Publisher: {item['publisher']}, Genre: {item['genre']}, Available: {'Yes' if item['available'] else 'No'}")
                else:
                    print("No books found matching your search.\n")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                conn_library.close()

    def borrow_book(self, user):
        while True:
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
                cursor.execute("SELECT * FROM books WHERE ISBN = ?", (isbn,))
                book = cursor.fetchone()

                if book:
                    print(f"\nBook Details:\nISBN: {book['ISBN']},\nTitle: {book['title']},\nAuthor: {book['author']},\nPublisher: {book['publisher']},\nPublication Date: {book['publication_date']},\nEdition: {book['edition']},\nLanguage: {book['language']},\nGenre: {book['genre']},\nAvailable: {'Yes' if book['available'] else 'No'}")
                    
                    confirm = input("\nDo you want to borrow this book? (Type 'yes' or '1' to confirm, or any other key to cancel): ").strip().lower()
                    if confirm in ['yes', '1']:
                        if book['available']:
                            if len(user.borrowed_books) < 5:
                                cursor.execute("UPDATE books SET available = 0 WHERE ISBN = ?", (isbn,))
                                due_date = (datetime.now() + timedelta(weeks=2)).strftime('%Y-%m-%d')
                                cursor.execute("INSERT INTO requests (user_id, item_id, request_type, status, due_date) VALUES (?, ?, ?, ?, ?)", (user.user_id, book['item_id'], "Borrow", "Borrowed", due_date))
                                
                                user.borrowed_books = user.fetch_borrowed_books()
                                conn_library.commit()
                                print(f"\nBook with ISBN {isbn} borrowed successfully. Due date: {due_date}")

                                # Check and display notifications after borrowing
                                notifications = user.check_notifications()
                                if notifications:
                                    print("\nNotifications:")
                                    for notification in notifications:
                                        print(f"- {notification}")
                            else:
                                print("\nYou have reached the maximum limit of 5 borrowed books.")
                        else:
                            print("\nBook is not available for borrowing.")
                    else:
                        print("\nBorrowing cancelled. Please enter the ISBN again or enter another ISBN.")
                else:
                    print("\nBook with this ISBN does not exist.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                conn_library.close()

    def return_book(self, user):
        while True:
            print("\n-    Return a Book    -")
            if not user.borrowed_books:
                print("\nYou have no books currently borrowed.")
                print("Returning to the menu...")
                break

            print("Your currently borrowed books:")
            for book in user.borrowed_books:
                print(f"ISBN: {book['ISBN']}, Title: {book['title']}, Author: {book['author']}")

            isbn_or_return = input("\nEnter the ISBN of the book you want to return (or type '0' to go back): ")
            if isbn_or_return == "0":
                print("Returning to the menu...")
                break

            conn_library = sqlite3.connect('library.db')
            conn_library.row_factory = sqlite3.Row
            cursor = conn_library.cursor()

            try:
                if any(book['ISBN'] == isbn_or_return for book in user.borrowed_books):
                    cursor.execute("UPDATE books SET available = 1 WHERE ISBN = ?", (isbn_or_return,))
                    cursor.execute("DELETE FROM requests WHERE user_id = ? AND item_id = (SELECT item_id FROM books WHERE ISBN = ?) AND request_type = 'Borrow'", (user.user_id, isbn_or_return))
                    
                    conn_library.commit()
                    
                    # Refresh the borrowed_books list
                    user.borrowed_books = user.fetch_borrowed_books()
                    
                    print(f"Book with ISBN {isbn_or_return} returned successfully.")
                else:
                    print("You have not borrowed a book with this ISBN.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
            finally:
                conn_library.close()

    def reserve_book(self, user):
        while True:
            print("""\n- Reserve a Book -
            Enter the ISBN of the book you want to reserve.
            Type '0' to go back to the menu.\n""")
            isbn = input("Enter ISBN: ").strip()
            if isbn == "0":
                print("Returning to the menu...")
                break

            conn_library = sqlite3.connect('library.db')
            conn_library.row_factory = sqlite3.Row
            cursor = conn_library.cursor()

            try:
                cursor.execute("SELECT * FROM books WHERE ISBN = ?", (isbn,))
                book = cursor.fetchone()

                if book:
                    print(f"\nBook Details:\nISBN: {book['ISBN']},\nTitle: {book['title']},\nAuthor: {book['author']},\nPublisher: {book['publisher']},\nPublication Date: {book['publication_date']},\nEdition: {book['edition']},\nLanguage: {book['language']},\nGenre: {book['genre']},\nAvailable: {'Yes' if book['available'] else 'No'}")
                    if not book['available']:  # Book is unavailable
                        confirm = input("\nDo you want to reserve this book? (Type 'yes' or '1' to confirm, or any other key to cancel): ").strip().lower()
                        if confirm in ['yes', '1']:
                            # Insert a reservation request into the requests table
                            cursor.execute("""
                                INSERT INTO requests (user_id, item_id, request_type, status)
                                VALUES (?, ?, ?, ?)
                            """, (user.user_id, book['item_id'], "Reserve", "Pending"))
                            conn_library.commit()
                            print("\nReservation request submitted successfully. The librarian will review your request.")
                        else:
                            print("\nReservation cancelled. Please enter the ISBN again or enter another ISBN.")
                    else:
                        print("\nThis book is currently available. You can borrow it instead of reserving it.")
                else:
                    print("\nBook with this ISBN does not exist.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                conn_library.close()

    ## LIBRARIAN MENU - ALL METHODS FOR LIBRARIAN MENU HERE ##
    def librarian_menu(self, user):
        while True:
            print("""\n-  Librarian Menu    -
                  
                  1. View Profile
                  2. Add a Book
                  3. Update a Book
                  4. Remove a Book
                  5. Handle Borrowing/Reservation Requests
                  6. Generate Overdue Books Report
                  7. Logout\n""")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                user.view_profile() # Polymorphism - duck typing used here, uses expected properties
            elif choice == "2":
                self.add_book()
            elif choice == "3":
                self.update_book()
            elif choice == "4":
                self.remove_book()
            elif choice == "5":
                self.handle_requests()
            elif choice == "6":
                self.generate_overdue_report()
            elif choice == "7":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_profile(self, user):
        print(f"\n{user.user_type} ID: {user.user_id}\nName: {user.fullname}\nEmail: {user.email_address}")

    def add_book(self):
        print("\n- Add a Book -")
        try:
            # Get book details from the librarian
            item_id = int(input("Enter the item ID: "))
            isbn = input("Enter the ISBN: ")
            title = input("Enter the title: ")
            author = input("Enter the author: ")
            publisher = input("Enter the publisher: ")
            publication_date = input("Enter the publication date (YYYY-MM-DD): ")
            edition = input("Enter the edition: ")
            language = input("Enter the language: ")
            genre = input("Enter the genre: ")

            # Insert the book into the database
            with sqlite3.connect('library.db') as conn_library:  # Use a context manager
                cursor = conn_library.cursor()
                cursor.execute("""
                    INSERT INTO books (item_id, ISBN, title, author, publisher, publication_date, edition, language, genre, available)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """, (item_id, isbn, title, author, publisher, publication_date, edition, language, genre))
                conn_library.commit()
            print("Book added successfully!")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def update_book(self):
        print("\n- Update a Book -")
        try:
            isbn = input("Enter the ISBN of the book to update: ")
            conn_library = sqlite3.connect('library.db')
            conn_library.row_factory = sqlite3.Row
            cursor = conn_library.cursor()
            cursor.execute("SELECT * FROM books WHERE ISBN = ?", (isbn,))
            book = cursor.fetchone()

            if book:
                print(f"\nCurrent Book Details:\nISBN: {book['ISBN']},\nTitle: {book['title']},\nAuthor: {book['author']},\nPublisher: {book['publisher']},\nPublication Date: {book['publication_date']},\nEdition: {book['edition']},\nLanguage: {book['language']},\nGenre: {book['genre']}")
                
                # Get updated details
                title = input("\nEnter new title (leave blank to keep current): ") or book['title']
                author = input("Enter new author (leave blank to keep current): ") or book['author']
                publisher = input("Enter new publisher (leave blank to keep current): ") or book['publisher']
                publication_date = input("Enter new publication date (YYYY-MM-DD) (leave blank to keep current): ") or book['publication_date']
                edition = input("Enter new edition (leave blank to keep current): ") or book['edition']
                language = input("Enter new language (leave blank to keep current): ") or book['language']
                genre = input("Enter new genre (leave blank to keep current): ") or book['genre']

                # Update the book in the database
                cursor.execute("""
                    UPDATE books SET title = ?, author = ?, publisher = ?, publication_date = ?, edition = ?, language = ?, genre = ?
                    WHERE ISBN = ?
                """, (title, author, publisher, publication_date, edition, language, genre, isbn))
                conn_library.commit()
                print("\nBook updated successfully!")
            else:
                print("\nBook with this ISBN does not exist.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            conn_library.close()

    def remove_book(self):
        print("\n- Remove a Book -")
        try:
            isbn = input("Enter the ISBN of the book to remove: ")
            conn_library = sqlite3.connect('library.db')
            conn_library.row_factory = sqlite3.Row
            cursor = conn_library.cursor()
            cursor.execute("SELECT * FROM books WHERE ISBN = ?", (isbn,))
            book = cursor.fetchone()

            if book:
                confirm = input(f"Are you sure you want to remove the book '{book['title']}' by {book['author']}? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    cursor.execute("DELETE FROM books WHERE ISBN = ?", (isbn,))
                    conn_library.commit()
                    print("\nBook removed successfully!")
                else:
                    print("\nBook removal cancelled.")
            else:
                print("\nBook with this ISBN does not exist.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            conn_library.close()

    def handle_requests(self):
        print("\n- Handle Borrowing and Reservation Requests -")
        try:
            conn_library = sqlite3.connect('library.db')
            conn_library.row_factory = sqlite3.Row
            cursor = conn_library.cursor()

            # Fetch all pending requests
            cursor.execute("SELECT * FROM requests WHERE status = 'Pending'")
            requests = cursor.fetchall()

            if requests:
                print("\nPending Requests:")
                for request in requests:
                    print(f"Request ID: {request['request_id']}, User ID: {request['user_id']}, Item ID: {request['item_id']}, Type: {request['request_type']}")

                request_id = input("Enter the request ID to handle (or '0' to go back): ")
                if request_id != "0":
                    cursor.execute("SELECT * FROM requests WHERE request_id = ?", (request_id,))
                    request = cursor.fetchone()

                    if request:
                        action = input(f"Do you want to approve or reject this request? (approve/reject): ").strip().lower()
                        if action == 'approve':
                            cursor.execute("UPDATE requests SET status = 'Approved' WHERE request_id = ?", (request_id,))
                            conn_library.commit()
                            print(f"Reservation request approved for user ID {request['user_id']}.")
                        elif action == 'reject':
                            cursor.execute("UPDATE requests SET status = 'Rejected' WHERE request_id = ?", (request_id,))
                            conn_library.commit()
                            print("Request rejected successfully!")
                        else:
                            print("Invalid action. Please enter 'approve' or 'reject'.")
                    else:
                        print("Request with this ID does not exist.")
            else:
                print("No pending requests.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            conn_library.close()

    def generate_overdue_report(self):
        print("\n- Generate Overdue Books Report -")
        
        # Connect to the library database
        conn_library = sqlite3.connect('library.db')
        conn_library.row_factory = sqlite3.Row
        cursor_library = conn_library.cursor()
        
        # Connect to the users database
        conn_users = sqlite3.connect('users.db')
        conn_users.row_factory = sqlite3.Row
        cursor_users = conn_users.cursor()

        try:
            # Get the current date
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Fetch overdue books from library.db
            cursor_library.execute("""
                SELECT requests.user_id, books.ISBN, books.title, books.author, requests.due_date
                FROM requests
                JOIN books ON requests.item_id = books.item_id
                WHERE requests.due_date < ? AND requests.status = 'Borrowed'
            """, (current_date,))
            overdue_books = cursor_library.fetchall()

            if overdue_books:
                print("\nOverdue Books Report:")
                
                # Loop through each overdue book and fetch the corresponding user's fullname from users.db
                for book in overdue_books:
                    # Fetch the fullname of the user from users.db
                    cursor_users.execute("SELECT fullname FROM users WHERE user_id = ?", (book['user_id'],))
                    user = cursor_users.fetchone()
                    
                    # Print book details along with user's fullname
                    if user:
                        print(f"ISBN: {book['ISBN']}, Title: {book['title']}, Author: {book['author']}, Due Date: {book['due_date']}, Borrower: {user['fullname']}")
                    else:
                        print(f"ISBN: {book['ISBN']}, Title: {book['title']}, Author: {book['author']}, Due Date: {book['due_date']}, Borrower: [User not found]")
            else:
                print("\nNo overdue books found.")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            conn_library.close()
            conn_users.close()

    ## ADMIN MENU - ALL METHODS FOR ADMIN MENU HERE ##
    def admin_menu(self, user):
        while True:
            print("""\n-  Admin Menu    -
                  
                  1. View Profile
                  2. Manage Users
                  3. Set Library Rules
                  4. Logout and Exit\n""")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                user.view_profile() # Polymorphism - duck typing used here, uses expected properties
            elif choice == "2":
                self.manage_users()
            elif choice == "3":
                self.set_library_rules(user)
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def manage_users(self):
        while True:
            print("""\n- Manage Users -
                  
                  1. View All Users
                  2. Add a User
                  3. Update a User
                  4. Delete a User
                  5. Back to Admin Menu\n""")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.view_all_users()
            elif choice == "2":
                self.add_user()
            elif choice == "3":
                self.update_user()
            elif choice == "4":
                self.delete_user()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def view_all_users(self):
        conn_users = sqlite3.connect('users.db')
        conn_users.row_factory = sqlite3.Row
        cursor = conn_users.cursor()

        try:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

            if users:
                print("\nAll Users:")
                for user in users:
                    print(f"User ID: {user['user_id']}, Name: {user['fullname']}, Email: {user['email_address']}, User Type: {user['user_type']}")
            else:
                print("No users found.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            conn_users.close()

    def add_user(self):
        print("\n- Add a User -")
        try:
            fullname = input("Enter full name: ")
            dob = input("Enter date of birth (YYYY-MM-DD): ")
            phone_num = input("Enter phone number: ")
            email = input("Enter email address: ")
            password = getpass("Enter password: ")
            user_type = input("Enter user type (Member/Librarian/Admin): ").capitalize()

            conn_users = sqlite3.connect('users.db')
            cursor = conn_users.cursor()
            cursor.execute("INSERT INTO users (fullname, dob, phone_num, email_address, password, user_type) VALUES (?, ?, ?, ?, ?, ?)",
                           (fullname, dob, phone_num, email, password, user_type))
            conn_users.commit()
            conn_users.close()
            print("User added successfully!")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def update_user(self):
        print("\n- Update a User -")
        try:
            user_id = input("Enter the user ID to update: ")
            conn_users = sqlite3.connect('users.db')
            conn_users.row_factory = sqlite3.Row
            cursor = conn_users.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()

            if user:
                print(f"\nCurrent User Details:\nUser ID: {user['user_id']}, Name: {user['fullname']}, Email: {user['email_address']}, User Type: {user['user_type']}")
                
                # Get updated details, implement way to constantly refresh table data?s
                fullname = input("\nEnter new full name (leave blank to keep current): ") or user['fullname']
                dob = input("Enter new date of birth (YYYY-MM-DD) (leave blank to keep current): ") or user['dob']
                phone_num = input("Enter new phone number (leave blank to keep current): ") or user['phone_num']
                email = input("Enter new email address (leave blank to keep current): ") or user['email_address']
                password = getpass("Enter new password (leave blank to keep current): ") or user['password']
                user_type = input("Enter new user type (Member/Librarian/Admin) (leave blank to keep current): ").capitalize() or user['user_type']

                # Update the user in the database
                cursor.execute("""
                    UPDATE users SET fullname = ?, dob = ?, phone_num = ?, email_address = ?, password = ?, user_type = ?
                    WHERE user_id = ?
                """, (fullname, dob, phone_num, email, password, user_type, user_id))
                conn_users.commit()
                print("\nUser updated successfully!")
            else:
                print("\nUser with this ID does not exist.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            conn_users.close()

    def delete_user(self):
        print("\n- Delete a User -")
        try:
            user_id = input("Enter the user ID to delete: ")
            conn_users = sqlite3.connect('users.db')
            conn_users.row_factory = sqlite3.Row
            cursor = conn_users.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()

            if user:
                confirm = input(f"Are you sure you want to delete the user '{user['fullname']}'? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                    conn_users.commit()
                    print("\nUser deleted successfully!")
                else:
                    print("\nUser deletion cancelled.")
            else:
                print("\nUser with this ID does not exist.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            conn_users.close()

    def set_library_rules(self, user):
        print("\n- Set Library Rules -")
        try:
            print(f"Current Borrowing Limit: {user.borrowing_limit} books")
            print(f"Current Late Penalty: £{user.late_penalty_per_day} per day")
            
            new_limit = input("Enter new borrowing limit (leave blank to keep current): ")
            if new_limit:
                user.borrowing_limit = int(new_limit)
            
            new_penalty = input("Enter new late penalty per day (leave blank to keep current): ")
            if new_penalty:
                user.late_penalty_per_day = float(new_penalty)
            
            print("\nLibrary rules updated successfully!")
            print(f"New Borrowing Limit: {user.borrowing_limit} books")
            print(f"New Late Penalty: £{user.late_penalty_per_day} per day")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

## SLMS STARTING MENU ##
print("""\n-  Library Management System   -
      
    Please type the corresponding choice for what you would like to do:
    1. Signup
    2. Login
    3. Exit
    """)
# User signup/login
while True:
    choice = input("Enter choice: ")
    if choice == "1":
        User.signup()
        break
    elif choice == "2":
        User.login()
        break
    elif choice == "3":
        print("Exiting system...")
        break
    else:
        print("Invalid input. Please enter a valid choice.")
        