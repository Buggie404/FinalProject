from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import sys
import os
import re
import datetime

class BookEdit1App:
    def __init__(self, root, book_data=None, assets_path=None):
        # Initialize the main window
        self.root = root
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        
        # Store the book data
        self.book_data = book_data
        print(f"Book data received: {book_data}")
        
        # Set up asset paths
        self.output_path = Path(__file__).parent
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

        # Store images and UI elements
        self.images = {}
        self.entries = {}
        self.buttons = {}
        
        # Track validation errors
        self.field_errors = {
            'title': False,
            'author': False,
            'published_year': False,
            'category': False,
            'quantity': False
        }

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()
        self.create_entry_fields()
        
        # Fill entry fields with book data
        if self.book_data:
            self.populate_fields()
            
        # Setup field validation events
        self.setup_field_events()

    def relative_to_assets(self, path):
        """Helper function to get the absolute path to assets"""
        return self.assets_path / Path(path)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, color):
        """Draw a rectangle with rounded corners."""
        # Top left corner
        self.canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, 
                              start=90, extent=90, fill=color, outline=color)
        # Top right corner
        self.canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, 
                              start=0, extent=90, fill=color, outline=color)
        # Bottom left corner
        self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, 
                              start=180, extent=90, fill=color, outline=color)
        # Bottom right corner
        self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, 
                              start=270, extent=90, fill=color, outline=color)

        # Rectangle body
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)

    def create_background(self):
        """Create the main background with rounded corners"""
        # Sidebar (no rounded corners needed)
        self.canvas.create_rectangle(
            0.0, 0.0, 262.0, 605.0,
            fill="#0A66C2", outline=""
        )

        # Large horizontal rectangle (with rounded corners)
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

        # Create save button - using a custom method to ensure it's properly connected
        self.create_confirm_button()

    def create_confirm_button(self):
        """Create the confirm button with direct binding to update_book"""
        button_name = "btn_Confirm"
        dimensions = (421.0, 498.0, 313.0, 48.0)
        
        self.images[button_name] = PhotoImage(
            file=self.relative_to_assets(f"{button_name}.png")
        )

        # Create button with direct binding to update_book method
        button = Button(
            image=self.images[button_name],
            borderwidth=0,
            highlightthickness=0,
            command=self.update_book,  # Direct binding here
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
        print("Confirm button created with direct binding to update_book")

    def create_entry_fields(self):
        """Create the entry fields for book information"""
        # Title Entry
        self.create_entry_field("lnE_Title", (679.5, 136.0), (543.0, 112.0, 273.0, 46.0))
        
        # Author Entry
        self.create_entry_field("lnE_Author", (679.5, 213.0), (543.0, 189.0, 273.0, 46.0))
        
        # Published Year Entry
        self.create_entry_field("lnE_PublishedYear", (679.5, 290.0), (543.0, 266.0, 273.0, 46.0))
        
        # Category Entry
        self.create_entry_field("lnE_Category", (679.5, 367.0), (543.0, 343.0, 273.0, 46.0))
        
        # Quantity Entry
        self.create_entry_field("lnE_Quantity", (679.5, 444.0), (543.0, 420.0, 273.0, 46.0))

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
        
        # Add validation flag attribute
        entry._shown_warning = False

    def populate_fields(self):
        """Fill entry fields with book data"""
        if not self.book_data:
            return
            
        # Set values in entry fields
        self.entries["lnE_Title"].insert(0, self.book_data[1])
        self.entries["lnE_Author"].insert(0, self.book_data[2])
        self.entries["lnE_PublishedYear"].insert(0, str(self.book_data[3]))
        self.entries["lnE_Category"].insert(0, self.book_data[4])
        self.entries["lnE_Quantity"].insert(0, str(self.book_data[5]))

    def setup_field_events(self):
        """Set up validation events for entry fields"""
        # Bind validation to FocusOut events
        self.entries["lnE_Title"].bind("<FocusOut>", self.validate_title)
        self.entries["lnE_Author"].bind("<FocusOut>", self.validate_author)
        self.entries["lnE_PublishedYear"].bind("<FocusOut>", self.validate_published_year)
        self.entries["lnE_Category"].bind("<FocusOut>", self.validate_category)
        self.entries["lnE_Quantity"].bind("<FocusOut>", self.validate_quantity)
        
        # Reset warning flag on key release
        for field in self.entries.values():
            field.bind("<KeyRelease>", self.reset_warning_flag)

    def reset_warning_flag(self, event):
        """Reset the warning flag when field content changes"""
        event.widget._shown_warning = False

    def validate_title(self, event):
        """Validate title field"""
        title = self.entries["lnE_Title"].get().strip()
        
        # Check if empty
        if not title:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Title", "Title cannot be empty.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Title"].focus_set())
            self.field_errors['title'] = True
            return False
            
        # Check length
        if len(title) < 2 or len(title) > 255:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Title", "Title must be between 2 and 255 characters.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Title"].focus_set())
            self.field_errors['title'] = True
            return False
            
        # Standardize spaces
        standardized_title = re.sub(r'\s+', ' ', title)
        self.entries["lnE_Title"].delete(0, 'end')
        self.entries["lnE_Title"].insert(0, standardized_title)
        
        self.field_errors['title'] = False
        return True

    def validate_author(self, event):
        """Validate author field"""
        author = self.entries["lnE_Author"].get().strip()
        
        # Check if empty
        if not author:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", "Author cannot be empty.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Author"].focus_set())
            self.field_errors['author'] = True
            return False
            
        # Check length
        if len(author) < 2 or len(author) > 100:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", "Author must be between 2 and 100 characters.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Author"].focus_set())
            self.field_errors['author'] = True
            return False
            
        # Check for numbers
        if re.search(r'\d', author):
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", "Author name cannot contain numbers.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Author"].focus_set())
            self.field_errors['author'] = True
            return False
            
        # Check for allowed characters
        if not re.match(r'^[a-zA-ZÀ-ỹ\s\-\.,&]+$', author):
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", 
                                      "Only letters, spaces, hyphens (-), periods (.), commas (,), and ampersands (&) are allowed.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Author"].focus_set())
            self.field_errors['author'] = True
            return False
            
        # Check for consecutive special characters
        if re.search(r'[\-]{2,}|[\. ]{2,}|[,]{2,}|[&]{2,}', author):
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Author", 
                                      "Special characters (., -, comma, &) cannot appear consecutively.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Author"].focus_set())
            self.field_errors['author'] = True
            return False
            
        # Format author name to title case with special handling
        formatted_author = self.format_author_name(author)
        self.entries["lnE_Author"].delete(0, 'end')
        self.entries["lnE_Author"].insert(0, formatted_author)
        
        self.field_errors['author'] = False
        return True
        
    def format_author_name(self, author):
        """Format author name with proper capitalization"""
        # Split by spaces
        words = author.split()
        result = []

        for word in words:
            # If word contains special characters like period or hyphen
            if '.' in word or '-' in word or ',' in word or '&' in word:
                # Split by special characters and keep them
                parts = []
                current = ""
                for char in word:
                    if char in '.-,&':
                        if current:
                            parts.append(current)
                        current = ""
                        parts.append(char)
                    else:
                        current += char
                if current:
                    parts.append(current)

                # Process each part
                processed_parts = []
                for i, part in enumerate(parts):
                    if part in '.-,&':
                        processed_parts.append(part)
                    elif i == 0 or parts[i-1] in '.-':
                        # Capitalize if it's the first part or follows a period or hyphen
                        processed_parts.append(part[0].upper() + part[1:].lower() if part else "")
                    else:
                        # Otherwise lowercase
                        processed_parts.append(part.lower())

                result.append(''.join(processed_parts))
            else:
                # Regular word - capitalize first letter
                result.append(word[0].upper() + word[1:].lower() if word else "")

        # Join with spaces and standardize multiple spaces
        formatted_author = ' '.join(result)
        return re.sub(r'\s+', ' ', formatted_author)

    def validate_published_year(self, event):
        """Validate published year field"""
        year = self.entries["lnE_PublishedYear"].get().strip()
        
        # Check if empty
        if not year:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Year", "Published Year cannot be empty.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_PublishedYear"].focus_set())
            self.field_errors['published_year'] = True
            return False
            
        # Check if it's a number
        if not year.isdigit():
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Year", "Published Year must be a number.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_PublishedYear"].focus_set())
            self.field_errors['published_year'] = True
            return False
            
        # Check range
        year_int = int(year)
        current_year = datetime.datetime.now().year
        
        if year_int < 1440 or year_int > current_year:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Year", 
                                      f"Published Year must be between 1440 and {current_year}.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_PublishedYear"].focus_set())
            self.field_errors['published_year'] = True
            return False
            
        self.field_errors['published_year'] = False
        return True

    def validate_category(self, event):
        """Validate category field"""
        category = self.entries["lnE_Category"].get().strip()
        
        # Check if empty
        if not category:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Category", "Category cannot be empty.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Category"].focus_set())
            self.field_errors['category'] = True
            return False
            
        # Valid categories list
        valid_categories = [
            "Fiction", "Non-Fiction", "Mystery", "Science", 
            "Fantasy", "History", "Romance", "Biography", 
            "Thriller", "Technology"
        ]
        
        # Check if category is valid
        if category not in valid_categories:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Category", 
                                      f"Category must be one of: {', '.join(valid_categories)}.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Category"].focus_set())
            self.field_errors['category'] = True
            return False
            
        self.field_errors['category'] = False
        return True

    def validate_quantity(self, event):
        """Validate quantity field"""
        quantity = self.entries["lnE_Quantity"].get().strip()
        
        # Check if empty
        if not quantity:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Quantity", "Quantity cannot be empty.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Quantity"].focus_set())
            self.field_errors['quantity'] = True
            return False
            
        # Check if it's a number
        if not quantity.isdigit():
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Quantity", "Quantity must be a positive integer.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Quantity"].focus_set())
            self.field_errors['quantity'] = True
            return False
            
        # Check if it's positive
        quantity_int = int(quantity)
        if quantity_int <= 0:
            if not event.widget._shown_warning:
                messagebox.showwarning("Invalid Quantity", "Quantity must be greater than zero.")
                event.widget._shown_warning = True
                self.root.after(100, lambda: self.entries["lnE_Quantity"].focus_set())
            self.field_errors['quantity'] = True
            return False
            
        self.field_errors['quantity'] = False
        return True

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")
        
        if button_name == "btn_BackToHomepage":
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

    def update_book(self):
        """Validate all fields and update book in database"""
        print("Update book method called!")
        
        # Create dummy event objects for validation
        dummy_event = lambda widget: type('obj', (object,), {'widget': widget, '_shown_warning': False})
        
        # Force validation on all fields
        title_valid = self.validate_title(dummy_event(self.entries["lnE_Title"]))
        author_valid = self.validate_author(dummy_event(self.entries["lnE_Author"]))
        year_valid = self.validate_published_year(dummy_event(self.entries["lnE_PublishedYear"]))
        category_valid = self.validate_category(dummy_event(self.entries["lnE_Category"]))
        quantity_valid = self.validate_quantity(dummy_event(self.entries["lnE_Quantity"]))
        
        print(f"Validation results: title={title_valid}, author={author_valid}, year={year_valid}, category={category_valid}, quantity={quantity_valid}")
        
        # Check if any validation failed
        if not all([title_valid, author_valid, year_valid, category_valid, quantity_valid]):
            # Focus on the first field with an error
            for field_name, is_error in self.field_errors.items():
                if is_error:
                    field_map = {
                        'title': 'lnE_Title',
                        'author': 'lnE_Author',
                        'published_year': 'lnE_PublishedYear',
                        'category': 'lnE_Category',
                        'quantity': 'lnE_Quantity'
                    }
                    self.entries[field_map[field_name]].focus_set()
                    return
            return
            
        # Collect book data
        book_id = self.book_data[0]  # Original ISBN/book_id (unchanged)
        title = self.entries["lnE_Title"].get().strip()
        author = self.entries["lnE_Author"].get().strip()
        published_year = int(self.entries["lnE_PublishedYear"].get().strip())
        category = self.entries["lnE_Category"].get().strip()
        quantity = int(self.entries["lnE_Quantity"].get().strip())
        
        print(f"Updating book: ID={book_id}, title={title}, author={author}, year={published_year}, category={category}, quantity={quantity}")
        
        # Create updated book data dictionary
        updated_data = {
            'title': title,
            'author': author,
            'published_year': published_year,
            'category': category,
            'quantity': quantity
        }
        
        # Update the book in the database
        try:
            # Import Book model
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            grandparent_dir = os.path.dirname(parent_dir)
            
            # Add possible paths to sys.path
            possible_paths = [
                grandparent_dir,
                os.path.join(grandparent_dir, "LibraryManagementApp"),
                parent_dir,
                current_dir
            ]
            
            for path in possible_paths:
                if path not in sys.path:
                    sys.path.append(path)
                    
            from Model.book_model import Book
            
            # Create a Book object with the book_id
            book = Book(book_id=book_id)
            
            # Update the book with the new data
            success = book.update_book(updated_data)
            
            print(f"Database update result: {success}")
            
            if success:
                # Show success message using Message_2
                from View.noti_tab_view_1 import Message_2
                Message_2(self.root, 'edit_book')
            else:
                messagebox.showerror("Update Failed", "Failed to update book information.")
                
        except Exception as e:
            print(f"Error updating book: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Update Error", f"An error occurred: {str(e)}")

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

if __name__ == "__main__":
    window = Tk()
    app = BookEdit1App(window)
    app.run()
