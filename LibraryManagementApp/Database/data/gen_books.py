import sqlite3
import random
import pandas as pd
import re
import os
import sys

# Import the Database class from db_lma.py
# Adjust the import path as needed based on your project structure
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the View directory
parent_dir = os.path.dirname(current_dir)
# Go up one more level to the project root directory
project_root = os.path.dirname(parent_dir)
# Add project root to sys.path
sys.path.append(project_root)
from Database.db_lma import Database

def format_isbn(isbn_val):
    """Format ISBN to 10 digits with leading zeros"""
    # If ISBN is not a number, return None
    if pd.isna(isbn_val):
        return None
    
    # Convert to string and remove any non-digit characters
    isbn_str = str(isbn_val)
    digits_only = re.sub(r'[^0-9]', '', isbn_str)
    
    # If no digits left, return None
    if not digits_only:
        return None
    
    # Handle ISBNs of different lengths
    if len(digits_only) > 10:
        # If longer than 10, take the last 10 digits
        return digits_only[-10:]
    elif len(digits_only) < 10:
        # If shorter than 10, pad with zeros at the beginning
        return digits_only.zfill(10)
    else:
        # Already 10 digits
        return digits_only

def generate_books():
    # Initialize database connection using our Database class
    db = Database()
    
    # Convert ISBN column to TEXT type if needed
    db.convert_isbn_to_text()
    
    # Clear existing books from the database
    db.clear_books_table()
    
    # Load book data from CSV
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the View directory
    parent_dir = os.path.dirname(current_dir)
    # Go up one more level to the project root directory
    project_root = os.path.dirname(parent_dir)
    # Add project root to sys.path
    sys.path.append(project_root)
    df_path = "LibraryManagementApp/Database/data/books.csv"
    
    if not os.path.exists(df_path):
        print(f"CSV file not found at: {df_path}")
        db.close()
        return
    
    print(f"📖 Loading books from CSV: {df_path}")
    df = pd.read_csv(df_path, delimiter=";", encoding='ISO-8859-1', on_bad_lines='skip', low_memory=False, nrows=150)
    
    # Apply the ISBN formatting function
    df["ISBN"] = df["ISBN"].apply(format_isbn)
    
    # Ensure ISBN is treated as string, not a number
    df["ISBN"] = df["ISBN"].astype(str)
    
    # Remove rows with invalid ISBNs
    df = df.dropna(subset=["ISBN"])
    
    # Define book categories
    categories = ["Fiction", "Non-Fiction", "Mystery", "Science", "Fantasy", "History", "Romance", "Biography", "Thriller", "Technology"]
    
    # Prepare data for database insertion
    books_data = []
    for index, row in df.iterrows():
        book_id = row["ISBN"]
        title = row["Book-Title"]
        author = row["Book-Author"]
        published_year = row["Year-Of-Publication"]
        category = random.choice(categories)
        quantity = random.randint(1, 20)
        books_data.append((book_id, title, author, published_year, category, quantity))
    
    # Insert data into the database
    try:
        db.cursor.executemany("INSERT OR IGNORE INTO Books VALUES (?, ?, ?, ?, ?, ?)", books_data)
        db.conn.commit()
        print(f"Inserted {len(books_data)} books with properly formatted 10-digit ISBNs")
    except sqlite3.Error as e:
        print(f"Error inserting books: {e}")
    
    # Close the database connection
    db.close()

# Run the generator if executed directly
if __name__ == "__main__":
    generate_books()