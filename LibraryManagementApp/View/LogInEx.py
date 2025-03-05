from Homepage import Ui_MainWindow

class BMI_Ext(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
    
    def setPermissions(self, role):
        if role == "user":
            self.btnBooksManage.setVisible(False)
            self.lbl_BooksManage.setVisible(False)
            self.btnUsersManage.setVisible(False)
            self.lbl_UsersManage.setVisible(False)
        elif role == "admin":
            self.btnBooksManage.setVisible(True)
            self.lbl_BooksManage.setVisible(True)
            self.btnUsersManage.setVisible(True)
            self.lbl_UsersManage.setVisible(True)