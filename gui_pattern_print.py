import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QWidget, \
    QLineEdit, QTextEdit, QComboBox, QMessageBox



# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selectedTag = None
        self.threshold = 20
        self.setWindowTitle("A GUI Print Pattern Tool")
        self.resize(1200, 800)
        self.scrapData = None
        self.soup = None

        # Styles
        self.buttonStyles = "background-color:#BBCCFF; padding: 8px; border-radius: 5px;"
        self.searchInput = QHBoxLayout()

        self.urlLabel = QLabel()
        self.urlLabel.setText('Enter the Number :')
        self.urlLabel.setStyleSheet("font-weight: 700; font-size: 18px;")
        self.searchInput.addWidget(self.urlLabel)

        self.urlTextField = QLineEdit()
        self.urlTextField.setStyleSheet("padding: 8px;")
        self.searchInput.addWidget(self.urlTextField)

        self.bottomContent = QHBoxLayout()
        self.getResultBtn = QPushButton('Print Diamond')
        self.getResultBtn.setStyleSheet(self.buttonStyles)
        self.getResultBtn.clicked.connect(self.printDiamond)
        self.triangleBtn = QPushButton('Print Triangle')
        self.triangleBtn.setStyleSheet(self.buttonStyles)
        self.triangleBtn.clicked.connect(self.printTriangle)

        self.rectangleBtn = QPushButton('Print Rectangle')
        self.rectangleBtn.setStyleSheet(self.buttonStyles)
        self.rectangleBtn.clicked.connect(self.printFilledRectangle)

        self.hollowRectangleBtn = QPushButton('Hollow Rectangle')
        self.hollowRectangleBtn.setStyleSheet(self.buttonStyles)
        self.hollowRectangleBtn.clicked.connect(self.printHollowRectangle)
        self.bottomContent.addWidget(self.getResultBtn)
        self.bottomContent.addWidget(self.rectangleBtn)
        self.bottomContent.addWidget(self.hollowRectangleBtn)
        self.bottomContent.addWidget(self.triangleBtn)

        self.halfDiamondBtn = QPushButton('Half Diamond')
        self.halfDiamondBtn.setStyleSheet(self.buttonStyles)
        self.halfDiamondBtn.clicked.connect(self.printLowTriangle)
        self.bottomContent.addWidget(self.halfDiamondBtn)

        self.scrapResultField = QTextEdit()
        self.scrapResultField.setStyleSheet("background-color:white; padding: 16px;")

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addLayout(self.searchInput)
        self.pageLayout.addWidget(self.scrapResultField)
        self.pageLayout.addLayout(self.bottomContent)


        widget = QWidget()
        widget.setLayout(self.pageLayout)
        self.setCentralWidget(widget)


    def openInfoDialog(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Info!")
        dlg.setText(message)
        
        dlg.exec()

    
    def printTriangle(self):
        number = int(self.urlTextField.text())
        if number > self.threshold:
            self.openInfoDialog('Please enter a value less than threshold')
        else:
            self.mountain(number)


    def printDiamond(self):
        number = int(self.urlTextField.text())
        if number > self.threshold:
            self.openInfoDialog('Please enter a value less than threshold')
        else:
            self.triangle(number)

    
    def printLowTriangle(self):
        number = int(self.urlTextField.text())
        if number > self.threshold:
            self.openInfoDialog('Please enter a value less than threshold')
        else:
            self.lowTriangle(number)

    
    def printFilledRectangle(self):
        number = int(self.urlTextField.text())
        if number > self.threshold:
            self.openInfoDialog('Please enter a value less than threshold')
        else:
            self.filledRectangle(number)

    def printHollowRectangle(self):
        number = int(self.urlTextField.text())
        if number > self.threshold:
            self.openInfoDialog('Please enter a value less than threshold')
        else:
            self.hollowRectangle(number)

    def triangle(self, n):
     
        # number of spaces
        k = n - 1
        result  = ''
        # outer loop to handle number of rows
        for i in range(0, n):
        
            for j in range(0, k):
                result += " "
        
            # decrementing k after each loop
            k = k - 1
        
            for j in range(0, i+1):
            
                # printing stars
                result += "* "
        
            # ending line after each row
            result += "\n"

        k = 1
        for i in range(0, n):

            for j in range(0, k):
                result += " "
            
            for j in range(k, n):
                result += "* "
            
            result += "\n"
            k += 1
        
        self.scrapResultField.setText(result)


    def mountain(self, n):
        i = 1

        result = ""
        while i < n:
            for j in range(0, i):
                result += "*"
            result += "\n"
            i += 1


        while i > 0:
            for j in range(i, 0, -1):
                result += "*"
            result += "\n"
            i -= 1
        
        self.scrapResultField.setText(result)

    
    def lowTriangle(self, n):
        i = 0

        result = ""
        for j in range(n):

            for k in range(i):
                result += " "
            
            for l in range(i, n):
                result += "* "
            
            i += 1
            result += "\n"

        self.scrapResultField.setText(result)


    def filledRectangle(self, n):
        result = ""
        for i in range(n):

            for j in range(n):
                result += "* "

            result += "\n"
        
        self.scrapResultField.setText(result)

    
    def hollowRectangle(self, n):
        result = ""
        indices = [0, n-1]
        
        for i in range(n):
            for j in range(n):
                if i in indices:
                    result += "* "
                else:
                    if j == 0:
                        result += "* "
                    else:
                        result += " "

            result += "\n"
        
        self.scrapResultField.setText(result)

        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
