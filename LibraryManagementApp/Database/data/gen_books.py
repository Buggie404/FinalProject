import sqlite3
import random
import pandas as pd

connect = sqlite3.connect('LibraryManagementApp/Database/library.db')
cursor = connect.cursor()

df_path = "LibraryManagementApp/Database/data/books.csv"
df = pd.read_csv(df_path, delimiter = ";", encoding='ISO-8859-1', on_bad_lines='skip', low_memory=False, nrows=150)
df["ISBN"] = pd.to_numeric(df["ISBN"], errors='coerce')

categories = ["Fiction", "Non-Fiction", "Mystery", "Science", "Fantasy", "History", "Romance", "Biography", "Thriller", "Technology"]

books_data = []
for index, row in df.iterrows():
    book_id = row["ISBN"]
    title = row["Book-Title"]
    author = row["Book-Author"]
    published_year = row["Year-Of-Publication"]
    category = random.choice(categories)
    quantity = random.randint(1, 20)
    books_data.append((book_id, title, author, published_year, category, quantity))

cursor.executemany("INSERT OR IGNORE INTO Books VALUES (?, ?, ?, ?, ?, ?)", books_data)
connect.commit()