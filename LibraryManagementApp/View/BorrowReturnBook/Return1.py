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
    def __init__(self, root, assets_path=None):
        self.root = root
        self.root.geometry("898x605")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
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
            print(f"Warning: Image {image_name} not found")
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
        print("btn_BorrowBook clicked")
        # Implement borrow book functionality here
    
    def on_return_book_click(self):
        print("btn_ReturnBook clicked")
        # Implement return book functionality here
    
    def on_back_to_homepage_click(self):
        print("btn_BackToHomepage clicked")
        # Implement back to homepage functionality here
    
    # def on_search_click(self):
    #     print("btn_Search clicked")
        # Implement search functionality here
        # receipt_id = self.lnE_ReceiptID.get()
        # print(f"Searching for receipt ID: {receipt_id}")
    def on_search_click(self):
        # receipt_id = self.lnE_ReceiptID.get()
        
        # if not receipt_id:
        #     print("Vui lòng nhập Receipt ID!")  
        #     return
        
        # print(f"Tìm kiếm Receipt ID: {receipt_id}")
        
        # # Đóng Return1App và mở Return2App
        # self.root.destroy()
        
        # new_window = Tk()
        # parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # sys.path.append(parent_dir)  
        # from Return2 import Return2App  
        # Return2App(new_window)
        # new_window.mainloop()
        receipt_id = self.lnE_ReceiptID.get()

        if not receipt_id:
            messagebox.showwarning("Warning", "Please enter a Receipt ID")
            return
    
    # Kiểm tra receipt trong database
        receipt_data = Receipt.get_receipt_by_id(receipt_id)

        if not receipt_data:
            messagebox.showerror("Error", "Receipt not found!")
            return
    
        # Nếu tìm thấy, đóng cửa sổ Return1 và mở Return2, truyền receipt_id qua
        self.root.destroy()

        new_window = Tk()

        from View.BorrowReturnBook.Return2 import Return2App 
        Return2App(new_window)
        new_window.mainloop()

# Entry point
if __name__ == "__main__":
    window = Tk()
    app = Return1App(window)
    window.mainloop()