from PyQt6.QtWidgets import QApplication, QMainWindow
from BorrowEx import BMI_Ext
import sys

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

w = QMainWindow()
f = BMI_Ext()
f.setupUi(w)

"""Code gọi hàm phân loại role ở Log In"""
# # role = "user"
# role = "admin"
# f.setPermissions(role)

"""Code check available book ở function Borrow -> code thêm connect với db"""
f.search_books()

w.show()
sys.exit(app.exec())