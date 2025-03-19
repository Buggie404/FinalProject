""" To handle  Validation """
# Import fetched data from Admin Model
from Model.admin_model import Admin
from Model.user_model import User
from View.UserManagement import UserManagement

class Search_users:
    def __init__(self):
        pass

    @staticmethod
    def search_by_id(user_id):
        if not user_id:
            return False, "There are no matching IDs!"

        user = User.get_id(user_id)
        if user:
            return True, user
        return False, "There are no matching IDs!"

    @staticmethod
    def search_by_username(username):
        if not username:
            return False, "There are no matching usernames!"

        user = User.get_username(username)
        if user:
            return True, user
        return False, "There are no matching usernames!"