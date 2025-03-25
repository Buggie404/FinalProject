from pathlib import Path 
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox

class Borrow1App:
    def __init__(self, root, user_data=None, receipt_id=None, assets_path=None):
        self.root = root
        self.user_data = user_data
        
        # Get user_role from user_data
        if self.user_data and len(self.user_data) > 6 and self.user_data[6] == "Admin":
            self.role = "admin"
        else:
            self.role = None or "user"
        
        # Extract user_id from user_data if available
        if self.user_data:
            self.user_id = self.user_data[0]  # get user id from user data
        else:
            self.user_id = None
            
        self.receipt_id = receipt_id
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.output_path = Path(__file__).parent
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBorrow1")

        # Store image references to prevent garbage collection
        self.images = {}

        # Setup UI components
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
        
        # Load all images
        self.load_images()
        
        # Create UI elements
        self.create_sidebar()
        self.create_main_content()
        self.create_buttons()

    def relative_to_assets(self, path: str) -> Path:
        """Convert relative asset path to absolute path"""
        return self.assets_path / Path(path)

    def load_images(self):
        """Load all required images"""
        image_files = [
            "lnE_ID.png",
            "lnE_ISBN.png",
            "btn_BackToHomepage.png",
            "btn_ReturnBook.png",
            "btn_BorrowBook.png",
            "btn_Search.png",
            "image_1.png",
            "image_2.png",
            "image_3.png",
            "image_5.png"
        ]

        for image_file in image_files:
            full_path = self.relative_to_assets(image_file)
            try:
                self.images[image_file] = PhotoImage(file=full_path)
            except Exception as e:
                print(f"Error loading image {full_path}: {e}")

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

    def create_sidebar(self):
        """Create the blue sidebar rectangle and its content"""
        self.canvas.create_rectangle(
            0.0,
            0.0,
            262.0,
            605.0,
            fill="#0A66C2",
            outline=""
        )

        # Add images to sidebar
        if "image_4.png" in self.images:
            self.canvas.create_image(
                131.0,
                74.0,
                image=self.images["image_4.png"]
            )

        if "image_5.png" in self.images:
            self.canvas.create_image(
                130.0,
                73.0,
                image=self.images["image_5.png"]
            )

    def create_main_content(self):
        """Create the main content area with entry fields and header images"""
        self.create_rounded_rectangle(
            285.0, 80.0, 871.0, 525.0,
            radius=10, color="#F1F1F1"
        )

        # Create header images
        self.create_image("image_1.png", 578.0, 118.0)
        self.create_image("image_2.png", 400.0, 223.0)
        self.create_image("image_3.png", 400.0, 301.0)

        # Create entry fields
        self.create_entry("lnE_ID.png", 684.5, 223.0, 554.0, 199.0, 261.0, 46.0)
        self.create_entry("lnE_ISBN.png", 684.5, 301.0, 554.0, 277.0, 261.0, 46.0)
        
        # Populate user ID if available - after entries are created
        if hasattr(self, 'lnE_ID') and hasattr(self, 'user_id') and self.user_id:
            self.lnE_ID.delete(0, 'end')
            self.lnE_ID.insert(0, str(self.user_id))

    def create_image(self, image_name, x, y):
        """Helper method to create an image"""
        if image_name in self.images:
            self.canvas.create_image(
                x, y,
                image=self.images[image_name]
            )

    def create_entry(self, image_name, img_x, img_y, entry_x, entry_y, width, height):
        """Helper method to create an entry field with background image"""
        if image_name in self.images:
            self.canvas.create_image(
                img_x, img_y,
                image=self.images[image_name]
            )

        entry = Entry(
            bd=0,
            bg="#E7DCDC",
            fg="#000716",
            highlightthickness=0
        )

        entry.place(
            x=entry_x,
            y=entry_y,
            width=width,
            height=height
        )

        # Store reference to entry fields for later access
        if image_name == "lnE_ID.png":
            self.lnE_ID = entry
            # If we have a user_id, populate it immediately
            if hasattr(self, 'user_id') and self.user_id:
                entry.delete(0, 'end')
                entry.insert(0, str(self.user_id))
        elif image_name == "lnE_ISBN.png":
            self.lnE_ISBN = entry

        return entry

    def create_buttons(self):
        """Create all buttons"""
        self.create_button("btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_clicked)
        self.create_button("btn_ReturnBook.png", 0.0, 219.0, 262.0, 25.0, self.on_return_book_clicked)
        self.create_button("btn_BorrowBook.png", 0.0, 181.0, 262.0, 25.0, self.on_borrow_book_clicked)
        self.create_button("btn_Search.png", 420.0, 401.0, 313.0, 48.0, self.on_search_clicked)

    def create_button(self, image_name, x, y, width, height, command):
        """Helper method to create a button"""
        if image_name in self.images:
            button = Button(
                image=self.images[image_name],
                borderwidth=0,
                highlightthickness=0,
                command=command,
                relief="flat"
            )

            button.place(
                x=x,
                y=y,
                width=width,
                height=height
            )

            # Store reference to buttons for later access
            if image_name == "btn_BackToHomepage.png":
                self.btn_BackToHomepage = button
            elif image_name == "btn_ReturnBook.png":
                self.btn_ReturnBook = button
            elif image_name == "btn_BorrowBook.png":
                self.btn_BorrowBook = button
            elif image_name == "btn_Search.png":
                self.btn_Search = button

            return button

    def on_back_to_homepage_clicked(self): # Switch back to Hokmepage window
        """Handle Back to Homepage button click event"""
        if IndexError:
            messagebox.showerror("Error", "Cannot go to Homepage while Borrowing Book!")
        else:
            self.root.destroy()
            from View.Homepage import HomepageApp
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root, role = self.role, user_data = self.user_data)
            homepage_root.mainloop()

    def on_return_book_clicked(self): # Switch to Return Book window
        """Handle Return Book button click event"""
        self.root.destroy()
        from View.BorrowReturnBook.Return1 import Return1App
        return_root = Tk()
        return_1 = Return1App(return_root, user_data=self.user_data)
        return_root.mainloop()

    def on_borrow_book_clicked(self): # Switch back to Borrow/Return window
        """Handle Borrow Book button click event"""
        self.root.destroy()
        from View.BorrowReturnBook.BorrowReturnBook import BorrowReturnApp
        borrow_return_root = Tk()
        borrow_return = BorrowReturnApp(borrow_return_root, user_data=self.user_data)
        borrow_return_root.mainloop()

    def on_search_clicked(self):
        """Handle Search button click event"""
        # Get user input
        book_id = self.lnE_ISBN.get().strip()
        # Fill user_id with logged-in account
        user_id = self.lnE_ID.get().strip()
        if hasattr(self, 'user_id') and self.user_id:
            if str(user_id) != str(self.user_id):
                messagebox.showerror("Error", "Cannot user other ID to borrow books!")
            user_id = self.user_id

        # Import View and Controller
        from Controller.borrow_return_controller import BorrowController, BorrowingCart
        from View.noti_tab_view_1 import Message_1
        from View.BorrowReturnBook.Borrow2 import Borrow2App
        from Model.book_model import Book

        # Get the cart and set the user
        cart = BorrowingCart.get_instance()
        if user_id:
            cart.set_user(user_id)

        # Validate user and book
        is_valid, user_data, book_data, error_message = BorrowController.validate_user_and_book(user_id, book_id)

        if not is_valid:
            # Display error message
            if error_message == "No match ID!":
                Message_1(self.root, 'edit_pass_id')
            elif error_message == "No match ISBN!":
                Message_1(self.root, 'edit_book_id')
            elif error_message == "ID cannot be empty!":
                messagebox.showerror("Error", "ID cannot be empty")
            else:
                messagebox.showerror("Error", "ISBN cannot be empty!")
            return

        # If valid, switch to Borrow2 window
        self.root.destroy()
        borrowing_root = Tk()
        borrowing = Borrow2App(borrowing_root, self.user_data, book_id)

        # Set values in Borrow2
        borrowing.canvas.itemconfig(borrowing.lbl_ID, text=user_id)
        borrowing.canvas.itemconfig(borrowing.lbl_ISBN, text=book_id)

        # Get and set available quantity
        available_quantity = Book.get_quantity(book_id)
        borrowing.canvas.itemconfig(borrowing.lbl_AvailableQuantities, text=available_quantity)
        borrowing_root.mainloop()

if __name__ == "__main__":
    window = Tk()
    app = Borrow1App(window)
    window.mainloop()