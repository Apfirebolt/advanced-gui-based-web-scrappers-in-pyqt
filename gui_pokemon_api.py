import sys
import aiohttp
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QWidget, \
    QLineEdit, QTextEdit, QComboBox, QMessageBox


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selectedTag = None
        self.threshold = 20
        self.setWindowTitle("A GUI Application for Pokemon Details")
        self.resize(1200, 800)
        self.scrapData = None
        self.soup = None

        # Styles
        self.buttonStyles = "background-color:#CCCCCC; padding: 8px; border-radius: 5px;"
        self.searchInput = QHBoxLayout()

        self.urlLabel = QLabel()
        self.urlLabel.setText('Enter the Url to Get Pokemon Details :')
        self.urlLabel.setStyleSheet("font-weight: 700; font-size: 18px;")
        self.searchInput.addWidget(self.urlLabel)

        self.urlTextField = QLineEdit()
        self.urlTextField.setStyleSheet("padding: 8px;")
        self.searchInput.addWidget(self.urlTextField)

        self.bottomContent = QHBoxLayout()

        self.getResultBtn = QPushButton('Get Pokemon Data')
        self.getResultBtn.setStyleSheet(self.buttonStyles)
        self.getResultBtn.clicked.connect(self.getAPIResponse)
        self.bottomContent.addWidget(self.getResultBtn)

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

    
    async def getApiData(self):
        async with aiohttp.ClientSession() as session:

            pokemon_url = self.urlTextField.text()

            if not pokemon_url.startswith("https://pokeapi.co/api/v2/pokemon"):
                self.openInfoDialog('Url is not valid')
            else:
                self.scrapResultField.setText('Loading...')
                async with session.get(pokemon_url) as resp:
                    pokemon = await resp.json()
                    self.scrapResultField.setText(str(pokemon))

    
    def getAPIResponse(self):
        asyncio.run(self.getApiData())

        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
