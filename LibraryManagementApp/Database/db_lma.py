import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('LibraryManagementApp/Database/library.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""create table Books (
                book_id integer primary key autoincrement,
                title text not null,
                author text not null,
                published_year integer check (published_year > 0),
                category text not null,
                quantity integer not null
                check (quantity >= 0) default 0
        )""")

        self.cursor.execute("""create table Users (
                user_id integer primary key autoincrement,
                name text not null,
                username text not null unique,
                email text not null unique,
                password text not null,
                date_of_birth date not null,
                role text not null
                check (role in ('User', 'Admin')) default 'User'
        )""")

        self.cursor.execute("""create table Receipts (
                receipt_id integer primary key autoincrement,
                user_id integer not null,
                book_id integer not null,
                borrow_date date not null,
                return_date date,
                status text not null
                check (status in ('Borrowed', 'Returned', 'Overdue')) default 'Borrowed',
                foreign key (user_id) references Users(user_id) on delete cascade,
                foreign key (book_id) references Books(book_id) on delete cascade
        )""")

        self.conn.commit()
    
    def close(self):
        self.conn.close()