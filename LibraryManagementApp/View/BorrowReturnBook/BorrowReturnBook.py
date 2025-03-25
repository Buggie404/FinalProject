from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import sys
import os

class BorrowReturnApp:
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
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameBorrowReturnBook")

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
        self.create_sidebar()
        self.create_main_buttons()
        
        self.root.mainloop()
    
    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)
    
    def load_images(self):
        image_files = [
            "btn_BackToHomepage.png",
            "btn_ReturnBook.png",
            "btn_BorrowBook.png",
            "image_1.png",
            "image_2.png"
        ]
        
        for image_file in image_files:
            full_path = self.relative_to_assets(image_file)
            try:
                self.images[image_file] = PhotoImage(file=full_path)
            except Exception as e:
                print(f"Error loading image {full_path}: {e}")
    
    def create_sidebar(self):
        self.canvas.create_rectangle(0.0, 0.0, 262.0, 605.0, fill="#0A66C2", outline="")
        
        if "image_1.png" in self.images:
            self.canvas.create_image(130.0, 73.0, image=self.images["image_1.png"])
        
        if "image_2.png" in self.images:
            self.canvas.create_image(587.0, 387.0, image=self.images["image_2.png"])
    
    def create_main_buttons(self):
        self.create_button("btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_clicked)
        self.create_button("btn_ReturnBook.png", 0.0, 219.0, 262.0, 25.0, self.on_return_book_clicked)
        self.create_button("btn_BorrowBook.png", 0.0, 181.0, 262.0, 25.0, self.on_borrow_book_clicked)
    
    def create_button(self, image_name, x, y, width, height, command):
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
        return button
    
    def on_back_to_homepage_clicked(self):
        self.root.destroy()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(base_dir, "View"))
        sys.path.append(base_dir)
        from View.Homepage import HomepageApp
        homepage_root = Tk()
        homepage = HomepageApp(homepage_root,role=self.role, user_data=self.user_data)
        homepage_root.mainloop()

    def on_borrow_book_clicked(self):
        self.root.destroy()
        from View.BorrowReturnBook.Borrow1 import Borrow1App
        borrow1_root = Tk()
        borrow1 = Borrow1App(borrow1_root, user_data=self.user_data)
        borrow1_root.mainloop()

    def on_return_book_clicked(self):
        self.root.destroy()
        from View.BorrowReturnBook.Return1 import Return1App
        return1_root = Tk()
        return1 = Return1App(return1_root, user_data=self.user_data)
        return1_root.mainloop()

if __name__ == "__main__":
    window = Tk()
    app = BorrowReturnApp(window)
    window.mainloop()