from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)

from Model.receipt_model import Receipt
from tkinter import messagebox

class Return1App:
    def __init__(self, root, user_data=None, assets_path=None):
        self.root = root
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        self.user_data = user_data

        if self.user_data and len(self.user_data) > 6 and self.user_data[6] == "Admin":
            self.role = "admin"
        else:
            self.role = None or "user"

        self.output_path = Path(__file__).parent
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameReturn1")
        
        self.images = {}
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
        
        self.load_images()
        self.create_main_layout()
        self.create_sidebar()
        self.create_main_content()
        self.create_entry_fields()
        self.create_buttons()
    
    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)
    
    def load_images(self):
        """Load all image assets"""
        image_files = [
            "image_1.png",
            "image_2.png",
            "image_4.png",
            "lnE_ReceiptID.png",
            "btn_BackToHomepage.png",
            "btn_ReturnBook.png",
            "btn_BorrowBook.png",
            "btn_Search.png"
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
    
    def create_main_layout(self):
        """Create the main layout rectangles"""
        # Main content area background
        self.create_rounded_rectangle(
            285.0,
            80.0,
            871.0,
            525.0,
            radius = 10,
            color="#F1F1F1"
        )
    
    def create_sidebar(self):
        """Create the sidebar with buttons and logo"""
        # Blue sidebar background
        self.canvas.create_rectangle(
            0.0,
            0.0,
            262.0,
            605.0,
            fill="#0A66C2",
            outline=""
        )
        
        # Logo image
        if "image_4.png" in self.images:
            self.canvas.create_image(
                130.0,
                73.0,
                image=self.images["image_4.png"]
            )
        
        # Create sidebar buttons
        self.create_button("btn_BorrowBook.png", 0.0, 181.0, 262.0, 25.0, self.on_borrow_book_click)
        self.create_button("btn_ReturnBook.png", 0.0, 219.0, 262.0, 25.0, self.on_return_book_click)
        self.create_button("btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_click)
    
    def create_main_content(self):
        """Create the main content area with images"""
        # Header image
        if "image_1.png" in self.images:
            self.canvas.create_image(
                578.0,
                118.0,
                image=self.images["image_1.png"]
            )
        
        # Receipt ID label image
        if "image_2.png" in self.images:
            self.canvas.create_image(
                397.0,
                223.0,
                image=self.images["image_2.png"]
            )
    
    def create_entry_fields(self):
        """Create entry fields"""
        if "lnE_ReceiptID.png" in self.images:
            entry_bg_1 = self.canvas.create_image(
                684.5,
                223.0,
                image=self.images["lnE_ReceiptID.png"]
            )
            
            self.lnE_ReceiptID = Entry(
                bd=0,
                bg="#E7DCDC",
                fg="#000716",
                highlightthickness=0
            )
            self.lnE_ReceiptID.place(
                x=554.0,
                y=199.0,
                width=261.0,
                height=46.0
            )
    
    def create_buttons(self):
        """Create action buttons"""
        self.create_button("btn_Search.png", 420.0, 401.0, 313.0, 48.0, self.on_search_click)
    
    def create_button(self, image_name, x, y, width, height, command):
        """Helper method to create buttons"""
        if image_name not in self.images:
            return None
            
        button = Button(
            image=self.images[image_name], 
            borderwidth=0, 
            highlightthickness=0, 
            command=command, 
            relief="flat"
        )
        
        button.place(x=x, y=y, width=width, height=height)
        
        button_name = image_name.replace(".png", "")
        if button_name.startswith("btn_"):
            setattr(self, button_name, button)
            
        return button
    
    # Event handlers
    def on_borrow_book_click(self):
        self.root.destroy()
        from View.BorrowReturnBook.Borrow1 import Borrow1App
        borrow1_root = Tk()
        borrow1 = Borrow1App(borrow1_root,user_data=self.user_data)
        borrow1_root.mainloop()
        
    def on_return_book_click(self):
        self.root.destroy()
        from View.BorrowReturnBook.Return1 import Return1App
        return1_root = Tk()
        return1 = Return1App(return1_root, user_data=self.user_data)
        return1_root.mainloop()
    
    def on_back_to_homepage_click(self):
        self.root.destroy()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(base_dir, "View"))
        sys.path.append(base_dir)
        from View.Homepage import HomepageApp
        homepage_root = Tk()
        homepage = HomepageApp(homepage_root,role=self.role, user_data=self.user_data)
        homepage_root.mainloop()

    def on_search_click(self):
        receipt_id = self.lnE_ReceiptID.get()

        if not receipt_id:
            messagebox.showwarning("Warning", "Please enter a Receipt ID")
            return
        
        # Use the controller to validate the receipt
        from Controller.borrow_return_controller import ReturnController

        # Extract user_id from self.user_data if available
        user_id = self.user_data[0] if self.user_data else None

        # Validate receipt access through controller
        is_valid, message = ReturnController.validate_receipt_access(receipt_id, user_id)

        if not is_valid:
            messagebox.showerror("Error", message)
            return
        
        is_valid_status, status_message = ReturnController.validate_receipt_status(receipt_id)
        if not is_valid_status:
            from View.noti_tab_view_1 import AlreadyReturnedNotification
            AlreadyReturnedNotification(self.root, status_message)
            return
    
        self.root.destroy()
        from View.BorrowReturnBook.Return2 import Return2App 
        return2_root = Tk()
        return2 = Return2App(return2_root, receipt_id = receipt_id, user_data=self.user_data)
        return2_root.mainloop()

if __name__ == "__main__":
    window = Tk()
    app = Return1App(window)
    window.mainloop() 