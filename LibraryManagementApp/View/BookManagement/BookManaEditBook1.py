from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Model.book_model import Book
from View.noti_tab_view_1 import Message_2, Invalid
import re
import datetime

class BookEdit1App:
    def __init__(self, root, assets_path=None, book_data=None):
        # Initialize the main window
        self.root = root
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        #Store book data
        self.book_data = book_data

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
        self.buttons= {}

        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()
        self.create_entry_fields()

        # Populate fields with book data if provided
        if self.book_data:
            self.populate_fields()

    def relative_to_assets(self, path):
        """Helper function to get the absolute path to assets"""
        return self.assets_path / Path(path)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, color):
        """Vẽ hình chữ nhật có bo góc."""
        # Bo góc trên bên trái
        self.canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, fill=color, outline=color)
        # Bo góc trên bên phải
        self.canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, fill=color, outline=color)
        # Bo góc dưới bên trái
        self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill=color,
                               outline=color)
        # Bo góc dưới bên phải
        self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill=color,
                               outline=color)

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
        self.create_rounded_rectangle(291.0, 39.0, 877.0, 567.0, radius=10, color="#F1F1F1")

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
        self.load_image("image_2", (583.0, 69.0))
        self.load_image("image_3", (337.0, 124.0))
        self.load_image("image_4", (337.0, 192.0))
        self.load_image("image_5", (346.0, 260.0))
        self.load_image("image_8", (381.0, 328.0))
        self.load_image("image_6", (355.0, 396.0))
        self.load_image("image_7", (353.0, 464.0))

        # Create save button
        self.create_button("btn_Confirm", (425.0, 508.0, 313.0, 48.0))

        # Bind confirm button to update function
        if "btn_Confirm" in self.buttons:
            self.buttons["btn_Confirm"].config(command=self.update_book)

    def create_entry_fields(self):
        """Create the entry fields for book information"""
        # ISBN Entry
        self.create_entry_field("lnE_ISBN", (681.5, 124.0), (545.0, 100.0, 273.0, 46.0))

        # # Make ISBN entry read-only
        # if "lnE_ISBN" in self.entries:
        #     self.entries["lnE_ISBN"].config(state="readonly")

        # Title Entry
        self.create_entry_field("lnE_Title", (681.5, 192.0), (545.0, 168.0, 273.0, 46.0))

        # Author Entry
        self.create_entry_field("lnE_Author", (681.5, 260.0), (545.0, 236.0, 273.0, 46.0))

        # Year Entry
        self.create_entry_field("lnE_PublishedYear", (681.5, 328.0), (545.0, 304.0, 273.0, 46.0))

        # Category Entry
        self.create_entry_field("lnE_Category", (681.5, 396.0), (545.0, 372.0, 273.0, 46.0))

        # Quantity Entry
        self.create_entry_field("lnE_Quantity", (681.5, 464.0), (545.0, 440.0, 273.0, 46.0))

    def load_image(self, image_name, position):
        """Load an image and place it on the canvas"""
        self.images[image_name] = PhotoImage(
            file=self.relative_to_assets(f"{image_name}.png")
        )
        self.canvas.create_image(
            position[0],
            position[1],
            image=self.images[image_name]
        )

    def create_entry_field(self, entry_name, bg_position, dimensions):
        """Create an entry field with background image"""
        # Create entry background image
        self.images[entry_name] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )
        self.canvas.create_image(
            bg_position[0],
            bg_position[1],
            image=self.images[entry_name]
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
        
        # # Make ISBN field read-only if it's the ISBN field
        # if entry_name == "lnE_ISBN":
        #     entry.config(state="readonly")
        
        # Store entry widget in dictionary
        self.entries[entry_name] = entry

    def load_image(self, image_name, position):
        """Load an image and place it on the canvas"""
        self.images[image_name] = PhotoImage(
            file=self.relative_to_assets(f"{image_name}.png")
        )
        self.canvas.create_image(
            position[0],
            position[1],
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

        self.buttons[button_name] = button

    def create_entry_field(self, entry_name, bg_position, dimensions):
        """Create an entry field with background image"""
        # Create entry background image
        self.images[entry_name] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )
        self.canvas.create_image(
            bg_position[0],
            bg_position[1],
            image=self.images[entry_name]
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

    # def button_click(self, button_name):
    #     """Handle button click events"""
    #     print(f"{button_name} clicked")

    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")
        
        if button_name == "btn_BackToHomepage":
            self.root.destroy()
            from View.Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root)
            homepage_root.mainloop()
    
    def populate_fields(self):
        """Populate the edit form fields with book data."""
        if not self.book_data:
            return
            
        # Map book data to entry fields
        field_mapping = {
            # 'lnE_ISBN': str(self.book_data[0]),
            'lnE_Title': self.book_data[1],
            'lnE_Author': self.book_data[2],
            'lnE_PublishedYear': str(self.book_data[3]),
            'lnE_Category': self.book_data[4],
            'lnE_Quantity': str(self.book_data[5])
        }
        
        # Set values in entry fields
        for field_name, value in field_mapping.items():
            if field_name in self.entries:
                entry = self.entries[field_name]
                # Need to set state to normal for readonly fields to insert text
                if field_name == 'lnE_ISBN':
                    entry.config(state="normal")
                entry.delete(0, 'end')
                entry.insert(0, value)
                # # Set ISBN back to readonly
                # if field_name == 'lnE_ISBN':
                #     entry.config(state="readonly")
    
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
        
        # Validate all fields
        valid, message, book_data = self.validate_all_fields(
            isbn, title, author, published_year, category, quantity
        )
        
        if not valid:
            Invalid(self.root, 'Input')
            return
            
        # Update book in database
        try:
            book = Book(book_id=isbn)
            success = book.update_book(book_data)
            
            if success:
                # Show success message
                Message_2(self.root, 'edit_book')
            else:
                Invalid(self.root, 'Input')
        except Exception as e:
            print(f"Error updating book: {str(e)}")
            Invalid(self.root, 'Input')
    
    def validate_all_fields(self, isbn, title, author, published_year, category, quantity):
        """Validate all fields and return validation result."""
        # Valid categories list
        valid_categories = [
            "Fiction", "Non-Fiction", "Mystery", "Science",
            "Fantasy", "History", "Romance", "Biography",
            "Thriller", "Technology"
        ]
        
        # ISBN validation (read-only, shouldn't change)
        if not isbn or not str(isbn).isdigit() or len(str(isbn)) != 10:
            return False, "ISBN must be exactly 10 digits.", {}
        
        # Title validation
        if not title or title.strip() == "":
            return False, "Title cannot be empty.", {}
        if len(title.strip()) < 2 or len(title.strip()) > 255:
            return False, "Title must be between 2 and 255 characters.", {}
        
        # Format title (remove extra spaces)
        formatted_title = re.sub(r'\s+', ' ', title.strip())
        
        # Author validation
        if not author or author.strip() == "":
            return False, "Author cannot be empty.", {}
        if len(author.strip()) < 2 or len(author.strip()) > 100:
            return False, "Author must be between 2 and 100 characters.", {}
        
        # Check for numbers in author
        if re.search(r'\d', author):
            return False, "Author name cannot contain numbers.", {}
        
        # Check for allowed characters in author
        allowed_pattern = r'^[a-zA-Z\s\-\.,&]+$'
        if not re.match(allowed_pattern, author.strip()):
            return False, "Author can only contain letters, spaces, hyphens, periods, commas, and ampersands.", {}
        
        # Check for consecutive special characters
        if re.search(r'[\-]{2,}|[\. ]{2,}|[,]{2,}|[&]{2,}', author):
            return False, "Special characters cannot appear consecutively.", {}
        
        # Format author (title case for first letter of each word)
        words = author.strip().split()
        formatted_author = ' '.join([word[0].upper() + word[1:].lower() if word else '' for word in words])
        
        # Published year validation
        if not published_year or not published_year.isdigit():
            return False, "Published Year must be a number.", {}
        
        year_int = int(published_year)
        current_year = datetime.datetime.now().year
        if year_int < 1440 or year_int > current_year:
            return False, f"Published Year must be between 1440 and {current_year}.", {}
        
        # Category validation
        if not category or category not in valid_categories:
            return False, f"Category must be one of: {', '.join(valid_categories)}.", {}
        
        # Quantity validation
        if not quantity or not quantity.isdigit():
            return False, "Quantity must be a positive number.", {}
        
        quantity_int = int(quantity)
        if quantity_int <= 0:
            return False, "Quantity must be greater than zero.", {}
        
        # If all validations passed, create book data dictionary
        book_data = {
            'title': formatted_title,
            'author': formatted_author,
            'published_year': year_int,
            'category': category,
            'quantity': quantity_int
        }
        
        return True, "Book updated successfully!", book_data

    # def run(self):
    #     """Start the application main loop"""
    #     self.root.mainloop()

# For standalone testing
if __name__ == "__main__":
    window = Tk()
    app = BookEdit1App(window)
    app.run()