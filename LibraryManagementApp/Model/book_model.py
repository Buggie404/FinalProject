#import database

class Book:
    def __init__(self, title=None, author=None, category=None, published_year=None, quantity=None):
        self.title = title
        self.author = author
        self.category = category
        self.pulished_year = published_year
        self.quantity = quantity
        # self.db = Database()
    def save(self):
        pass

    def get_book_by_id(book_id):
        pass

    def get_book_by_title(title):
        pass
 


