from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import re
import datetime
from Model.book_model import Book
from View.noti_tab_view_1 import Message_2, Invalid

class BookEdit1App:
    def __init__(self, root, book_data=None, assets_path=None):
        # Initialize the main window
        self.root = root
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        
        # Store book data
        self.book_data = book_data
        print(f"Received book_data: {book_data}")  # Debug print
        
        # Set up asset paths
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBookManaEditBook1")

        # Create canvas
        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=605,
            width=898,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Store images as instance variables to prevent garbage collection
        self.images = {}
        self.entries = {}
        self.buttons = {}
        self.error_labels = {}  # For validation error messages
        
        # Valid categories
        self.valid_categories = [
            "Fiction", "Non-Fiction", "Mystery", "Science",
            "Fantasy", "History", "Romance", "Biography",
            "Thriller", "Technology"
        ]

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()
        self.create_entry_fields()
        
        # Populate fields if book data is provided
        if self.book_data:
            self.populate_fields()
            
        # Set up validation bindings
        self.setup_validation_bindings()

    def relative_to_assets(self, path):
        """Helper function to get the absolute path to assets"""
        return self.assets_path / Path(path)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, color):
        """Vẽ hình chữ nhật có bo góc."""
        # Bo góc trên bên trái
        self.canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, 
                               start=90, extent=90, fill=color, outline=color)
        # Bo góc trên bên phải
        self.canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, 
                               start=0, extent=90, fill=color, outline=color)
        # Bo góc dưới bên trái
        self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, 
                               start=180, extent=90, fill=color, outline=color)
        # Bo góc dưới bên phải
        self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, 
                               start=270, extent=90, fill=color, outline=color)

        # Phần thân của hình chữ nhật
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)

    def create_background(self):
        """Tạo nền chính với bo góc"""
        # Sidebar (không cần bo góc)
        self.canvas.create_rectangle(
            0.0, 0.0, 262.0, 605.0,
            fill="#0A66C2", outline=""
        )

        # Hình chữ nhật lớn nằm ngang (bo góc)
        self.create_rounded_rectangle(285.0, 47.0, 871.0, 558.0, radius=10, color="#F1F1F1")

    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Logo
        self.load_image("image_1", (131.0, 74.0))

        # Sidebar buttons
        self.create_button("btn_AddBook", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditBookInformation", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

    def create_main_panel(self):
        """Create the main panel elements"""
        # Load title and icons
        self.load_image("image_2", (577.0, 70.0))
        self.load_image("image_3", (336.0, 135.0))  # Title icon
        self.load_image("image_4", (345.0, 212.0))  # Author icon
        self.load_image("image_7", (380.0, 289.0))  # Published Year icon
        self.load_image("image_5", (354.0, 366.0))  # Category icon
        self.load_image("image_6", (352.0, 443.0))  # Quantity icon

        # Create save button
        self.create_button("btn_Confirm", (421.0, 498.0, 313.0, 48.0))

    def create_entry_fields(self):
        """Create the entry fields for book information"""
        # Title field
        self.create_entry_field("lnE_Title", (679.5, 136.0), (543.0, 112.0, 273.0, 46.0))
        
        # Author field
        self.create_entry_field("lnE_Author", (679.5, 213.0), (543.0, 189.0, 273.0, 46.0))
        
        # Published Year field
        self.create_entry_field("lnE_PublishedYear", (679.5, 290.0), (543.0, 266.0, 273.0, 46.0))
        
        # Category field
        self.create_entry_field("lnE_Category", (679.5, 367.0), (543.0, 343.0, 273.0, 46.0))
        
        # Quantity field
        self.create_entry_field("lnE_Quantity", (679.5, 444.0), (543.0, 420.0, 273.0, 46.0))
        
        # Create error message labels (initially hidden)
        self.create_error_label("error_title", (543.0, 158.0))
        self.create_error_label("error_author", (543.0, 235.0))
        self.create_error_label("error_published_year", (543.0, 312.0))
        self.create_error_label("error_category", (543.0, 389.0))
        self.create_error_label("error_quantity", (543.0, 466.0))

    def load_image(self, image_name, position):
        """Load an image and place it on the canvas"""
        self.images[image_name] = PhotoImage(
            file=self.relative_to_assets(f"{image_name}.png")
        )
        self.canvas.create_image(
            position[0], position[1],
            image=self.images[image_name]
        )

    def create_button(self, button_name, dimensions):
        """Create a button with the given name and dimensions"""
        self.images[button_name] = PhotoImage(
            file=self.relative_to_assets(f"{button_name}.png")
        )

        button = Button(
            image=self.images[button_name],
            borderwidth=0,
            highlightthickness=0,
            command=lambda b=button_name: self.button_click(b),
            relief="flat"
        )

        button.place(
            x=dimensions[0],
            y=dimensions[1],
            width=dimensions[2],
            height=dimensions[3]
        )

        # Store button widget in dictionary
        self.buttons[button_name] = button

    def create_entry_field(self, entry_name, bg_position, dimensions):
        """Create an entry field with background image"""
        # Create entry background image
        self.images[f"{entry_name}_bg"] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )
        self.canvas.create_image(
            bg_position[0], bg_position[1],
            image=self.images[f"{entry_name}_bg"]
        )

        # Create entry widget
        entry = Entry(
            bd=0,
            bg="#E7DCDC",
            fg="#000716",
            highlightthickness=0
        )

        entry.place(
            x=dimensions[0],
            y=dimensions[1],
            width=dimensions[2],
            height=dimensions[3]
        )

        # Store entry widget in dictionary
        self.entries[entry_name] = entry
        
        return entry
        
    def create_error_label(self, label_name, position):
        """Create an error message label (initially hidden)"""
        label = Text(
            self.root,
            bg="#F1F1F1",
            fg="red",
            font=("Arial", 8),
            height=1,
            width=30,
            bd=0,
            highlightthickness=0
        )
        
        label.place(
            x=position[0],
            y=position[1],
            width=273.0,
            height=20.0
        )
        
        # Initially hide the label
        label.insert("1.0", "")
        label.config(state="disabled")
        
        # Store label widget in dictionary
        self.error_labels[label_name] = label
        
    def show_error(self, label_name, message):
        """Show error message in the specified label"""
        label = self.error_labels[label_name]
        label.config(state="normal")
        label.delete("1.0", "end")
        label.insert("1.0", message)
        label.config(state="disabled")
        
    def clear_error(self, label_name):
        """Clear error message from the specified label"""
        label = self.error_labels[label_name]
        label.config(state="normal")
        label.delete("1.0", "end")
        label.config(state="disabled")

    def populate_fields(self):
        """Populate form fields with book data"""
        if not self.book_data:
            print("No book data to populate fields")
            return
        
        print(f"Populating fields with: {self.book_data}")  # Debug print
        
        # Set field values
        field_mapping = {
            "lnE_Title": self.book_data[1],
            "lnE_Author": self.book_data[2],
            "lnE_PublishedYear": str(self.book_data[3]),
            "lnE_Category": self.book_data[4],
            "lnE_Quantity": str(self.book_data[5])
        }
        
        for field_name, value in field_mapping.items():
            if field_name in self.entries:
                self.entries[field_name].delete(0, "end")
                self.entries[field_name].insert(0, value)
    
    def setup_validation_bindings(self):
        """Set up validation bindings for entry fields"""
        # Title validation
        if "lnE_Title" in self.entries:
            self.entries["lnE_Title"].bind("<FocusOut>", self.validate_title)
            
        # Author validation
        if "lnE_Author" in self.entries:
            self.entries["lnE_Author"].bind("<FocusOut>", self.validate_author)
            
        # Published Year validation
        if "lnE_PublishedYear" in self.entries:
            self.entries["lnE_PublishedYear"].bind("<FocusOut>", self.validate_published_year)
            
        # Category validation
        if "lnE_Category" in self.entries:
            self.entries["lnE_Category"].bind("<FocusOut>", self.validate_category)
            
        # Quantity validation
        if "lnE_Quantity" in self.entries:
            self.entries["lnE_Quantity"].bind("<FocusOut>", self.validate_quantity)
    
    def validate_title(self, event=None):
        """Validate title field"""
        title = self.entries["lnE_Title"].get().strip()
        
        if not title:
            self.show_error("error_title", "Title cannot be empty")
            return False
            
        if len(title) < 2:
            self.show_error("error_title", "Title must be at least 2 characters")
            return False
            
        if len(title) > 255:
            self.show_error("error_title", "Title must be at most 255 characters")
            return False
            
        # Clear error if validation passes
        self.clear_error("error_title")
        return True
        
    def validate_author(self, event=None):
        """Validate author field"""
        author = self.entries["lnE_Author"].get().strip()
        
        if not author:
            self.show_error("error_author", "Author cannot be empty")
            return False
            
        if len(author) < 2:
            self.show_error("error_author", "Author must be at least 2 characters")
            return False
            
        if len(author) > 100:
            self.show_error("error_author", "Author must be at most 100 characters")
            return False
            
        # Check for numbers
        if re.search(r'\d', author):
            self.show_error("error_author", "Author cannot contain numbers")
            return False
            
        # Check for allowed characters
        allowed_pattern = r'^[a-zA-Z\s\-\.,&]+$'
        if not re.match(allowed_pattern, author):
            self.show_error("error_author", "Only letters, spaces, -, ., ,, & allowed")
            return False
            
        # Check for consecutive special characters
        if re.search(r'[\-]{2,}|[\. ]{2,}|[,]{2,}|[&]{2,}', author):
            self.show_error("error_author", "Special chars cannot be consecutive")
            return False
            
        # Clear error if validation passes
        self.clear_error("error_author")
        return True
        
    def validate_published_year(self, event=None):
        """Validate published year field"""
        year = self.entries["lnE_PublishedYear"].get().strip()
        
        if not year:
            self.show_error("error_published_year", "Published Year cannot be empty")
            return False
            
        if not year.isdigit():
            self.show_error("error_published_year", "Published Year must be a number")
            return False
            
        year_int = int(year)
        current_year = datetime.datetime.now().year
        
        if year_int < 1440 or year_int > current_year:
            self.show_error("error_published_year", f"Year must be between 1440 and {current_year}")
            return False
            
        # Clear error if validation passes
        self.clear_error("error_published_year")
        return True
        
    def validate_category(self, event=None):
        """Validate category field"""
        category = self.entries["lnE_Category"].get().strip()
        
        if not category:
            self.show_error("error_category", "Category cannot be empty")
            return False
            
        if category not in self.valid_categories:
            self.show_error("error_category", f"Must be one of: {', '.join(self.valid_categories)}")
            return False
            
        # Clear error if validation passes
        self.clear_error("error_category")
        return True
        
    def validate_quantity(self, event=None):
        """Validate quantity field"""
        quantity = self.entries["lnE_Quantity"].get().strip()
        
        if not quantity:
            self.show_error("error_quantity", "Quantity cannot be empty")
            return False
            
        if not quantity.isdigit():
            self.show_error("error_quantity", "Quantity must be a positive number")
            return False
            
        if int(quantity) <= 0:
            self.show_error("error_quantity", "Quantity must be greater than zero")
            return False
            
        # Clear error if validation passes
        self.clear_error("error_quantity")
        return True
    
    def validate_all_fields(self):
        """Validate all fields before saving"""
        # Validate each field
        title_valid = self.validate_title()
        author_valid = self.validate_author()
        published_year_valid = self.validate_published_year()
        category_valid = self.validate_category()
        quantity_valid = self.validate_quantity()
        
        # Return True only if all validations pass
        return title_valid and author_valid and published_year_valid and category_valid and quantity_valid
    
    def format_author(self, author):
        """Format author name according to requirements"""
        # Remove extra spaces
        author = author.strip()
        author = re.sub(r'\s+', ' ', author)
        
        # Title case for first letter of each word
        words = author.split()
        formatted_author = ' '.join([word[0].upper() + word[1:].lower() if word else '' for word in words])
        
        return formatted_author
    
    def format_title(self, title):
        """Format title according to requirements"""
        # Remove extra spaces
        title = title.strip()
        title = re.sub(r'\s+', ' ', title)
        
        return title
        
    def update_book(self):
        """Validate input and update book in database."""
        # Get values from entry fields
        # For ISBN (readonly), we get it from book_data
        isbn = self.book_data[0] if self.book_data else ""
        
        # Get other values from entries
        title = self.entries['lnE_Title'].get().strip() if 'lnE_Title' in self.entries else ""
        author = self.entries['lnE_Author'].get().strip() if 'lnE_Author' in self.entries else ""
        published_year = self.entries['lnE_PublishedYear'].get().strip() if 'lnE_PublishedYear' in self.entries else ""
        category = self.entries['lnE_Category'].get().strip() if 'lnE_Category' in self.entries else ""
        quantity = self.entries['lnE_Quantity'].get().strip() if 'lnE_Quantity' in self.entries else ""
        
        # Validate fields one by one and focus on the first field with error
        
        # Title validation
        if not title or title.strip() == "":
            messagebox.showerror("Invalid Input", "Title cannot be empty.")
            self.entries['lnE_Title'].focus_set()
            return
        if len(title.strip()) < 2 or len(title.strip()) > 255:
            messagebox.showerror("Invalid Input", "Title must be between 2 and 255 characters.")
            self.entries['lnE_Title'].focus_set()
            return
        
        # Author validation
        if not author or author.strip() == "":
            messagebox.showerror("Invalid Input", "Author cannot be empty.")
            self.entries['lnE_Author'].focus_set()
            return
        if len(author.strip()) < 2 or len(author.strip()) > 100:
            messagebox.showerror("Invalid Input", "Author must be between 2 and 100 characters.")
            self.entries['lnE_Author'].focus_set()
            return
        
        # Check for numbers in author
        if re.search(r'\d', author):
            messagebox.showerror("Invalid Input", "Author name cannot contain numbers.")
            self.entries['lnE_Author'].focus_set()
            return
        
        # Check for allowed characters in author
        allowed_pattern = r'^[a-zA-Z\s\-\.,&]+$'
        if not re.match(allowed_pattern, author.strip()):
            messagebox.showerror("Invalid Input", "Author can only contain letters, spaces, hyphens, periods, commas, and ampersands.")
            self.entries['lnE_Author'].focus_set()
            return
        
        # Check for consecutive special characters
        if re.search(r'[\-]{2,}|[\. ]{2,}|[,]{2,}|[&]{2,}', author):
            messagebox.showerror("Invalid Input", "Special characters cannot appear consecutively.")
            self.entries['lnE_Author'].focus_set()
            return
        
        # Published year validation
        if not published_year or not published_year.isdigit():
            messagebox.showerror("Invalid Input", "Published Year must be a number.")
            self.entries['lnE_PublishedYear'].focus_set()
            return
        
        year_int = int(published_year)
        current_year = datetime.datetime.now().year
        if year_int < 1440 or year_int > current_year:
            messagebox.showerror("Invalid Input", f"Published Year must be between 1440 and {current_year}.")
            self.entries['lnE_PublishedYear'].focus_set()
            return
        
        # Category validation
        valid_categories = [
            "Fiction", "Non-Fiction", "Mystery", "Science",
            "Fantasy", "History", "Romance", "Biography",
            "Thriller", "Technology"
        ]
        
        if not category or category not in valid_categories:
            messagebox.showerror("Invalid Input", f"Category must be one of: {', '.join(valid_categories)}.")
            self.entries['lnE_Category'].focus_set()
            return
        
        # Quantity validation
        if not quantity or not quantity.isdigit():
            messagebox.showerror("Invalid Input", "Quantity must be a positive number.")
            self.entries['lnE_Quantity'].focus_set()
            return
        
        quantity_int = int(quantity)
        if quantity_int <= 0:
            messagebox.showerror("Invalid Input", "Quantity must be greater than zero.")
            self.entries['lnE_Quantity'].focus_set()
            return
        
        # Format author (title case for first letter of each word)
        words = author.strip().split()
        formatted_author = ' '.join([word[0].upper() + word[1:].lower() if word else '' for word in words])
        
        # Format title (remove extra spaces)
        formatted_title = re.sub(r'\s+', ' ', title.strip())
        
        # If all validations passed, create book data dictionary
        book_data = {
            'title': formatted_title,
            'author': formatted_author,
            'published_year': year_int,
            'category': category,
            'quantity': quantity_int
        }
        
        # Update book in database
        try:
            book = Book(book_id=isbn)
            success = book.update_book(book_data)
            
            if success:
                # Show success message using Message_2 from noti_tab_view_1
                Message_2(self.root, 'edit_book')  # Không cần import lại ở đây
            else:
                messagebox.showerror("Update Failed", "Failed to update book in database.")

            print(f"Error updating book: {str()}")
            messagebox.showerror("Update Failed", f"Error updating book: {str()}")
        except Exception as e:
            print(f"Error updating book: {str(e)}")
            messagebox.showerror("Update Failed", f"Error updating book: {str(e)}")
        # """Update book in database"""
        # if not self.validate_all_fields():
        #     return False
        
        # # Get ISBN from the stored book data
        # isbn = self.book_data[0]
            
        # # Get values from entry fields
        # title = self.format_title(self.entries["lnE_Title"].get())
        # author = self.format_author(self.entries["lnE_Author"].get())
        # published_year = int(self.entries["lnE_PublishedYear"].get().strip())
        # category = self.entries["lnE_Category"].get().strip()
        # quantity = int(self.entries["lnE_Quantity"].get().strip())
        
        # # Create book data dictionary
        # book_data = {
        #     'title': title,
        #     'author': author,
        #     'published_year': published_year,
        #     'category': category,
        #     'quantity': quantity
        # }
        
        # # Update book in database
        # try:
        #     book = Book(book_id=isbn)
        #     success = book.update_book(book_data)
            
        #     if success:
        #         # Show success message
        #         Message_2(self.root, 'edit_book')
        #         return True
        #     else:
        #         Invalid(self.root, 'Input')
        #         return False
        # except Exception as e:
        #     print(f"Error updating book: {str(e)}")
        #     Invalid(self.root, 'Input')
        #     return False

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")
        
        if button_name == "btn_Confirm":
            self.update_book()
        elif button_name == "btn_BackToHomepage":
            self.root.destroy()
            from View.Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root)
            homepage_root.mainloop()
        elif button_name == "btn_AddBook":
            self.root.destroy()
            from View.BookManagement.BookManaAddBook import BookManagementAddBookApp
            add_book_root = Tk()
            add_book = BookManagementAddBookApp(add_book_root)
            add_book_root.mainloop()
        elif button_name == "btn_EditBookInformation":
            self.root.destroy()
            from View.BookManagement.BookManaEditBook import BookManaEditBook
            edit_book_root = Tk()
            edit_book = BookManaEditBook(edit_book_root)
            edit_book_root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = BookEdit1App(root)
    root.mainloop()


# from pathlib import Path
# from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


# class BookManagementApp:
#     def __init__(self, root, assets_path=None):
#         # Initialize the main window
#         self.root = root
#         self.root.geometry("898x605")
#         self.root.configure(bg="#FFFFFF")
#         self.root.resizable(False, False)

#         # Set up asset paths
#         self.output_path = Path(__file__).parent
#         # Allow assets_path to be configurable
#         if assets_path:
#             self.assets_path = Path(assets_path)
#         else:
#             self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBookManaEditBook1")

#         # Create canvas
#         self.canvas = Canvas(
#             self.root,
#             bg="#FFFFFF",
#             height=605,
#             width=898,
#             bd=0,
#             highlightthickness=0,
#             relief="ridge"
#         )
#         self.canvas.place(x=0, y=0)

#         # Store images as instance variables to prevent garbage collection
#         self.images = {}
#         self.entries = {}
#         self.buttons = {}

#         # Build UI components
#         self.create_background()
#         self.create_sidebar()
#         self.create_main_panel()
#         self.create_entry_fields()

#     def relative_to_assets(self, path):
#         """Helper function to get the absolute path to assets"""
#         return self.assets_path / Path(path)

#     def create_rounded_rectangle(self, x1, y1, x2, y2, radius, color):
#         """Vẽ hình chữ nhật có bo góc."""
#         # Bo góc trên bên trái
#         self.canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, fill=color, outline=color)
#         # Bo góc trên bên phải
#         self.canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, fill=color, outline=color)
#         # Bo góc dưới bên trái
#         self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill=color,
#                                outline=color)
#         # Bo góc dưới bên phải
#         self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill=color,
#                                outline=color)

#         # Phần thân của hình chữ nhật
#         self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
#         self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)

#     def create_background(self):
#         """Tạo nền chính với bo góc"""
#         # Sidebar (không cần bo góc)
#         self.canvas.create_rectangle(
#             0.0, 0.0, 262.0, 605.0,
#             fill="#0A66C2", outline=""
#         )

#         # Hình chữ nhật lớn nằm ngang (bo góc)
#         self.create_rounded_rectangle(285.0, 47.0, 871.0, 558.0, radius=10, color="#F1F1F1")

#     def create_sidebar(self):
#         """Create the sidebar logo and buttons"""
#         # Logo
#         self.load_image("image_1", (131.0, 74.0))

#         # Sidebar buttons
#         self.create_button("btn_AddBook", (0.0, 181.0, 262.0, 25.0))
#         self.create_button("btn_EditBookInformation", (0.0, 219.0, 262.0, 25.0))
#         self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))

#     def create_main_panel(self):
#         """Create the main panel elements"""
#         # Load title and icons
#         self.load_image("image_2", (577.0, 70.0))
#         self.load_image("image_3", (336.0, 135.0))
#         self.load_image("image_4", (345.0, 212.0))
#         self.load_image("image_7", (380.0, 289.0))
#         self.load_image("image_5", (354.0, 366.0))
#         self.load_image("image_6", (352.0, 443.0))

#         # Create save button
#         self.create_button("btn_Confirm", (421.0, 498.0, 313.0, 48.0))

#     def create_entry_fields(self):
#         """Create the entry fields for book information"""
#         # First Entry (Title)
#         self.create_entry_field("lnE_Title", (679.5, 136.0), (543.0, 112.0, 273.0, 46.0))

#         # Second Entry (Author)
#         self.create_entry_field("lnE_Author", (679.5, 213.0), (543.0, 189.0, 273.0, 46.0))

#         # Third Entry (PublishedYear)
#         self.create_entry_field("lnE_PublishedYear", (679.5, 290.0), (543.0, 266.0, 273.0, 46.0))

#         # Fourth Entry (Category)
#         self.create_entry_field("lnE_Category", (679.5, 367.0), (543.0, 343.0, 273.0, 46.0))

#         # Fifth Entry (Quantity)
#         self.create_entry_field("lnE_Quantity", (679.5, 444.0), (543.0, 420.0, 273.0, 46.0))

#     def load_image(self, image_name, position):
#         """Load an image and place it on the canvas"""
#         self.images[image_name] = PhotoImage(
#             file=self.relative_to_assets(f"{image_name}.png")
#         )
#         self.canvas.create_image(
#             position[0],
#             position[1],
#             image=self.images[image_name]
#         )

#     def create_button(self, button_name, dimensions):
#         """Create a button with the given name and dimensions"""
#         self.images[button_name] = PhotoImage(
#             file=self.relative_to_assets(f"{button_name}.png")
#         )

#         button = Button(
#             image=self.images[button_name],
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda b=button_name: self.button_click(b),
#             relief="flat"
#         )

#         button.place(
#             x=dimensions[0],
#             y=dimensions[1],
#             width=dimensions[2],
#             height=dimensions[3]
#         )

#         # Store button widget in dictionary
#         self.buttons[button_name] = button

#     def create_entry_field(self, entry_name, bg_position, dimensions):
#         """Create an entry field with background image"""
#         # Create entry background image
#         self.images[f"{entry_name}_bg"] = PhotoImage(
#             file=self.relative_to_assets(f"{entry_name}.png")
#         )
#         self.canvas.create_image(
#             bg_position[0],
#             bg_position[1],
#             image=self.images[f"{entry_name}_bg"]
#         )

#         # Create entry widget
#         entry = Entry(
#             bd=0,
#             bg="#E7DCDC",
#             fg="#000716",
#             highlightthickness=0
#         )
#         entry.place(
#             x=dimensions[0],
#             y=dimensions[1],
#             width=dimensions[2],
#             height=dimensions[3]
#         )

#         # Store entry widget in dictionary
#         self.entries[entry_name] = entry

#     def button_click(self, button_name):
#         """Handle button click events"""
#         print(f"{button_name} clicked")

#     def run(self):
#         """Start the application main loop"""
#         self.root.mainloop()


# if __name__ == "__main__":
#     window = Tk()
#     app = BookManagementApp(window)
#     app.run()