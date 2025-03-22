import sqlite3
import random
import pandas as pd
import os
import sys
import re
import csv

# Import the Database class from db_lma.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)
from Database.db_lma import Database

def is_english_text(text):
    """
    Check if the text is primarily in English by looking for non-ASCII characters.
    This is a simple heuristic and may not be perfect.
    """
    if not isinstance(text, str):
        return True  # Handle non-string values
    
    # Regular expression to match basic Latin characters, numbers, and common punctuation
    english_pattern = re.compile(r'^[a-zA-Z0-9\s\.,\-_\'\":;!?&()\[\]]*$')
    
    # Check if at least 90% of the text matches the pattern
    return english_pattern.match(text) is not None

def is_single_author(author):
    """
    Check if the author field represents a single person (no delimiters like /, &, and, etc.)
    """
    if not isinstance(author, str):
        return False
    
    # Check for common delimiters that indicate multiple authors
    delimiters = ['/', '&', ' and ', ',', ';']
    for delimiter in delimiters:
        if delimiter in author:
            return False
    
    # Additional check for patterns like "Author1 & Author2" or "Author1, Author2"
    if re.search(r'\b(with|et al|and)\b', author.lower()):
        return False
    
    return True

def update_books_table():
    # Initialize database connection using the Database class
    db = Database()
    
    if db.conn is None:
        return
    
    try:
        db.cursor.execute("DROP TABLE IF EXISTS Books")
        
        db.create_books_table()

        csv_path = os.path.join(current_dir, "test_books.csv")
        
        if not os.path.exists(csv_path):
            csv_path = os.path.join(parent_dir, "test_books.csv")
            if not os.path.exists(csv_path):
                # Try project root
                csv_path = os.path.join(project_root, "test_books.csv")
            if not os.path.exists(csv_path):
                print("Could not find test_books.csv automatically")
                custom_path = input("Please enter the full path to test_books.csv: ")
                if os.path.exists(custom_path):
                    csv_path = custom_path
                else:
                    db.close()
                    return
        
        try:
            df = pd.read_csv(csv_path, on_bad_lines='skip', quoting=csv.QUOTE_MINIMAL)
        except TypeError:
            df = pd.read_csv(csv_path, error_bad_lines=False, quoting=csv.QUOTE_MINIMAL)
        
        # Use ISBN-13 for book_id
        if 'isbn13' in df.columns:
            df.rename(columns={'isbn13': 'book_id'}, inplace=True)
        elif 'ISBN13' in df.columns:
            df.rename(columns={'ISBN13': 'book_id'}, inplace=True)
        elif 'ISBN' in df.columns:
            df.rename(columns={'ISBN': 'book_id'}, inplace=True)
        
        # Check if book_id column exists
        if 'book_id' not in df.columns:
            if 'goodreads_book_id' in df.columns:
                print("Using goodreads_book_id as book_id")
                df.rename(columns={'goodreads_book_id': 'book_id'}, inplace=True)
            else:
                print("Creating sequential book_id")
                df['book_id'] = [f"ID-{i+1:010d}" for i in range(len(df))]
        
        # Convert book_id to string and ensure it's valid
        df['book_id'] = df['book_id'].astype(str)
        # Clean book_id to ensure it's suitable as a primary key
        df['book_id'] = df['book_id'].apply(lambda x: re.sub(r'[^0-9a-zA-Z-]', '', str(x)))
        df['book_id'] = df['book_id'].apply(lambda x: f"ID-{random.randint(1000000000, 9999999999)}" if not x else x)
        
        # Handle title column
        if 'title' not in df.columns:
            if 'Book-Title' in df.columns:
                df.rename(columns={'Book-Title': 'title'}, inplace=True)
            elif 'book_title' in df.columns:
                df.rename(columns={'book_title': 'title'}, inplace=True)
            elif 'original_title' in df.columns:
                df.rename(columns={'original_title': 'title'}, inplace=True)
            else:
                # If no title column, use a placeholder
                df['title'] = "Unknown Title"
        
        # Handle author column
        if 'author' not in df.columns:
            if 'authors' in df.columns:
                df.rename(columns={'authors': 'author'}, inplace=True)
            elif 'Book-Author' in df.columns:
                df.rename(columns={'Book-Author': 'author'}, inplace=True)
            else:
                # If no author column, use a placeholder
                df['author'] = "Unknown Author"
        
        # Handle missing values in required columns
        df['title'] = df['title'].fillna("Unknown Title")
        df['author'] = df['author'].fillna("Unknown Author")
        
        # Extract published year from publication_date (if applicable)
        if 'published_year' not in df.columns:
            if 'publication_date' in df.columns:
                df['published_year'] = df['publication_date'].astype(str).str.extract(r'(\d{4})').fillna(0).astype(int)
            elif 'Year-Of-Publication' in df.columns:
                df['published_year'] = df['Year-Of-Publication']
            elif 'original_publication_year' in df.columns:
                df['published_year'] = df['original_publication_year']
            else:
                # If no publication year column, use a random year
                df['published_year'] = [random.randint(1900, 2023) for _ in range(len(df))]
        
        # Filter for English-only titles and authors
        print("Filtering for English-only titles and authors...")
        english_titles_mask = df['title'].apply(is_english_text)
        english_authors_mask = df['author'].apply(is_english_text)
        
        # Filter for single authors (no collaborations)
        print("Filtering for books with single authors (no collaborations)...")
        single_author_mask = df['author'].apply(is_single_author)
        
        # Apply all filters
        df = df[english_titles_mask & english_authors_mask & single_author_mask]
        
        print(f"After filtering: {len(df)} books with English titles and single authors")
        
        # Define book categories
        categories = ["Fiction", "Non-Fiction", "Mystery", "Science", "Fantasy", 
                      "History", "Romance", "Biography", "Thriller", "Technology"]
        
        # Remove duplicate book_ids (keep first occurrence)
        df = df.drop_duplicates(subset=['book_id'])
        
        # Limit to exactly 150 books
        max_books = 150
        if len(df) > max_books:
            df = df.head(max_books)
        else:
            pass
        
        # Prepare data for database insertion
        books_data = []
        for index, row in df.iterrows():
            book_id = row["book_id"]
            title = str(row["title"])[:255]  # Limit title length
            author = str(row["author"])[:255]  # Limit author length
            
            # Ensure published_year is an integer
            try:
                published_year = int(float(row["published_year"]))
                if published_year < 0 or published_year > 2024:
                    published_year = random.randint(1900, 2023)
            except (ValueError, TypeError):
                published_year = random.randint(1900, 2023)
                
            category = random.choice(categories)
            quantity = random.randint(1, 20)
            books_data.append((book_id, title, author, published_year, category, quantity))
        
        db.cursor.executemany("INSERT OR IGNORE INTO Books VALUES (?, ?, ?, ?, ?, ?)", books_data)
        db.conn.commit()
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the database connection
        db.close()

# Run the update function if executed directly
if __name__ == "__main__":
    update_books_table()