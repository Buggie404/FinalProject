from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

class ReturnOverdueApp:
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
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameReturnOverdue")
        
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
        self.create_buttons()
    
    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)
    
    def load_images(self):
        """Load all image assets"""
        image_files = [
            "image_1.png",
            "image_3.png",
            "image_4.png",
            "btn_BackToHomepage.png",
            "btn_ReturnBook.png",
            "btn_BorrowBook.png",
            "btn_PayFine.png"
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
        
        # Overdue fine table
        self.tbl_OverdueFine = self.canvas.create_rectangle(
            395.0,
            193.0,
            760.0,
            417.0,
            fill="#D9D9D9",
            outline=""
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
        
        # Logo images  
        if "image_3.png" in self.images:
            self.image_3 = self.canvas.create_image(
                130.0,
                73.0,
                image=self.images["image_3.png"]
            )
        
        # Create sidebar buttons
        self.create_button("btn_BorrowBook.png", 0.0, 181.0, 262.0, 25.0, self.on_borrow_book_click)
        self.create_button("btn_ReturnBook.png", 0.0, 219.0, 262.0, 25.0, self.on_return_book_click)
        self.create_button("btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_click)
    
    def create_main_content(self):
        """Create the main content area with images"""
        # Header images
        if "image_1.png" in self.images:
            self.image_1 = self.canvas.create_image(
                578.0,
                118.0,
                image=self.images["image_1.png"]
            )
        
        if "image_4.png" in self.images:
            self.image_4 = self.canvas.create_image(
                578.0,
                162.0,
                image=self.images["image_4.png"]
            )
    
    def create_buttons(self):
        """Create action buttons"""
        self.create_button("btn_PayFine.png", 421.0, 456.0, 313.0, 48.0, self.on_pay_fine_click)
    
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
    
    def on_pay_fine_click(self):
        print("btn_PayFine clicked")
        # Implement pay fine functionality here

# Entry point
if __name__ == "__main__":
    window = Tk()
    app = ReturnOverdueApp(window)
    window.mainloop()