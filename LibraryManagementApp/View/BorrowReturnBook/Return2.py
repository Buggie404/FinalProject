from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import os, sys
from datetime import datetime, timedelta
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)
from View.noti_tab_view_1 import Drop_Off
class Return2App:
    def __init__(self, root, receipt_id=None, user_data=None, assets_path=None):
        self.root = root
        self.root.geometry("898x605")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        self.receipt_id = receipt_id
        self.user_data = user_data
        
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameReturn2")
        
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
        self.create_main_content()
        self.create_sidebar()
        self.create_buttons()
        self.create_text_fields()
        # Load receipt data if ID is provided
        if self.receipt_id:
            self.load_receipt_data()
        
    def relative_to_assets(self, path: str) -> Path:
        """Convert relative asset path to absolute path"""
        return self.assets_path / Path(path)
    
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
            "btn_DropOff.png"
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
        self.canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill=color,
                               outline=color)
        # Bo góc dưới bên phải
        self.canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill=color,
                               outline=color)

        # Phần thân của hình chữ nhật
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)
    
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
            285.0,
            39.0,
            871.0,
            567.0,
            color="#F1F1F1",
            radius=10
        )
        
        # Header image
        if "image_3.png" in self.images:
            self.canvas.create_image(
                577.0,
                70.0,
                image=self.images["image_3.png"]
            )
        
        # Other images
        image_positions = [
            ("image_4.png", 401.0, 120.0),
            ("image_5.png", 366.0, 188.0),
            ("image_6.png", 377.0, 256.0),
            ("image_7.png", 411.0, 392.0),
            ("image_8.png", 428.0, 460.0),
            ("image_9.png", 420.0, 324.0)
        ]
        
        for img_name, x, y in image_positions:
            if img_name in self.images:
                self.canvas.create_image(
                    x, y, image=self.images[img_name]
                )
    
    def create_text_fields(self):
        """Create all text fields in the application"""
        text_configs = [
            (577.0, 110.0, "212", "lbl_ReceiptID"),
            (577.0, 178.0, "112", "lbl_UserID"),
            (577.0, 247.0, "0123456789", "lbl_ISBN"),
            (577.0, 315.0, "1", "lbl_Quantity"),
            (577.0, 383.0, "2025/03/21", "lbl_BorrowDate"),
            (577.0, 451.0, "2025/03/25", "lbl_ReturnDate")
        ]
        
        for x, y, text, field_name in text_configs:
            text_field = self.canvas.create_text(
                x, y,
                anchor="nw",
                text=text,
                fill="#0A66C2",
                font=("Montserrat Medium", 18 * -1)
            )
            
            # Store text field references
            setattr(self, field_name, text_field)
    
    def create_buttons(self):
        """Create all buttons in the application"""
        button_configs = [
            ("btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_clicked),
            ("btn_ReturnBook.png", 0.0, 219.0, 262.0, 25.0, self.on_return_book_clicked),
            ("btn_BorrowBook.png", 0.0, 181.0, 262.0, 25.0, self.on_borrow_book_clicked),
            ("btn_DropOff.png", 422.0, 501.0, 313.0, 48.0, self.on_drop_off_clicked)
        ]
        
        for img_name, x, y, width, height, command in button_configs:
            self.create_button(img_name, x, y, width, height, command)
    
    def create_button(self, image_name, x, y, width, height, command):
        """Helper method to create a button"""
        if image_name not in self.images:
            print(f"Warning: Image {image_name} not found")
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
    
    def on_back_to_homepage_clicked(self):
        """Handle back to homepage button click"""
        print("btn_BackToHomepage clicked")
        self.root.destroy()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(base_dir, "View"))
        sys.path.append(base_dir)
        from View.Homepage import HomepageApp
        homepage_root = Tk()
        homepage = HomepageApp(homepage_root)
        homepage_root.mainloop()

    def on_return_book_clicked(self):
        """Handle return book button click"""
        print("btn_ReturnBook clicked")
        self.root.destroy()
        from View.BorrowReturnBook.Return1 import Return1App
        return1_root = Tk()
        return1 = Return1App(return1_root)
        return1_root.mainloop()

    def on_borrow_book_clicked(self):
        """Handle borrow book button click"""
        print("btn_BorrowBook clicked")
        self.root.destroy()
        from View.BorrowReturnBook.Borrow1 import Borrow1App
        borrow1_root = Tk()
        borrow1 = Borrow1App(borrow1_root)
        borrow1_root.mainloop()

    def on_drop_off_clicked(self):
        from Controller.return_controller import ReturnController
        from View.noti_tab_view_1 import Drop_Off
        from tkinter import messagebox
        from datetime import datetime, timedelta
        import traceback

        print("btn_DropOff clicked")
        
        try:
            # Get the current date for database update
            current_date = datetime.now()
            formatted_return_date = current_date.strftime("%Y-%m-%d")
            
            # Get the book_id from the UI
            book_id = self.canvas.itemcget(self.lbl_ISBN, "text")
            
            # Compare current date with return deadline to determine status
            if hasattr(self, 'return_deadline'):
                if current_date.date() <= self.return_deadline.date():
                    receipt_status = "Returned"
                else:
                    receipt_status = "Overdue"
            else:
                # Fallback if return_deadline is not set
                receipt_status = "Returned"
            
            # Update return_date and status in database ONLY
            from Model.receipt_model import Receipt
            success = Receipt.update_return_status(self.receipt_id, formatted_return_date, receipt_status)
            
            if not success:
                messagebox.showerror("Error", "Database update failed!")
                return
            
            # Update book quantity in database
            from Model.book_model import Book
            Book.update_book_quantity_after_return(book_id, 1)
            
            # IMPORTANT: Do NOT update the UI display for return_date
            # The UI should continue showing the original return deadline
            
            # Display Drop Off notification
            drop_off_window = Drop_Off(self.root, receipt_status, self.receipt_id)
            
            # Wait for popup to close before continuing
            self.root.wait_window(drop_off_window.delete_noti)
            
            # Handle next steps based on receipt status
            if receipt_status == "Overdue":
                drop_off_window.pay_overdue_fine()
            else:
                drop_off_window.switch_to_return()
                
        except Exception as e:
            print(f"Error in on_drop_off_clicked: {e}")
            traceback.print_exc()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")



        # Load receipt data from database
    def load_receipt_data(self):
        """Load and display receipt data for the given receipt_id"""
        if not self.receipt_id:
            print("No receipt ID provided")
            return

        from Model.receipt_model import Receipt
        # Get receipt data from database
        receipt_data = Receipt.get_single_receipt_by_id(self.receipt_id)

        if not receipt_data:
            print(f"No receipt found with ID: {self.receipt_id}")
            messagebox.showerror("Error", f"No receipt found with ID: {self.receipt_id}")
            return

        print(f"Loaded receipt data: {receipt_data}")

        # Update text fields with receipt data
        # Assuming receipt_data format: (receipt_id, user_id, book_id, borrow_date, return_date, status, borrowed_quantity)
        self.canvas.itemconfigure(self.lbl_ReceiptID, text=str(receipt_data[0]))  # receipt_id
        self.canvas.itemconfigure(self.lbl_UserID, text=str(receipt_data[1]))     # user_id
        self.canvas.itemconfigure(self.lbl_ISBN, text=str(receipt_data[2]))       # book_id (ISBN)

        # For quantity - check if it exists in the data
        if len(receipt_data) > 6 and receipt_data[6] is not None:
            self.canvas.itemconfigure(self.lbl_Quantity, text=str(receipt_data[6]))
        else:
            self.canvas.itemconfigure(self.lbl_Quantity, text="1")  # Default quantity
            
        # Ngày mượn sách
        if receipt_data[3]:
            borrow_date_obj = receipt_data[3]
            if isinstance(borrow_date_obj, str):
                try:
                    borrow_date_obj = datetime.strptime(borrow_date_obj, "%Y-%m-%d")
                except ValueError:
                    try:
                        borrow_date_obj = datetime.strptime(borrow_date_obj, "%Y/%m/%d")
                    except ValueError:
                        print(f"Invalid borrow date format: {borrow_date_obj}")
                        return
                        
            # Format and display borrow date
            borrow_date_str = borrow_date_obj.strftime("%Y/%m/%d")
            self.canvas.itemconfigure(self.lbl_BorrowDate, text=borrow_date_str)

            # Tính hạn trả (deadline) và lưu vào self
            self.return_deadline = borrow_date_obj + timedelta(days=20)
            return_deadline_str = self.return_deadline.strftime("%Y/%m/%d")

            # Hiển thị deadline vào lbl_ReturnDate
            self.canvas.itemconfigure(self.lbl_ReturnDate, text=return_deadline_str)



if __name__ == "__main__":
    window = Tk()
    app = Return2App(window)
    window.mainloop()