from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

class BorrowReceiptApp:
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
        self.create_text_fields()
    
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
                    x, y, image=self.images[img_name]
                )
    
    def create_text_fields(self):
        """Create all text fields in the application"""
        text_configs = [
            (579.0, 107.0, "212", "lbl_ReceiptID"),
            (579.0, 175.0, "112", "lbl_UserID"),
            (579.0, 244.0, "0123456789", "lbl_ISBN"),
            (579.0, 312.0, "1", "lbl_Quantity"),
            (579.0, 380.0, "2025/03/21", "lbl_BorrowDate"),
            (579.0, 448.0, "2025/03/25", "lbl_ReturnDate")
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
            ("btn_Back.png", 424.0, 501.0, 313.0, 48.0, self.on_back_clicked)
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
    
    def on_return_book_clicked(self):
        """Handle return book button click"""
        print("btn_ReturnBook clicked")
    
    def on_borrow_book_clicked(self):
        """Handle borrow book button click"""
        print("btn_BorrowBook clicked")
    
    def on_back_clicked(self):
        """Handle back button click"""
        print("btn_Back clicked")


if __name__ == "__main__":
    window = Tk()
    app = BorrowReceiptApp(window)
    window.mainloop()