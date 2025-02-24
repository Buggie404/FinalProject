# models/admin.py - Quản lý Admin
from user_model import User
class Admin(User):
    def __init__(self, user_id, name, username, email, password, date_of_birth, role="admin"):
        super().__init__(user_id, name, username, email, password, date_of_birth, role)
        

    def add_user(self, user_list, new_user):
        pass
    
    def reset_password(self, user, new_password):
        pass
      
    def delete_user(self, user_list, user):
        pass
    
    def add_book(self, book_list, book):
        pass
    
    def edit_book(self, book, new_data):
        pass
       
    def delete_book(self, book_list, book):
        pass
       
