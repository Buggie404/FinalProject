from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import sys
import os

# Import controller
from Controller.book_management_controller import BookEditController

class BookEdit1App:
    def __init__(self, root, user_data = None, book_data=None, assets_path=None):
        # Initialize the main window
        self.root = root
        self.user_data = user_data
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        if self.user_data and len(self.user_data) > 6 and self.user_data[6] == "Admin":
            self.role = "admin"
        else:
            self.role = None or "user"
        
        # Store the book data
        self.book_data = book_data
        print(f"Book data received: {book_data}")
        
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
        
        # Build UI components
        self.create_background()
        self.create_sidebar()
        self.create_main_panel()
        self.create_entry_fields()
        
        # Initialize controller with this view
        self.controller = BookEditController(self)
        
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
        
        # Create save button
        self.create_confirm_button()
    
    def create_confirm_button(self):
        """Create the confirm button with binding to controller"""
        button_name = "btn_Confirm"
        dimensions = (421.0, 498.0, 313.0, 48.0)
        
        self.images[button_name] = PhotoImage(
            file=self.relative_to_assets(f"{button_name}.png")
        )
        
        # Create button with binding to controller's update_book method
        button = Button(
            image=self.images[button_name],
            borderwidth=0,
            highlightthickness=0,
            command= lambda: None, # Link to controller method
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
        print("Confirm button created with binding to controller's update_book method")
    
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
        try:
            self.images[image_name] = PhotoImage(
                file=self.relative_to_assets(f"{image_name}.png")
            )
            self.canvas.create_image(
                position[0], position[1],
                image=self.images[image_name]
            )
        except Exception as e:
            pass
    
    def create_button(self, button_name, dimensions):
        """Create a button with the given name and dimensions"""
        try:
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
        except Exception as e:
            pass
    
    def create_entry_field(self, entry_name, bg_position, dimensions):
        """Create an entry field with background image"""
        try:
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
        except Exception as e:
            pass
    
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
        # Define field validation mapping with controller methods
        field_validations = {
            "lnE_Title": self.controller.validate_title,
            "lnE_Author": self.controller.validate_author,
            "lnE_PublishedYear": self.controller.validate_published_year,
            "lnE_Category": self.controller.validate_category,
            "lnE_Quantity": self.controller.validate_quantity
        }
        
        # Bind validation to FocusOut events
        for field_name, validate_func in field_validations.items():
            self.entries[field_name].bind("<FocusOut>", 
                lambda event, func=validate_func: self.on_field_focus_out(event, func))
            
            # Reset warning flag on key release
            self.entries[field_name].bind("<KeyRelease>", self.reset_warning_flag)
    
    def reset_warning_flag(self, event):
        """Reset the warning flag when field content changes"""
        event.widget._shown_warning = False

    def on_field_focus_out(self, event, validate_func):
        """Handle field focus out event with validation"""
        # Skip validation if we're in the middle of form submission
        if hasattr(event.widget, '_skip_validation') and event.widget._skip_validation:
            return None
        
        # Call the validation function
        is_valid = validate_func(event)
        
        if not is_valid:
            # If validation fails, set focus back to this field
            self.root.after(10, lambda: event.widget.focus_set())
            return "break"  # Prevent default focus behavior
        
        return None
    
    def button_click(self, button_name):
        """Handle button click events"""
        
        if button_name == "btn_BackToHomepage":
            self.root.destroy()
            from View.Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role = self.role, user_data = self.user_data)
            homepage_root.mainloop()

        elif button_name == "btn_AddBook": 
            self.root.destroy()
            from View.BookManagement.BookManaAddBook import BookManagementAddBookApp
            add_book_root = Tk()
            add_book = BookManagementAddBookApp(add_book_root, user_data=self.user_data)
            add_book_root.mainloop()
            
        elif button_name == "btn_EditBookInformation":
            self.root.destroy()
            from View.BookManagement.BookManaEditBook import BookManaEditBook
            edit_book_root = Tk()
            edit_book = BookManaEditBook(edit_book_root, user_data=self.user_data)
            edit_book_root.mainloop()
    
    def get_field_values(self):
        """Get all field values for controller to use"""
        return {
            "title": self.entries["lnE_Title"].get().strip(),
            "author": self.entries["lnE_Author"].get().strip(),
            "published_year": self.entries["lnE_PublishedYear"].get().strip(),
            "category": self.entries["lnE_Category"].get().strip(),
            "quantity": self.entries["lnE_Quantity"].get().strip()
        }
    
    def show_success_message(self):
        """Hiển thị thông báo thành công và quay lại màn hình BookManaEditBook"""
        try:
            # Hiển thị thông báo thành công
            messagebox.showinfo("Success", "Book updated successfully!")
            
            # Đóng cửa sổ hiện tại
            self.root.destroy()
            
            # Mở màn hình BookManaEditBook mới
            from View.BookManagement.BookManaEditBook import BookManaEditBook
            edit_book_root = Tk()
            edit_book = BookManaEditBook(edit_book_root,user_data=self.user_data)
            edit_book_root.mainloop()
        except Exception as e:
            print(f"Error in show_success_message: {e}")
            import traceback
            traceback.print_exc()
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

if __name__ == "__main__":
    window = Tk()
    app = BookEdit1App(window)
    app.run()
