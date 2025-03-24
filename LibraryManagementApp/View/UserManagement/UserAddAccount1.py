from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import sys
import os

class UserAddAccount1App:
    def __init__(self, root, user_id=None, user_data = None,  role=None, assets_path=None):
        self.root = root
        self.root.geometry("898x605+0+0")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        self.user_id = user_id  # Store the user ID

        from Model.user_model import User
        self.user_data = user_data if user_data else User.get_id(self.user_id)  
              
        if self.user_data and len(self.user_data) > 6 and self.user_data[6] == "Admin":
            self.role = "admin"
        else:
            self.role = None or "user"

        # Set up asset paths
        self.output_path = Path(__file__).parent
        # Allow assets_path to be configurable
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            self.assets_path = self.output_path.parent / Path(r"Ultilities/build/assets/frameUserAddAccount1")
        
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

        # Load user data if a user_id was provided
        if self.user_id:
            self.load_user_data()
    
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
        self.images["image_1"] = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(
            130.0,
            74.0,
            image=self.images["image_1"]
        )
    
    def create_main_content(self):
        """Create the main content area with background"""
        self.create_rounded_rectangle(
            285.0,
            39.0,
            871.0,
            567.0,
            color="#F1F1F1",
            radius=10
        )
        
        # Header image
        self.images["image_2"] = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(
            577.0,
            70.0,
            image=self.images["image_2"]
        )
    
    def create_text_fields(self):
        """Create all text fields in the application"""
        text_configs = [
            (577.0, 107.0, "170", "#0A66C2", ("Montserrat Medium", 18 * -1), "lbl_UserID"),
            (577.0, 175.0, "Adam Smith", "#0A66C2", ("Montserrat Medium", 18 * -1), "lbl_Name"),
            (577.0, 244.0, "smitha0170", "#0A66C2", ("Montserrat Medium", 18 * -1), "lbl_Username"),
            (577.0, 312.0, "smitha0170@user.libma", "#0A66C2", ("Montserrat Medium", 18 * -1), "lbl_Email"),
            (577.0, 380.0, "User", "#0A66C2", ("Montserrat Medium", 18 * -1), "lbl_Role"),
            (577.0, 448.0, "2005/12/30", "#0A66C2", ("Montserrat Medium", 18 * -1), "lbl_DateOfBirth")
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
            ("image_3", "image_3.png", 367.0, 117.0),
            ("image_4", "image_4.png", 382.0, 185.0),
            ("image_5", "image_5.png", 402.0, 253.0),
            ("image_6", "image_6.png", 375.0, 389.0),
            ("image_7", "image_7.png", 412.0, 457.0),
            ("image_8", "image_8.png", 381.0, 321.0)
        ]
        
        for name, file, x, y in image_configs:
            self.images[name] = PhotoImage(file=self.relative_to_assets(file))
            self.canvas.create_image(x, y, image=self.images[name])
    
    def create_buttons(self):
        """Create all buttons in the application"""
        button_configs = [
            ("btn_BackToHomepage", "btn_BackToHomepage.png", 0.0, 563.0, 261.0, 25.0, self.on_back_to_homepage_clicked),
            ("btn_AddAccount", "btn_AddAccount.png", 0.0, 181.0, 262.0, 25.0, self.on_add_account_clicked),
            ("btn_EditAccountPassword", "btn_EditAccountPassword.png", 0.0, 219.0, 262.0, 25.0, self.on_edit_account_password_clicked),
            ("btn_Return", "btn_Return.png", 421.0, 501.0, 313.0, 48.0, self.on_return_clicked)
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
        from Homepage import HomepageApp
        homepage_root = Tk()
        homepage = HomepageApp(homepage_root, role = self.role, user_data=self.user_data)
        homepage_root.mainloop()
    
    def on_add_account_clicked(self):
        """Handle add account button click"""
        print("btn_AddAccount clicked")
        self.root.destroy()
        from UserAddAccount import UserAddAccountApp
        add_user_root = Tk()
        add_user = UserAddAccountApp(add_user_root, user_data=self.user_data)
        add_user_root.mainloop()
    
    def on_edit_account_password_clicked(self): # Cannot switch to Edit Account while Adding Account
        """Handle edit account password button click"""
        print("btn_EditAccountPassword clicked")
        pass
    
    def on_return_clicked(self):
        """Handle return button click"""
        print("btn_Return clicked")
        self.root.destroy()
        from View.UserManagement.UserManagement import UserManagementApp
        add_user_root = Tk()
        add_user = UserManagementApp(add_user_root, user_data=self.user_data)
        add_user_root.mainloop()
    
    def load_user_data(self):
        """Load user data from the database and update UI labels"""
        # Import necessary modules
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from Model.user_model import User
        
        # Get user data
        user_data = User.get_id(self.user_id)
        
        if user_data:
            # Update labels with user data
            # Print the user_data to debug what's being returned
            print(f"User data from database: {user_data}")
            
            # Check the structure of user_data and extract fields accordingly
            # Assuming user_data is a tuple with fields in order of the database columns:
            user_id, name, username, email, password, date_of_birth, role = user_data
            
            # Update the text of the text fields
            self.canvas.itemconfig(self.lbl_UserID, text=str(user_id))
            self.canvas.itemconfig(self.lbl_Name, text=name)
            self.canvas.itemconfig(self.lbl_Username, text=username)
            self.canvas.itemconfig(self.lbl_Email, text=email)
            self.canvas.itemconfig(self.lbl_Role, text=role)
            self.canvas.itemconfig(self.lbl_DateOfBirth, text=date_of_birth)

if __name__ == "__main__":
    window = Tk()
    app = UserAddAccount1App(window)
    window.mainloop()