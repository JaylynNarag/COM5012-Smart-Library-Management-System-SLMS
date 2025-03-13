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
    conn_library.execute("CREATE TABLE IF NOT EXISTS books(item_id INT PRIMARY KEY, ISBN TEXT, author DATE, publisher TEXT, publication_date INT, edition TEXT, language TEXT, genre TEXT)") # DB table for library items/books
    conn_library.execute("CREATE TABLE IF NOT EXISTS requests(request_id INTEGER PRIMARY KEY AUTOINCREMENT, member_id INT, book_id INT, request_type TEXT, status TEXT)") # DB table for requests = reservations, borrowed books
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
                print("\n-    Signup Menu    -\n\nPlease enter the corresponding number for what type of user you are:\n1. Member \n2. Librarian \n3. Admin\n")
                signup_choice = int(input("Enter choice: "))
                if signup_choice not in [1, 2, 3]:
                    raise ValueError("Invalid choice. Please enter a valid option.")
                elif signup_choice == 1:
                    signup_choice = "Member" 
                elif signup_choice == 2: # Key so that only certified librarians can signup accounts, only done to show difference between member account & librarian/admin
                    key_lib = input("Enter librarian key: ")
                    if key_lib != "CertifiedLibrarianKey":
                        print("Invalid librarian key. Please enter the certified key.")
                    else:
                        signup_choice = "Librarian"
                else: # Key so that only certified admins can signup accounts, only done to show difference between member account & librarian/admin
                    key_admin = input("Enter admin key: ")
                    if key_admin != "AdministratorsKey":
                        print("Invalid librarian key. Please enter the certified key.")
                    else:
                        signup_choice = "Admin"      
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
                correct_signup = True 
            except sqlite3.IntegrityError:
                print("Error: Email already exists. Try again.")
        print("Signup successful! You can now login.") # ADD SMTH HERE LIKE 'Press any key to go back to login menu'(?)






























    def login(self, emailaddress, password): # Emailaddress & password parameters to be entered & checked against DB
        conn_loginuser = sqlite3.connect('users.db')
        curs_login_user = conn_loginuser.cursor()
        curs_login_user.execute("SELECT * FROM users WHERE email_address = ? AND password = ?", (emailaddress, password))
        user_details = curs_login_user.fetchone() # Retrieves line where details are in the system
        conn_loginuser.close()

        if user_details != None:
            user_type = user_details[6] #gets user_type from the details fetched from the db
            # if user_type == "Member":
            # elif user_type == "Librarian":
            # elif user_type == "Administrator":
        else:
            print("Invalid login credentials! Please try again.") # ADD SMTH TO GET USER TO TRY AGAIN, LOOP HERE?
            return None
    
    def view_profile(self):
        pass




























class Member(User): # Inherits from user class
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password): # inherit everything except user type, member class already being called so member type already indicated
        super().__init__(user_id, fullname, dob, phone_num, email_address, password, "Member")
        self.borrowed_books = [] # list of borrowed books, public attr.
        self.__reserved_books = [] # private attr.
    
    def view_profile(self): # f string for more readability, only shows few details (maybe add modify details to change info stored on db?)
        print(f"Member ID: {self.user_id} + \n + Name: {self.fullname} + \n + Email: {self.email_address} + \n + Borrowed Books: {self.borrowed_books} + \n + Reserved Books: {self.__reserved_books}")

    ### TO BE IMPLEMENTED, BORROW AND RESERVE BOOKS BY USER ###
    # def submit_borrow_req():
    
    # def submit_reserve_req():

    def member_menu(self): # library menu tailored to member user
        while True:
            print("""-  Library Menu    -
                  
                  1. View Profile
                  2. Search the Library
                  3. Borrow from the Library
                  4. Return to the Library
                  5. Reserve from the Library
                  6. Logout\n""")
            choice = input("Enter choice: ").strip()
            if choice == "1": # View Profile
                self.view_profile()
            ### OTHER CHOICES TO BE IMPLEMENTED ###
            else:
                break
    
    ### TO BE IMPLEMENTED, WORK WITH THE MEMBER MENU ###
    # def search_book(self):
    
    # def borrow_book(self):
    
    # def return_book(self):
    
    # def reserve_book(self):

class Librarian(User): # Inherits from user class
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password): # inherit everything except user type, librarian class already being called so librarian type already indicated
        super().__init__(user_id, fullname, dob, phone_num, email_address, password, "Librarian")
    
    def view_profile(self):
        print(f"Member ID: {self.user_id} + \n + Name: {self.fullname} + \n + Email: {self.email_address}")

    ### TO BE IMPLEMENTED, LIBRARIAN SHOULD BE ABLE TO SEE REQUESTS AND FILTER WHICH ONES ARE SHOWN E.G. OVERDUE ONES, AND HANDLE REQUESTS THAT MAY NEED APPROVAL ###
    # def view_requests(self):
    
    # def handle_requests(self):

    def librarian_menu(self):
        while True:
            print("""-  Library Menu    -
                  
                  1. View Profile
                  2. Add an Item to the Library
                  3. Update an item from the Library
                  4. Remove an item from the Library
                  5. Reserve from the Library
                  6. Logout\n""")
            choice = input("Enter choice: ").strip() # no extra trails/unnecessary characters to be input by user, maybe not necessary? DONT MAKE INTO INT. SHOULD NOT MATTER.
            if choice == "1": # View Profile
                self.view_profile()
            ### OTHER CHOICES TO BE IMPLEMENTED ###
            else:
                break

    ### TO BE IMPLEMENTED, WORK WITH THE LIBRARIAN MENU ###
    # def add_book(self):
    
    # def update_book(self):
    
    # def remove_book(self):
    
    # def generate_report(self):

## SLMS STARTING MENU ##
print("""-  Library Management System   -
      
    Please type the corresponding choice for what you would like to do:
    1. Signup
    2. Login
    3. Exit
    """)
# User signup/login
choice = input("Enter choice: ")
if choice == "1":
    User.signup()