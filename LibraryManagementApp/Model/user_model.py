from Database.db_lma import Database

class User:
    def __init__(self, user_id=None, name=None, username=None, email=None, password=None, date_of_birth=None, role="user"):
        self.user_id = user_id #Primary key
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.role = role
        self.db = Database() # Connect to databse
    
    def save_user(self): #To save new user to database
        self.db.cursor.execute("INSERT INTO Users (name, username, email, password, date_of_birth, role) VALUES (?, ?, ?, ?, ?, ?)", 
                               (self.name, self.username, self.email, self.password, self.date_of_birth, self.role))
        self.db.conn.commit()
        self.user_id = self.db.cursor.lastrowid # Get the last inserted id
    
    @staticmethod
    def login(email, password): # Authenticate user login 
       db = Database()
       db.cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email, password))
       return db.cursor.fetchone()

    def change_pass(self, new_password): # Change user password
        self.db.cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (new_password, self.user_id))
        self.db.conn.commit()

    def edit_account_info(self, new_username, new_date_of_birth): # Edit user account info
        if User.get_username(new_username):
            return False  # Username already taken
        self.db.cursor.execute("UPDATE Users SET username = ?, date_of_birth = ? WHERE user_id = ?", (new_username, new_date_of_birth, self.user_id))
        self.db.conn.commit()
        return True

    @staticmethod
    def get_id(user_id): # Search user by id
        db = Database()
        db.cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        return db.cursor.fetchone()
    
    @staticmethod
    def get_username(username): # Search user by username
        db = Database()
        db.cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        return db.cursor.fetchone()
    
    @staticmethod
    def get_name(name): # Search user by name
        db = Database()
        db.cursor.execute("SELECT * FROM Users WHERE name = ?", (name,))
        return db.cursor.fetchone()
    
    @staticmethod
    def get_all_user(): # Get all users
        db = Database()
        db.cursor.execute("SELECT * FROM Users")
        return db.cursor.fetchall()

    @staticmethod
    def get_user_by_email(email): # Search user by email
        db = Database()
        db.cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        return db.cursor.fetchone()   