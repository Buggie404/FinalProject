from Borrow_Return import Ui_MainWindow

class BMI_Ext(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        self.stackedWidgetMain.setCurrentIndex(0)
        self.btnBorrowBook.clicked.connect(lambda: self.stackedWidgetMain.setCurrentIndex(1))
        self.stackedWidgetBorrowFuncs.setCurrentIndex(0)
        self.btnConfirmBorrowBook.clicked.connect(lambda: self.stackedWidgetBorrowFuncs.setCurrentIndex(3))
        self.btnPrintReceipt.clicked.connect(lambda: self.stackedWidgetBorrowFuncs.setCurrentIndex(4))
        self.btnAddMore.clicked.connect(lambda: self.stackedWidgetBorrowFuncs.setCurrentIndex(0))
        self.btnBackToBorrow.clicked.connect(lambda: self.stackedWidgetBorrowFuncs.setCurrentIndex(0))
        self.btnRedoBorrow.clicked.connect(lambda: self.stackedWidgetBorrowFuncs.setCurrentIndex(0))
        
    def search_books(self):
        available_books = 2
        if available_books > 0:
            self.btnSearchBorrowBook.clicked.connect(lambda: self.stackedWidgetBorrowFuncs.setCurrentIndex(1))
        else:
            self.btnSearchBorrowBook.clicked.connect(lambda: self.stackedWidgetBorrowFuncs.setCurrentIndex(2))