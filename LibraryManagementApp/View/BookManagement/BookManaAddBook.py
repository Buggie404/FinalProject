import os
import sys
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox

# Get the absolute path to the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to reach the project root
# If BookManaAddBook.py is in View/BookManagement, this goes up to the project root
project_root = os.path.dirname(os.path.dirname(current_dir))

# Add the project root to the Python path
sys.path.append(project_root)

# Now import from the Controller module
from Controller.book_management_controller import add_book

class BookManagementAddBookApp:
    def __init__(self, root, assets_path=None):
        # Initialize the main window
        self.root = root
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        # Set font that supports Vietnamese characters
        self.vietnamese_font = ("Arial Unicode MS", 10)  # or another Unicode font
        # Set up asset paths
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBookManaAddBook")
       
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
       
        # Store images and UI elements as instance variables
        self.images = {}
        self.buttons = {}
        self.entries = {}
       
        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()
        self.create_form_elements()
        self.create_action_buttons()
       
        # Initialize placeholders
        self.setup_field_placeholders()
       
        # Initialize warning flags
        for field in ["lnE_ISBN", "lnE_Title", "lnE_Author", "lnE_PublishedYear", "lnE_Category", "lnE_Quantity"]:
            self.entries[field]._shown_warning = False
   
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
        self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill=color, outline=color)
        # Bo góc dưới bên phải
        self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill=color, outline=color)
       
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
        self.create_rounded_rectangle(285.0, 39.0, 875.0, 567.0, radius=10, color="#F1F1F1")
   
    def create_sidebar(self):
        """Create the sidebar logo and buttons"""
        # Load and place logo
        self.load_image("image_1", (131.0, 74.0))
       
        # Create sidebar buttons
        self.create_button("btn_AddBook", (0.0, 181.0, 262.0, 25.0))
        self.create_button("btn_EditBookInformation", (0.0, 219.0, 262.0, 25.0))
        self.create_button("btn_BackToHomepage", (0.0, 563.0, 261.0, 25.0))
   
    def create_main_panel(self):
        """Create the main panel header"""
        # Load header image
        self.load_image("image_2", (581.0, 69.0))
   
    def create_form_elements(self):
        """Create form labels and entry fields"""
        # Labels for the form fields
        label_positions = [
            ("image_3", (335.0, 124.0)),  # ISBN
            ("image_4", (335.0, 192.0)),  # Title
            ("image_5", (344.0, 260.0)),  # Author
            ("image_8", (379.0, 328.0)),  # Published year
            ("image_6", (353.0, 396.0)),  # Category
            ("image_7", (351.0, 464.0))  # Quantity
        ]
       
        for label_name, position in label_positions:
            self.load_image(label_name, position)
       
        # Entry fields
        entry_fields = [
            ("lnE_ISBN", (679.5, 124.0), (543.0, 100.0, 273.0, 46.0)),  # ISBN
            ("lnE_Title", (679.5, 192.0), (543.0, 168.0, 273.0, 46.0)),  # Title
            ("lnE_Author", (679.5, 260.0), (543.0, 236.0, 273.0, 46.0)),  # Author
            ("lnE_PublishedYear", (679.5, 328.0), (543.0, 304.0, 273.0, 46.0)),  # Published Year
            ("lnE_Category", (679.5, 396.0), (543.0, 372.0, 273.0, 46.0)),  # Category
            ("lnE_Quantity", (679.5, 464.0), (543.0, 440.0, 273.0, 46.0))  # Quantity
        ]
       
        for entry_name, image_pos, dimensions in entry_fields:
            self.create_entry(entry_name, image_pos, dimensions, "#E7DCDC")
            # Set up focus events for validation
            self.entries[entry_name].bind("<FocusIn>", self.on_input_field_focus_in)
            self.entries[entry_name].bind("<FocusOut>", self.on_input_field_focus_out)
   
    def create_action_buttons(self):
        """Create action buttons"""
        # Add Book button
        self.create_button("btn_Confirm", (425.0, 508.0, 313.0, 48.0))
   
    def setup_field_placeholders(self):
        """Set up placeholders for form fields"""
        # Define placeholders
        self.placeholders = {
            "lnE_ISBN": "Enter ISBN",
            "lnE_Title": "Enter Title",
            "lnE_Author": "Enter Author",
            "lnE_PublishedYear": "Enter Year (1440-Present)",
            "lnE_Category": "Fiction, Non-Fiction, etc.",
            "lnE_Quantity": "Enter Quantity"
        }
       
        # Set placeholders
        for field, placeholder in self.placeholders.items():
            self.entries[field].insert(0, placeholder)
            self.entries[field].config(fg="grey")
   
    def on_input_field_focus_in(self, event):
        """Clear placeholder text when field receives focus"""
        widget = event.widget
       
        # Find which field this widget corresponds to
        for field_name, placeholder in self.placeholders.items():
            if widget == self.entries[field_name]:
                if widget.get() == placeholder:
                    widget.delete(0, "end")
                    widget.config(fg="#000716")  # Change to normal text color
                # Reset warning flag when user starts editing
                widget._shown_warning = False
                break

    def on_input_field_focus_out(self, event):
        """Restore placeholder text if field is empty and validate field content"""
        widget = event.widget
       
        # Define mapping of fields to their validation methods
        field_mapping = {
            "lnE_ISBN": (self.placeholders["lnE_ISBN"], add_book.validate_isbn_on_event),
            "lnE_Title": (self.placeholders["lnE_Title"], add_book.validate_title_on_event),
            "lnE_Author": (self.placeholders["lnE_Author"], add_book.validate_author_on_event),
            "lnE_PublishedYear": (self.placeholders["lnE_PublishedYear"], add_book.validate_published_year_on_event),
            "lnE_Category": (self.placeholders["lnE_Category"], add_book.validate_category_on_event),
            "lnE_Quantity": (self.placeholders["lnE_Quantity"], add_book.validate_quantity_on_event)
        }
       
        # Identify which field triggered the event
        for field_name, (placeholder, validation_func) in field_mapping.items():
            if widget == self.entries[field_name]:
                field_value = widget.get()
               
                # Restore placeholder if empty
                if not field_value:
                    widget.insert(0, placeholder)
                    widget.config(fg="grey")
                    widget._shown_warning = False  # Reset warning flag
                    return
               
                # Skip validation if it's still the placeholder
                if field_value == placeholder:
                    return
               
                # Validate field
                valid, message = validation_func(field_value)
               
                if not valid:
                    # Show warning only if not already shown
                    if not widget._shown_warning:
                        messagebox.showwarning(f"Invalid {field_name.split('_')[-1]}", message)
                        widget._shown_warning = True  # Set flag to prevent duplicate warnings
                    # Schedule focus to happen after the messagebox is closed
                    self.root.after(100, lambda w=widget: w.focus_set())
                else:
                    # If field is valid and it's an author or title, format it properly
                    if field_name == "lnE_Author":
                        _, _, formatted_value = add_book.validate_author(field_value)
                        # Only update if the formatting changed something
                        if formatted_value != field_value:
                            widget.delete(0, "end")
                            widget.insert(0, formatted_value)
                    elif field_name == "lnE_Title":
                        _, _, formatted_value = add_book.validate_title(field_value)
                        # Only update if the formatting changed something
                        if formatted_value != field_value:
                            widget.delete(0, "end")
                            widget.insert(0, formatted_value)
                   
                    widget._shown_warning = False  # Reset flag if validation passes
                break  # Exit loop after handling the matched field
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
       
        self.buttons[button_name] = button
   
    def create_entry(self, entry_name, image_position, dimensions, bg_color):
        """Create an entry field with the given parameters"""
        self.images[entry_name] = PhotoImage(
            file=self.relative_to_assets(f"{entry_name}.png")
        )
       
        entry_bg = self.canvas.create_image(
            image_position[0],
            image_position[1],
            image=self.images[entry_name]
        )
       
        entry = Entry(
            bd=0,
            bg=bg_color,
            fg="#000716",
            font=self.vietnamese_font,
            highlightthickness=0
        )
       
        entry.place(
            x=dimensions[0],
            y=dimensions[1],
            width=dimensions[2],
            height=dimensions[3]
        )
       
        self.entries[entry_name] = entry
   
    def button_click(self, button_name):
        """Handle button click events"""
        print(f"{button_name} clicked")
       
        if button_name == "btn_Confirm":
            # Temporarily disable FocusOut validation to avoid duplicate triggers
            for field_name in self.entries:
                self.entries[field_name].unbind("<FocusOut>")
           
            # Allow safe focus change without triggering validation
            self.root.focus_set()
           
            # Retrieve values from entry fields
            isbn = self.entries["lnE_ISBN"].get()
            title = self.entries["lnE_Title"].get()
            author = self.entries["lnE_Author"].get()
            published_year = self.entries["lnE_PublishedYear"].get()
            category = self.entries["lnE_Category"].get()
            quantity = self.entries["lnE_Quantity"].get()
           
            # Skip if placeholders are detected
            if isbn == self.placeholders["lnE_ISBN"]:
                messagebox.showerror("Error", "ISBN cannot be empty")
                return
            elif title == self.placeholders["lnE_Title"]:
                messagebox.showerror("Error", "Title cannot be empty")
                return
            elif author == self.placeholders["lnE_Author"]:
                messagebox.showerror("Error", "Author cannot be empty")
                return
            elif published_year == self.placeholders["lnE_PublishedYear"]:
                messagebox.showerror("Error", "Published Year cannot be empty")
                return
            elif category == self.placeholders["lnE_Category"]:
                messagebox.showerror("Error", "Category cannot be empty")
                return
            elif quantity == self.placeholders["lnE_Quantity"]:
                messagebox.showerror("Error", "Quantity cannot be empty")
                return
           
            # Process the form if all validations pass
            success, message, book_data = add_book.process_book_form(
                isbn, title, author, published_year, category, quantity
            )
           
            if success:
                # Transition to the confirmation screen
                self.root.destroy()
                from BookManaAddBook1 import BookManaAddBook1App
                confirm_root = Tk()
               
                # Create instance of confirmation screen and pass book data
                confirm_app = BookManaAddBook1App(confirm_root)
               
                # Set the book details in the confirmation screen
                confirm_app.canvas.itemconfig(confirm_app.lbl_ISBN, text=book_data['book_id'])
                confirm_app.canvas.itemconfig(confirm_app.lbl_Title, text=book_data['title'])
                confirm_app.canvas.itemconfig(confirm_app.lbl_Author, text=book_data['author'])
                confirm_app.canvas.itemconfig(confirm_app.lbl_PublishedYear, text=book_data['published_year'])
                confirm_app.canvas.itemconfig(confirm_app.lbl_Category, text=book_data['category'])
                confirm_app.canvas.itemconfig(confirm_app.lbl_Quantity, text=book_data['quantity'])
               
                confirm_root.mainloop()
            else:
                messagebox.showerror("Error", message)
       
        elif button_name == "btn_AddBook":
            # Refresh the current page
            self.root.destroy()
            root = Tk()
            app = BookManagementAddBookApp(root)
            root.mainloop()
       
        elif button_name == 'btn_EditBookInformation':
            # Navigate to Edit Book Information screen
            self.root.destroy()
            # Import and open the edit book screen
            # This would need to be implemented based on your application structure
       
        elif button_name == 'btn_BackToHomepage':
            # Navigate back to homepage
            self.root.destroy()
            # Import and open the homepage
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.append(parent_dir)
            from Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root)
            homepage_root.mainloop()
   
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = BookManagementAddBookApp(root)
    app.run()

