from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sys
import os
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

class BorrowReceiptApp:
    def __init__(self, root, user_data=None, receipt_id=None, borrow_date=None, return_deadline=None, assets_path=None):
        self.root = root
        self.user_data = user_data
        self.receipt_id = receipt_id
        self.borrow_date = borrow_date
        self.return_deadline = return_deadline  # Store the return deadline

        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        if self.user_data and len(self.user_data) > 6 and self.user_data[6] == "Admin":
            self.role = "admin"
        else:
            self.role = None or "user"

        self.output_path = Path(__file__).parent
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBorrowReceipt")

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

        # Load receipt data if we have a receipt_id
        if self.receipt_id:
            self.load_and_display_receipt()
        else:
            # For backward compatibility, use placeholder data if no receipt_id
            self.create_text_fields_with_placeholders()

    def load_and_display_receipt(self):
        """Load receipt data and create text fields with actual values"""
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.append(parent_dir)

        from Model.receipt_model import Receipt
        from Model.book_model import Book

        try:
            # Get primary receipt data
            receipt_data = Receipt.get_receipt_by_id(self.receipt_id)

            if not receipt_data:
                # If receipt not found, use placeholders
                self.create_text_fields_with_placeholders()
                return

            # Receipt_data structure: (receipt_id, user_id, book_id, borrow_date, return_date, status, borrowed_quantity)
            receipt_id = receipt_data[0]
            user_id = receipt_data[1]
            book_id = receipt_data[2]
            borrow_date = receipt_data[3]
            return_date = receipt_data[4]
            status = receipt_data[5]

            # Get borrowed_quantity - this might be at index 6
            borrowed_quantity = receipt_data[6] if len(receipt_data) > 6 else 1

            # Get all related receipts (same user_id, same borrow_date)
            related_receipts = []
            if self.borrow_date:
                related_receipts = Receipt.get_related_receipts(user_id, borrow_date)
            else:
                # If borrow_date wasn't provided, get it from the receipt
                self.borrow_date = borrow_date
                related_receipts = Receipt.get_related_receipts(user_id, borrow_date)

            # Initialize display_book_id variable
            display_book_id = book_id

            # If we have multiple related receipts, handle as a multi-book receipt
            if len(related_receipts) > 1:
                # For multiple books, display a comma-separated list of ISBNs
                book_ids = [receipt[2] for receipt in related_receipts]
                combined_book_ids = ", ".join(book_ids)

                # Truncate the combined book_ids if too long
                if len(combined_book_ids) > 26:
                    display_book_id = combined_book_ids[:23] + "..."
                else:
                    display_book_id = combined_book_ids

                # Calculate total quantity from related receipts
                total_quantity = 0
                for related_receipt in related_receipts:
                    # Check if borrowed_quantity is available at index 6
                    receipt_quantity = related_receipt[6] if len(related_receipt) > 6 else 1
                    total_quantity += receipt_quantity

                # Use return_deadline if provided, otherwise calculate it
                display_return_date = self.return_deadline
                if not display_return_date and borrow_date:
                    # Calculate return deadline (20 days after borrow_date)
                    try:
                        borrow_date_obj = datetime.datetime.strptime(borrow_date, '%Y-%m-%d')
                        display_return_date = (borrow_date_obj + datetime.timedelta(days=20)).strftime('%Y-%m-%d')
                    except ValueError:
                        display_return_date = "N/A"

                # Create text fields with multi-book receipt data
                self.create_text_fields(
                    receipt_id=str(receipt_id),
                    user_id=str(user_id),
                    book_id=display_book_id,
                    quantity=str(total_quantity),
                    borrow_date=borrow_date,
                    return_date=display_return_date  # Use calculated return deadline
                )

            else:
                # Single book receipt - display normally
                # Truncate book_id if it's too long
                if len(book_id) > 26:
                    display_book_id = book_id[:23] + "..."
                else:
                    display_book_id = book_id

                # Use return_deadline if provided, otherwise calculate it
                display_return_date = self.return_deadline
                if not display_return_date and borrow_date:
                    # Calculate return deadline (20 days after borrow_date)
                    try:
                        borrow_date_obj = datetime.datetime.strptime(borrow_date, '%Y-%m-%d')
                        display_return_date = (borrow_date_obj + datetime.timedelta(days=20)).strftime('%Y-%m-%d')
                    except ValueError:
                        display_return_date = "N/A"

                self.create_text_fields(
                    receipt_id=str(receipt_id),
                    user_id=str(user_id),
                    book_id=display_book_id,
                    quantity=str(borrowed_quantity),
                    borrow_date=borrow_date,
                    return_date=display_return_date  # Use calculated return deadline
                )
        except Exception as e:
            print(f"Error processing receipt data: {e}")
            import traceback
            traceback.print_exc()
            # If there's an error, use placeholders
            self.create_text_fields_with_placeholders()

    def relative_to_assets(self, path: str) -> Path:
        """Convert relative asset path to absolute path"""
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

    def load_images(self):
        """Load all required images"""
        image_files = [
            "image_2.png",
            "image_3.png",
            "image_4.png",
            "image_5.png",
            "image_6.png",
            "image_7.png",
            "image_8.png",
            "image_9.png",
            "btn_BackToHomepage.png",
            "btn_ReturnBook.png",
            "btn_BorrowBook.png",
            "btn_Back.png"
        ]

        for image_file in image_files:
            full_path = self.relative_to_assets(image_file)
            try:
                self.images[image_file] = PhotoImage(file=full_path)
            except Exception as e:
                print(f"Error loading image {full_path}: {e}")

    def create_sidebar(self):
        """Create the blue sidebar and its content"""
        self.canvas.create_rectangle(
            0.0,
            0.0,
            262.0,
            605.0,
            fill="#0A66C2",
            outline=""
        )

        # Add Logo
        if "image_2.png" in self.images:
            self.canvas.create_image(
                130.0,
                73.0,
                image=self.images["image_2.png"]
            )

    def create_main_content(self):
        """Create the main content area with the background and images"""
        # Background rectangle
        self.create_rounded_rectangle(
            287.0,
            39.0,
            873.0,
            567.0,
            color="#F0F0F0",
            radius=10
        )

        # Header image
        if "image_3.png" in self.images:
            self.canvas.create_image(
                579.0,
                70.0,
                image=self.images["image_3.png"]
            )

        # Other images
        image_positions = [
            ("image_4.png", 403.0, 117.0),
            ("image_5.png", 367.0, 185.0),
            ("image_6.png", 381.0, 253.0),
            ("image_7.png", 415.0, 389.0),
            ("image_8.png", 430.0, 457.0),
            ("image_9.png", 422.0, 321.0)
        ]

        for img_name, x, y in image_positions:
            if img_name in self.images:
                self.canvas.create_image(
                    x,
                    y,
                    image=self.images[img_name]
                )

    def create_text_fields(self, receipt_id="", user_id="", book_id="", quantity="", borrow_date="", return_date=""):
        """Create all text fields in the application"""
        if len(book_id) > 26:
            display_book_id = book_id[:23] + "..."
        else:
            display_book_id = book_id

        text_configs = [
            (579.0, 107.0, receipt_id, "lbl_ReceiptID"),
            (579.0, 175.0, user_id, "lbl_UserID"),
            (579.0, 244.0, display_book_id, "lbl_ISBN"),
            (579.0, 312.0, quantity, "lbl_Quantity"),
            (579.0, 380.0, borrow_date, "lbl_BorrowDate"),
            (579.0, 448.0, return_date, "lbl_ReturnDate")
        ]

        for x, y, text, field_name in text_configs:
            text_field = self.canvas.create_text(
                x,
                y,
                anchor="nw",
                text=text,
                fill="#0A66C2",
                font=("Montserrat Medium", 18 * -1)
            )

            # Store text field references
            setattr(self, field_name, text_field)

    def create_text_fields_with_placeholders(self):
        """Create text fields with placeholder values (for backward compatibility)"""
        # Calculate return deadline (20 days from today)
        today = datetime.datetime.now()
        return_deadline = (today + datetime.timedelta(days=20)).strftime('%Y-%m-%d')
        
        self.create_text_fields(
            receipt_id="212",
            user_id="112",
            book_id="0123456789",
            quantity="1",
            borrow_date=today.strftime('%Y-%m-%d'),
            return_date=return_deadline
        )

    def create_buttons(self):
        """Create all buttons in the application"""
        button_configs = [
            ("btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_clicked),
            ("btn_ReturnBook.png", 0.0, 219.0, 262.0, 25.0, self.on_return_book_clicked),
            ("btn_BorrowBook.png", 0.0, 181.0, 262.0, 25.0, self.on_borrow_book_clicked),
            ("btn_Back.png", 424.0, 501.0, 313.0, 48.0, self.on_back_clicked)
        ]

        for img_name, x, y, width, height, command in button_configs:
            self.create_button(img_name, x, y, width, height, command)

    def create_button(self, image_name, x, y, width, height, command):
        """Helper method to create a button"""
        if image_name not in self.images:
            return None

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

        # Store button references
        button_name = image_name.replace(".png", "")
        setattr(self, button_name, button)
        return button

    def on_back_to_homepage_clicked(self): # Switch to Homepage
        """Handle back to homepage button click"""
        self.root.destroy()
        from View.Homepage import HomepageApp
        homepage_root = Tk()
        homepage = HomepageApp(homepage_root, user_data = self.user_data, role = self.role)
        homepage_root.mainloop()

    def on_return_book_clicked(self): # Switch to Return book section
        """Handle return book button click"""
        self.root.destroy()
        from View.BorrowReturnBook.Return1 import Return1App
        return_root = Tk()
        return_1 = Return1App(return_root, user_data = self.user_data)
        return_root.mainloop()

    def on_borrow_book_clicked(self): # Switch to Borrow book section
        """Handle borrow book button click"""
        self.root.destroy()
        from View.BorrowReturnBook.Borrow1 import Borrow1App
        borrow_root = Tk()
        borrow = Borrow1App(borrow_root, user_data = self.user_data)
        borrow_root.mainloop()


    def on_back_clicked(self): # Switch to Borrow/Return window
        """Handle back button click"""
        self.root.destroy()
        from View.BorrowReturnBook.BorrowReturnBook import BorrowReturnApp
        borrow_return_root = Tk()
        borrow_return = BorrowReturnApp(borrow_return_root, user_data = self.user_data)
        borrow_return_root.mainloop()

if __name__ == "__main__":
    window = Tk()
    app = BorrowReceiptApp(window)
    window.mainloop()
