from globals import *
from app import *

class LeftPanel(QWidget):
    def __init__(self, parent):
        #https://pythonspot.com/pyqt5-tabs/

        super().__init__()
        self.imgLists = parent.imgLists
        self.layout = QGridLayout()



        self.scrollArea = QScrollArea(self)
        self.scrollArea.resize(500,parent.height)
        self.show()

        




class Pages(QWidget):
    def __init__(self, parent, pageNum):
        super().__init__()
        self.label = QLabel("page" + str(pageNum), parent)
        self.label.show()

class PageHolders(QWidget):
    def __init__(self, parent, pageHolderNum):
        super().__init__()
        self.label = QLabel("insert" + str(pageNum), parent)
        self.label.show()
