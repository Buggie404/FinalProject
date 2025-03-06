from Homepage import Ui_MainWindow

class BMI_Ext(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
    
    def setPermissions(self, role):
        if role == "user":
            self.btnStatistics.setVisible(False)
            self.lbl_Statistics.setVisible(False)
            self.btnUsersManage.setVisible(False)
            self.lbl_UsersManage.setVisible(False)
        elif role == "admin":
            self.btnStatistics.setVisible(True)
            self.lbl_Statistics.setVisible(True)
            self.btnUsersManage.setVisible(True)
            self.lbl_UsersManage.setVisible(True)