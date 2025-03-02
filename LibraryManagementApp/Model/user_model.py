from Database.db_lma import Database

class User:
    def __init__(self, user_id=None, name=None, username=None, email=None, password=None, date_of_birth=None, role="user"):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.date_of_birth = date_of_birth
        self.role = role
        self.db = Database() 
    
    def save_user(self):
        self.db.cursor.execute("INSERT INTO Users (name, username, email, password, date_of_birth, role) VALUES (?, ?, ?, ?, ?, ?)", 
                               (self.name, self.username, self.email, self.password, self.date_of_birth, self.role))
        self.db.conn.commit()
        self.user_id = self.db.cursor.lastrowid
    
    @staticmethod
    def login(email, password):
       db = Database()
       db.cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ? AND status = 'Activated'", (email, password))
       return db.cursor.fetchone()

    def change_pass(self, new_password):
        self.db.cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (new_password, self.user_id))
        self.db.conn.commit()

    def edit_account_info(self, new_username, new_date_of_birth):
        self.db.cursor.execute("UPDATE Users SET username = ?, date_of_birth = ? WHERE user_id = ?", (new_username, new_date_of_birth, self.user_id))
        self.db.conn.commit()

    @staticmethod
    def get_id(user_id):
        db = Database()
        db.cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        return db.cursor.fetchone()
    
    @staticmethod
    def get_username(username):
        db = Database()
        db.cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        return db.cursor.fetchone()
    
    @staticmethod
    def get_name(name):
        db = Database()
        db.cursor.execute("SELECT * FROM Users WHERE name = ?", (name,))
        return db.cursor.fetchone()
    
    @staticmethod
    def get_all_user():
        db = Database()
        db.cursor.execute("SELECT * FROM Users")
        return db.cursor.fetchall()




        