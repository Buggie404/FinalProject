from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

class Borrow2App:
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
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBorrow2")
        
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
    
    def relative_to_assets(self, path: str) -> Path:
        """Convert relative asset path to absolute path"""
        return self.assets_path / Path(path)
    
    def load_images(self):
        """Load all required images"""
        image_files = [
            "image_1.png",
            "image_2.png",
            "image_3.png",
            "image_4.png",
            "image_5.png",
            "image_7.png",
            "lnE_BorrowedNumber.png",
            "btn_BackToHomepage.png",
            "btn_ReturnBook.png",
            "btn_BorrowBook.png",
            "btn_Confirm.png"
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
        if "image_7.png" in self.images:
            self.canvas.create_image(
                130.0,
                73.0,
                image=self.images["image_7.png"]
            )
    
    def create_main_content(self):
        """Create the main content area with entries and labels"""
        # Background rectangle
        self.create_rounded_rectangle(
            285.0,
            80.0,
            871.0,
            525.0,
            radius=10,
            color="#F1F1F1"
        )
        
        # Header image
        if "image_1.png" in self.images:
            self.canvas.create_image(
                578.0,
                118.0,
                image=self.images["image_1.png"]
            )
        
        # Other images
        for img_name, x, y in [
            ("image_2.png", 381.0, 200.0),
            ("image_3.png", 366.0, 263.0),
            ("image_4.png", 401.0, 395.0),
            ("image_5.png", 410.0, 326.0)
        ]:
            if img_name in self.images:
                self.canvas.create_image(
                    x, y, image=self.images[img_name]
                )
        
        # Text fields
        self.lbl_ID = self.canvas.create_text(
            542.0,
            188.0,
            anchor="nw",
            text="000",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )
        
        self.lbl_ISBN = self.canvas.create_text(
            542.0,
            251.0,
            anchor="nw",
            text="123456789",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )
        
        self.lbl_AvailableQuantities = self.canvas.create_text(
            542.0,
            314.0,
            anchor="nw",
            text="0",
            fill="#0A66C2",
            font=("Montserrat Medium", 18 * -1)
        )
        
        # Create entry field
        self.create_entry(
            "lnE_BorrowedNumber.png",
            684.5,
            395.0,
            554.0,
            371.0,
            261.0,
            46.0
        )
    
    def create_entry(self, image_name, img_x, img_y, entry_x, entry_y, width, height):
        """Helper method to create an entry field with background image"""
        if image_name in self.images:
            self.canvas.create_image(
                img_x,
                img_y,
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
        
        # Store entry reference
        self.lnE_BorrowedNumber = entry
        
        return entry
    
    def create_buttons(self):
        """Create all buttons in the application"""
        button_configs = [
            ("btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_clicked),
            ("btn_ReturnBook.png", 0.0, 219.0, 262.0, 25.0, self.on_return_book_clicked),
            ("btn_BorrowBook.png", 0.0, 181.0, 262.0, 25.0, self.on_borrow_book_clicked),
            ("btn_Confirm.png", 421.0, 456.0, 313.0, 48.0, self.on_confirm_clicked)
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
    
    def on_confirm_clicked(self):
        """Handle confirm button click"""
        print("btn_Confirm clicked")


if __name__ == "__main__":
    window = Tk()
    app = Borrow2App(window)
    window.mainloop()