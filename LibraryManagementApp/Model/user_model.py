from Database.db_lma import Database

class User:
    # Create a class-level database connection
    _db = None
    
    @classmethod
    def get_db(cls):
        if cls._db is None:
            cls._db = Database()
        return cls._db
    
    def __init__(self, user_id=None, name=None, username=None, email=None, password=None, date_of_birth=None, role="user"):
        self.user_id = user_id #Primary key
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.role = role
        self.db = self.get_db() # Connect to databse

    def save_user(self):
        try:
            if self.user_id is None:
                # Let SQLite auto-generate ID if none is provided
                self.db.cursor.execute("INSERT INTO Users (name, username, email, password, date_of_birth, role) VALUES (?, ?, ?, ?, ?, ?)", 
                                (self.name, self.username, self.email, self.password, self.date_of_birth, self.role))
                self.user_id = self.db.cursor.lastrowid
            else:
                # Use the provided user_id
                self.db.cursor.execute("INSERT INTO Users (user_id, name, username, email, password, date_of_birth, role) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                                (self.user_id, self.name, self.username, self.email, self.password, self.date_of_birth, self.role))
            
            self.db.conn.commit()
            return True
        except Exception as e:
            self.db.conn.rollback()  # Rollback on error
            print(f"Error saving user: {e}")
            return False
    
    @staticmethod
    def login(email, password): # Authenticate user login 
       db = Database()
       db.cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", (email, password))
       return db.cursor.fetchone()

    def change_pass(self, new_password): # Change user password
        self.db.cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (new_password, self.user_id))
        self.db.conn.commit()

    def edit_account_info(self, new_username, new_date_of_birth): # Edit user account info
        current_user = User.get_username(new_username)
        if current_user and current_user[0] != self.user_id:
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
        db.cursor.execute("SELECT * FROM Users WHERE username LIKE ?", (username,))
        return db.cursor.fetchone()
    
    @staticmethod
    def search_username_partial(partial_username): # Search users by partial username match
        db = Database()
        db.cursor.execute("SELECT * FROM Users WHERE username LIKE ?", (f"%{partial_username}%",))
        return db.cursor.fetchall()
    
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