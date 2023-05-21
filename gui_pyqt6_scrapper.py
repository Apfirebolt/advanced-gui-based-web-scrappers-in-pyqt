import sys
import requests
import os
from bs4 import *
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QWidget, \
    QLineEdit, QTextEdit, QComboBox, QMessageBox


# Maintain a user agent list to avoid getting banned from scrapping a website
user_agent_list = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 
]


class OpenFileWindow(QMainWindow):
    """
    This "window" is a QWidget. If it has no parent.
    """
    def __init__(self, soup, parent=None):
        super(OpenFileWindow, self).__init__(parent)
        mainLayout = QVBoxLayout()
        formLayout = QHBoxLayout()
        self.soup = soup
        self.folderLabel = QLabel("Please type the name of the folder :")
        self.folderText = QLineEdit('')
        formLayout.addWidget(self.folderLabel)
        formLayout.addWidget(self.folderText)
        confirmBtn = QPushButton('Confirm')
        confirmBtn.clicked.connect(self.processDownload)

        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(confirmBtn)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    
    def downloadImages(self, images, folderName):

        count = 0

        print(f"Total {len(images)} Image Found!")

        # checking if images is not zero
        if len(images) != 0:
            for i, image in enumerate(images):
            
                try:
                    # In image tag ,searching for "data-srcset"
                    image_link = image["data-srcset"]
                    
                # then we will search for "data-src" in img
                # tag and so on..
                except:
                    try:
                        # In image tag ,searching for "data-src"
                        image_link = image["data-src"]
                    except:
                        try:
                            # In image tag ,searching for "data-fallback-src"
                            image_link = image["data-fallback-src"]
                        except:
                            try:
                                # In image tag ,searching for "src"
                                image_link = image["src"]

                            # if no Source URL found
                            except:
                                pass

                # After getting Image Source URL
                # We will try to get the content of image
                try:
                    r = requests.get(image_link).content
                    try:

                        # possibility of decode
                        r = str(r, 'utf-8')

                    except UnicodeDecodeError:

                        # After checking above condition, Image Download start
                        with open(f"{folderName}/images{i+1}.jpg", "wb+") as f:
                            f.write(r)

                        # counting number of image downloaded
                        count += 1
                except:
                    pass

        
            if count == len(images):
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Info!")
                dlg.setText('All images were downloaded successfully')
                dlg.exec()
                self.close()
                
            # if all images not download
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Info!")
                dlg.setText(f"Total {count} Images Downloaded Out of {len(images)}")
                dlg.exec()
                self.close()
    

    def processDownload(self):
        if len(self.folderText.text()) == 0:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Info!")
            dlg.setText('Please give a name to the folder')
            dlg.exec()
        else: 
            try:
                folderName = self.folderText.text()
                os.mkdir(folderName)
            except Exception as err:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Error!")
                dlg.setText('Some error occurred while creating folder')
                dlg.exec()
                self.close()

            images = self.soup.findAll('img')
            self.downloadImages(images, folderName)
            

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selectedTag = None
        self.url = None
        self.setWindowTitle("A GUI Based Downloader and Web Scrapper")
        self.resize(1200, 800)
        self.tags = ['h1', 'h2', 'h3', 'h4', 'a', 'div', 'p', 'li', 'table', 'tr', 'td']
        self.scrapData = None
        self.soup = None

        # Styles
        self.buttonStyles = "background-color:#BBCCFF; padding: 8px; border-radius: 5px;"
        self.searchInput = QHBoxLayout()

        self.urlLabel = QLabel()
        self.urlLabel.setText('Enter the URL :')
        self.urlLabel.setStyleSheet("font-weight: 700; font-size: 18px;")
        self.searchInput.addWidget(self.urlLabel)

        self.urlTextField = QLineEdit()
        self.urlTextField.setStyleSheet("padding: 8px;")
        self.searchInput.addWidget(self.urlTextField)

        # Tag selection content
        self.tagSelectionContent = QHBoxLayout()
        self.tagSelectionLabel = QLabel('Select a Tag')
        self.tagSelectionLabel.setStyleSheet("font-weight: 700; font-size: 16px;")
        self.tagSelectionComboBox = QComboBox()
        self.tagSelectionComboBox.setStyleSheet(self.buttonStyles)
        self.searchTagBtn = QPushButton('Get All Tags')
        self.searchTagBtn.setStyleSheet(self.buttonStyles)
        self.searchTagBtn.clicked.connect(self.selectTags)

        for item in self.tags:
            self.tagSelectionComboBox.addItem(item)

        self.tagSelectionContent.addWidget(self.tagSelectionLabel)
        self.tagSelectionContent.addWidget(self.tagSelectionComboBox)
        self.tagSelectionContent.addWidget(self.searchTagBtn)

        self.bottomContent = QHBoxLayout()
        self.getResultBtn = QPushButton('Get Result')
        self.getResultBtn.setStyleSheet(self.buttonStyles)
        self.getResultBtn.clicked.connect(self.getScrapResult)
        self.downloadImagesBtn = QPushButton('Download Images')
        self.downloadImagesBtn.setStyleSheet(self.buttonStyles)
        self.downloadImagesBtn.clicked.connect(self.downloadImages)
        self.bottomContent.addWidget(self.getResultBtn)
        self.bottomContent.addWidget(self.downloadImagesBtn)

        self.getScrapBtn = QPushButton('Scrap')
        self.getScrapBtn.setStyleSheet(self.buttonStyles)
        self.getScrapBtn.clicked.connect(self.loadScrapData)
        self.bottomContent.addWidget(self.getScrapBtn)

        self.scrapResultField = QTextEdit()
        self.scrapResultField.setStyleSheet("background-color:white; padding: 16px;")

        self.pageLayout = QVBoxLayout()
        self.pageLayout.addLayout(self.searchInput)
        self.pageLayout.addWidget(self.scrapResultField)
        self.pageLayout.addLayout(self.tagSelectionContent)
        self.pageLayout.addLayout(self.bottomContent)


        widget = QWidget()
        widget.setLayout(self.pageLayout)
        self.setCentralWidget(widget)

    
    def loadScrapData(self):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"} 
            r = requests.get(self.urlTextField.text(), headers=headers)

            # Parse HTML Code
            self.soup = BeautifulSoup(r.text, 'html.parser')

            self.scrapResultField.setText(self.soup.prettify())
            self.scrapData = self.soup.prettify()
        except Exception as err:
            print('Some exception occurred', err)
            self.scrapResultField.setText('Some exception occurred')

        
    def selectTags(self):
        if len(self.scrapResultField.toPlainText()) == 0:
            self.openInfoDialog('No scrap data available, please use a link to get scrap data')
        else:
            selectedTag = self.tagSelectionComboBox.currentText()
            tags = self.soup.findAll(selectedTag)
            if len(tags) == 0:
                self.openInfoDialog('No tags found in the scrap result, try another tag')
                self.scrapResultField.setText('No tags found')
            else:
                output = ''
                for tag in tags:
                    output += (str(tag) + '\n')
                self.scrapResultField.setText(output)
            
    
    def getScrapResult(self):
        if self.soup is None:
            self.openInfoDialog('No scrap data found, please scrap a website')
        self.scrapResultField.setText(self.soup.prettify())


    def openInfoDialog(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Info!")
        dlg.setText(message)
        
        dlg.exec()

    
    def downloadImages(self):
        if len(self.scrapResultField.toPlainText()) == 0:
            self.openInfoDialog('No scrap data available, please use a link to get scrap data')
        else:
            downloadWindow = OpenFileWindow(self.soup, self)
            downloadWindow.show()
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
