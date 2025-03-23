from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import os, sys
import datetime
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)
class ReturnOverdueApp:
    def __init__(self, root, receipt_id=None, assets_path=None):
        self.root = root
        self.root.geometry("898x605")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        self.receipt_id = receipt_id

        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameReturnOverdue")
        
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

        # Create UI elements
        self.create_main_content()
        self.create_sidebar()
        self.create_buttons()
        self.create_text_fields()
        self.create_images()
        self.load_due_and_fine_data()
        
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
        self.images["image_3"] = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(
            130.0,
            73.0,
            image=self.images["image_3"]
        )
    
    def create_main_content(self):
        """Create the main content area with background"""
        self.create_rounded_rectangle(
            285.0,
            103.0,
            871.0,
            469.0,
            color="#F1F1F1",
            radius=10
        )
        
        # Header image
        self.images["image_1"] = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(
            578.0,
            141.0,
            image=self.images["image_1"]
        )
    
    def create_text_fields(self):
        """Create all text fields in the application"""
        text_configs = [
            (579.0, 246.0, "1", "#0A66C2", ("Montserrat Medium", 18 * -1), "lbl_Quantity"),
            (579.0, 314.0, "10.000", "#0A66C2", ("Montserrat Medium", 18 * -1), "lbl_Amount")
        ]
        
        for x, y, text, fill, font, field_name in text_configs:
            text_field = self.canvas.create_text(
                x, y,
                anchor="nw",
                text=text,
                fill=fill,
                font=font
            )
            
            # Store text field references
            setattr(self, field_name, text_field)
    
    def create_images(self):
        """Create additional images in the UI"""
        image_configs = [
            ("image_4", "image_4.png", 578.0, 185.0),
            ("image_5", "image_5.png", 446.0, 256.0),
            ("image_6", "image_6.png", 396.0, 324.0)
        ]
        
        for name, file, x, y in image_configs:
            self.images[name] = PhotoImage(file=self.relative_to_assets(file))
            self.canvas.create_image(x, y, image=self.images[name])
    
    def create_buttons(self):
        """Create all buttons in the application"""
        button_configs = [
            ("btn_BackToHomepage", "btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_clicked),
            ("btn_ReturnBook", "btn_ReturnBook.png", 0.0, 219.0, 262.0, 25.0, self.on_return_book_clicked),
            ("btn_BorrowBook", "btn_BorrowBook.png", 0.0, 181.0, 262.0, 25.0, self.on_borrow_book_clicked),
            ("btn_PayFine", "btn_PayFine.png", 421.0, 382.0, 313.0, 48.0, self.on_pay_fine_clicked)
        ]
        
        for btn_name, img_name, x, y, width, height, command in button_configs:
            self.create_button(btn_name, img_name, x, y, width, height, command)
    
    def create_button(self, btn_name, image_name, x, y, width, height, command):
        """Helper method to create a button"""
        self.images[btn_name] = PhotoImage(file=self.relative_to_assets(image_name))
            
        button = Button(
            image=self.images[btn_name],
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
        setattr(self, btn_name, button)
        
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
    
    def on_pay_fine_clicked(self):
        """Handle pay fine button click"""
        print("btn_PayFine clicked")
        from View.noti_tab_view_1 import Message_2
        from Controller.return_controller import ReturnController
        message = Message_2(self.root, 'pay_fine')
        def custom_switch_to_borrowreturn():
            ReturnController.update_after_payment(self.receipt_id)
            self.root.destroy()
            from View.BorrowReturnBook.BorrowReturnBook import BorrowReturnApp
            borrow_return_root = Tk()
            borrow_return = BorrowReturnApp(borrow_return_root)
            borrow_return_root.mainloop()
        message.back_to_subfun = custom_switch_to_borrowreturn

        
    def load_due_and_fine_data(self):
        from Controller.return_controller import ReturnOverdueController
        if not self.receipt_id:
            print("Không có receipt_id!")
            return

        total_due_books, total_fine = ReturnOverdueController.calculate_due_and_fine(self.receipt_id)
        self.canvas.itemconfigure(self.lbl_Quantity, text=str(total_due_books))
        self.canvas.itemconfigure(self.lbl_Amount, text=f"{total_fine:,} VND")


if __name__ == "__main__":
    window = Tk()
    app = ReturnOverdueApp(window)
    window.mainloop()