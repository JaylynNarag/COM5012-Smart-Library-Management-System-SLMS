from abc import ABC, abstractmethod # Abstraction
import sqlite3 # 2 simple DBs made for this project, library & user
# Potentially add AES encryption? Make class on its own?

def setup_databases():
    # User DB - User details for signup/login
    connect_users = sqlite3.connect('users.db')
    conn_users = connect_users.cursor()
    conn_users.execute("CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY AUTOINCREMENT, fullname TEXT, dob DATE, phone_num TEXT, email_address TEXT, password TEXT, user_type TEXT)")
    connect_users.commit()
    connect_users.close()

    # Library DB - Actual library holding book info, item_id acts as accession number(?)
    connect_library = sqlite3.connect('library.db')
    conn_library = connect_library.cursor()
    conn_library.execute("CREATE TABLE IF NOT EXISTS items(item_id INT PRIMARY KEY, ISBN TEXT, author DATE, publisher TEXT, publication_date INT, edition TEXT, language TEXT, genre TEXT)")
    conn_library.execute("CREATE TABLE IF NOT EXISTS requests(request_id INTEGER PRIMARY KEY AUTOINCREMENT, member_id INT, book_id INT, request_type TEXT, status TEXT)")
    connect_library.commit()
    connect_library.close()

setup_databases() # Creates DBs & tables

# User class - parent class for member/librarian/admin
class User(ABC): # Abstraction - will use for abstract method to view profile (diff. behaviour for different obj.s made)
    def __init__(self, user_id, fullname, dob, phone_num, email_address, password, user_type):
        self.user_id = user_id
        self.fullname = fullname
        self.dob = dob
        self.phone_num = phone_num
        self.email_address = email_address
        self.password = password
        self.user_type = user_type
    
    def signup(self): # ADD TRY EXCEPTS HERE FOR USER LOGIN DETAILS MEETING CONSTRAINTS
        conn_signupuser = sqlite3.connect('users.db') # to insert the details into the user table
        curs_signup_user = conn_signupuser.cursor()
        curs_signup_user.execute("INSERT INTO users (user_id, fullname, dob, phone_num, email_address, password, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)", (self.user_id, self.fullname, self.dob, self.phone_num, self.email_address, self.password, self.user_type))
        conn_signupuser.commit()
        conn_signupuser.close()
        print("Signup successful.") # ADD SMTH HERE LIKE 'Press any key to go back to login menu'(?)
    
    def login(self, emailaddress, password): # Emailaddress & password parameters to be entered & checked against DB
        conn_loginuser = sqlite3.connect('users.db')
        curs_login_user = conn_loginuser.cursor()
        curs_login_user.execute("SELECT * FROM users WHERE email_address = ? AND password = ?", (emailaddress, password))
        user_details = curs_login_user.fetchone() # Retrieves line where details are in the system
        conn_loginuser.close()

        if user_details != None:
            user_type = user_details[6] #gets user_type from the details fetched from the db
            if user_type == "Member":
            elif user_type == "Librarian":
            elif user_type == "Administrator":
        else:
            print("Invalid login credentials! Please try again.") # ADD SMTH TO GET USER TO TRY AGAIN, LOOP HERE?
            return None
    
    # Abstract method: view profile method to be defined in respective child classes (return the necessary user details to be seen)
    @abstractmethod
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















print("""-  Library Management System   -
      
    Please type the corresponding choice for what user you are:
    1. Member
    2. Librarian
    3. Administrator
    4. Exit
    """)

# User signup/login
choice = input("Enter choice: ")
if choice == "1":
    print("""-  Member Signup   -""")