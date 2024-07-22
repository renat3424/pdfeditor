from globals import *
from app import *
from textBox import *
from rect import *
from leftpanel import *

class TabMan(QWidget):
    def __init__(self, parent):

        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout(self)

        self.imgLists = parent.imgLists
        self.fileNames = parent.fileNames
        self.tabList = []
        self.tabManager = QTabWidget()
        self.tabManager.setTabsClosable(True)
        self.tabManager.tabCloseRequested.connect(self.closeTab)


        self.height = parent.height


        self.layout.addWidget(self.tabManager)

        self.scenes = []
        self.views = []

        self.show()

    def closeTab(self,idx):
        del self.imgLists[idx]
        del self.fileNames[idx]
        del self.tabList[idx]

        self.tabManager.removeTab(idx)


    def addTab(self, images):
        idx = len(self.tabList) 

        self.tabList.append(PdfDisplay(self.parent))
        self.tabList[idx].addPdfTab(images)
   
        self.tabManager.addTab(self.tabList[idx], self.fileNames[idx])

    def getPdfDisplay(self, idx):
        return self.tabList[idx]

    def getIdx(self):
        return self.tabManager.currentIndex()

class PdfDisplay(QWidget):



    def __init__(self, parent):

        super().__init__()
        self.layout = QVBoxLayout(self)
        self.images = []
        self.pixmaps = []
        self.labels = []
        self.boxFields = []
        self.pageForms = [] #layouts
        self.pages = []
        self.boxFieldNum = 0


        self.font = parent.globalFont
        self.italic = False;
        self.fontSize = parent.globalFontSize



    def textBoxConfirmed(self):


        for textBox in self.boxFields:
            if textBox == None:
                continue
            x = textBox.topLeftPos.x()
            y = textBox.topLeftPos.y()
            width = textBox.textEdit.frameGeometry().width()
            height = textBox.textEdit.frameGeometry().height()
            text = textBox.textEdit.toPlainText()

            rect = QRectF(x, y, width, height);
            painter = QPainter(textBox.pixmap)
            painter.begin(self)
            painter.setFont(QFont(textBox.font, textBox.fontSize))


            option = QTextOption();
            option.QWrapMode = QTextOption.WordWrap;
            painter.drawText(rect, text, option)
            textBox.label.setPixmap(textBox.pixmap)

            textBox.__del__()
            painter.end()

    def textBoxCanceled(self):
        for textBox in self.boxFields:
            if textBox == None:
                continue
            textBox.__del__()



    def mousePressEventL(self, event, i, label, pixmap):
        global editMode
        print("editMode:",editMode)
        if(editMode==False):
            return


        pos = event.pos()


        self.boxFields.append(TextBox(self, pos, i, self.boxFieldNum, pixmap, label))
        self.boxFieldNum+=1

    def mouseMoveEventL(self, event, i, label, pixmap):
        selected = self.boxFields[self.boxFieldNum-1];

        selected.actionDrag(event, selected.bottomRight)

    def mouseReleaseEventL(self, event, i, label, pixmap):
        selected = self.boxFields[self.boxFieldNum-1];
        selected.actionDragFin(event, selected.bottomRight)
        selected.fresh = False;


    def attachMousePressEvent(self, i):
        self.labels[i].mousePressEvent = lambda event: self.mousePressEventL(event, i, self.labels[i], self.pixmaps[i])
        self.labels[i].mouseMoveEvent = lambda event: self.mouseMoveEventL(event, i, self.labels[i], self.pixmaps[i])
        self.labels[i].mouseReleaseEvent = lambda event: self.mouseReleaseEventL(event, i, self.labels[i], self.pixmaps[i])



    def addPdfTab(self, images):

        pdfWidget = QWidget()
        imageSet = QVBoxLayout(pdfWidget)
        self.images = images


        for i in range(0, len(images)):
            page = QWidget()
            pageLayout = QVBoxLayout(page)
            self.pageForms.append(pageLayout)
            self.pages.append(page)

            label = QLabel(self)
            pixmap = QPixmap(images[i])


            label.setGeometry(0,0,10,10)
            label.setPixmap(pixmap)
            label.hasScaledContents();


            self.pageForms[i].addWidget(label)

            self.pixmaps.append(pixmap)
            self.labels.append(label)
            imageSet.addWidget(page) 

        for i in range(0, len(self.labels)):
            self.attachMousePressEvent(i);




        pdfWidget.layout = imageSet

        self.pdfScroll = QScrollArea()
        self.pdfScroll.setWidget(pdfWidget)
        self.pdfScroll.setWidgetResizable(True)

        self.layout.addWidget(self.pdfScroll)

        self.pdfScroll.show();
