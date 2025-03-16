from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
import os
import sys
from Homepage import HomepageApp 


class LogInApp:
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
            # Fix path
            self.assets_path = self.output_path / Path(r"Ultilities/build/assets/frameLogIn")
        
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
        self.create_login_button()
    
    def relative_to_assets(self, path: str) -> Path:
        """Convert relative asset path to absolute path"""
        return self.assets_path / Path(path)
    
    def load_images(self):
        """Load all required images"""
        image_files = [
            "lnE_Email.png", 
            "lnE_Password.png", 
            "btn_LogIn.png", 
            "image_1.png", 
            "image_2.png"
        ]
        
        for image_file in image_files:
            full_path = self.relative_to_assets(image_file)
            print(f"Loading image: {full_path}")
            try:
                self.images[image_file] = PhotoImage(file=full_path)
            except Exception as e:
                print(f"Error loading image {full_path}: {e}")
    
    def create_sidebar(self):
        """Create the blue sidebar rectangle and its content"""
        self.canvas.create_rectangle(
            0.0,
            0.0,
            299.0,
            605.0,
            fill="#0A66C2",
            outline=""
        )
        
        # Add Logo
        if "image_1.png" in self.images:
            self.canvas.create_image(
                149.0,
                250.0,
                image=self.images["image_1.png"]
            )
    
    def create_main_content(self):
        """Create the main content area with entry fields and header image"""
        # Create header image
        if "image_2.png" in self.images:
            self.canvas.create_image(
                606.0,
                147.0,
                image=self.images["image_2.png"]
            )
        
        # Create email entry
        self.create_entry(
            "lnE_Email.png", 
            600.5, 
            317.0, 
            464.0, 
            293.0, 
            273.0, 
            46.0
        )
        
        # Create password entry
        self.create_entry(
            "lnE_Password.png", 
            600.5, 
            404.0, 
            464.0, 
            380.0, 
            273.0, 
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
        
        is_password = "Password" in image_name
        
        entry = Entry(
            bd=0,
            bg="#E7DCDC",
            fg="#000716",
            highlightthickness=0,
            show="•" if is_password else ""
        )
        
        entry.place(
            x=entry_x,
            y=entry_y,
            width=width,
            height=height
        )
        
        # Store reference to entry fields for later access
        if image_name == "lnE_Email.png":
            self.lnE_Email = entry
        elif image_name == "lnE_Password.png":
            self.lnE_Password = entry
            
        return entry
    
    def create_login_button(self):
        """Create the login button"""
        if "btn_LogIn.png" in self.images:
            self.create_button(
                "btn_LogIn.png",
                444.0,
                467.0,
                313.0,
                48.0,
                self.on_login_clicked
            )
    
    def create_button(self, image_name, x, y, width, height, command):
        """Helper method to create a button"""
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
        
        # Store reference to login button
        if image_name == "btn_LogIn.png":
            self.btn_LogIn = button
            
        return button
    
    def on_login_clicked(self):
        """Handle login button click event"""
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(parent_dir)
        from Controller.auth_controller import check_account_login
        print("btn_LogIn clicked")
        email = self.lnE_Email.get()
        password = self.lnE_Password.get()

        success, user_data = check_account_login(email, password)

        if success:  # if account is valid -> cho chuyển sang Homepage
            self.root.destroy()
            homepage_root = Tk()
            homepage = HomepageApp(homepage_root)
            homepage_root.mainloop()
        else:  # else -> cho hiện Invalid(self.root, 'account')
            from noti_tab_view_1 import Invalid
            Invalid(self.root, 'account')




if __name__ == "__main__":
    window = Tk()
    app = LogInApp(window)
    window.mainloop()