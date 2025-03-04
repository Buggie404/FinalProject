from PyQt6.QtWidgets import QApplication, QMainWindow
from LogInEx import BMI_Ext
import sys

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

w = QMainWindow()
f = BMI_Ext()
f.setupUi(w)

w.show()
sys.exit(app.exec())