from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

class HomepageApp:
    def __init__(self, root, assets_path=None):
        self.root = root
        # self.role = "user"  # Default role
        self.role = "admin"
        self.root.geometry("898x605")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.output_path = Path(__file__).parent
        self.assets_path = Path(assets_path) if assets_path else self.output_path / Path("Ultilities/build/assets/frameHomepage")
        
        self.images = {}
        self.canvas = Canvas(self.root, bg="#FFFFFF", height=605, width=898, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        
        self.load_images()
        self.create_sidebar()
        self.create_main_buttons()
    
    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)
    
    def load_images(self):
        image_files = [
            "image_1.png",
            "btn_AccountManagement.png",
            "btn_UserManagement.png",
            "btn_BorrowReturnBook.png",
            "btn_BookManagement.png"
        ]
        
        for image_file in image_files:
            full_path = self.relative_to_assets(image_file)
            try:
                self.images[image_file] = PhotoImage(file=full_path)
            except Exception as e:
                print(f"Error loading image {full_path}: {e}")
    
    def create_sidebar(self):
        """Create sidebar with logo"""
        self.canvas.create_rectangle(0.0, 0.0, 299.0, 605.0, fill="#0A66C2", outline="")
        if "image_1.png" in self.images:
            self.canvas.create_image(149.0, 250.0, image=self.images["image_1.png"])
    
    def create_main_buttons(self):
        """Create main buttons on the homepage"""
        self.create_button("btn_AccountManagement.png", 348.0, 88.0, 228.0, 202.6666717529297, self.on_account_management_clicked)
        self.create_button("btn_UserManagement.png", 613.0, 88.0, 228.0, 203.0, self.on_user_management_clicked)
        self.create_button("btn_BorrowReturnBook.png", 480.0, 315.0, 228.0, 203.0, self.on_borrow_return_clicked)
        self.create_button("btn_BookManagement.png", 613.0, 315.0, 228.0, 203.0, self.on_book_management_clicked)
        
        self.update_ui_based_on_role()
    
    def update_ui_based_on_role(self):
        """Hide and show buttons based on admin role"""
        if hasattr(self, "btn_BookManagement"):
            if self.role == "admin":
                self.btn_BorrowReturnBook.place(x=348.0, y=315.0, width=228.0, height=203.0)
                self.btn_BookManagement.place(x=613.0, y=315.0, width=228.0, height=203.0)
            else:
                self.btn_BookManagement.place_forget()
    
    def create_button(self, image_name, x, y, width, height, command):
        if image_name not in self.images:
            print(f"Warning: Image {image_name} not found")
            return None
            
        button = Button(
            image=self.images[image_name], 
            borderwidth=0, 
            highlightthickness=0, 
            command=command, 
            relief="flat")
        
        button.place(x=x, y=y, width=width, height=height)
        
        button_name = image_name.replace(".png", "")
        if button_name.startswith("btn_"):
            setattr(self, button_name, button)
            
        return button
    
    def on_account_management_clicked(self):
        print("btn_AccountManagement clicked")
    
    def on_user_management_clicked(self):
        print("btn_UserManagement clicked")
    
    def on_borrow_return_clicked(self):
        print("btn_BorrowReturnBook clicked")
    
    def on_book_management_clicked(self):
        print("btn_BookManagement clicked")

if __name__ == "__main__":
    window = Tk()
    app = HomepageApp(window)
    window.mainloop()