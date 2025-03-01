

from globals import *



class TextBox(QObject):

    def __init__ (self, parent, pos, i, textBoxNum, pixmap, label):
        super().__init__()

        self.fresh = True;
        self.clicked = False
        self.parent = parent

        fontHeight = QFontMetrics(QFont(parent.font)).height()

        self.sizeX = 0
        self.sizeY = 0

        self.label = label
        self.pixmap = pixmap
        self.index = textBoxNum
        self.topLeftPos = QPoint(pos.x()-10, pos.y()-10)
        self.topRightPos = QPoint(pos.x()+self.sizeX, pos.y()-10)
        self.bottomLeftPos = QPoint(pos.x()-10, pos.y()+self.sizeY)
        self.bottomRightPos = QPoint(pos.x()+self.sizeX, pos.y()+self.sizeY)

        self.topLeft = self.createDot(self.topLeftPos, parent.pages[i])
        self.topRight = self.createDot(self.topRightPos,parent.pages[i]);
        self.bottomLeft = self.createDot(self.bottomLeftPos,parent.pages[i]);
        self.bottomRight = self.createDot(self.bottomRightPos,parent.pages[i]);

        self.addListeners(self.topLeft)
        self.addListeners(self.topRight)
        self.addListeners(self.bottomLeft)
        self.addListeners(self.bottomRight)



        self.initialPosition = pos
        self.movingPosition = pos

        self.iTL = self.topLeftPos
        self.iTR = self.topRightPos
        self.iBL = self.bottomLeftPos
        self.iBR = self.bottomRightPos

        self.mTL = self.topLeftPos
        self.mTR = self.topRightPos
        self.mBL = self.bottomLeftPos
        self.mBR = self.bottomRightPos



        self.textEdit = QTextEdit(parent.pages[i])
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.textEdit.setLineWrapMode(1);
        self.textEdit.setWordWrapMode(2);

        self.textEdit.document().setDocumentMargin(0)

        self.font = parent.font
        self.fontSize = parent.fontSize
        self.textEdit.setCurrentFont(QFont(self.font,self.fontSize))

        self.textEdit.mousePressEvent = lambda event: self.saveInitialOffsetBox(event)
        self.textEdit.mouseReleaseEvent = lambda event: self.actionDragFinBox(event)
        self.textEdit.mouseMoveEvent = lambda event: self.actionDragBox(event);



        self.textEdit.move(pos)
        self.textEdit.resize(self.sizeX, self.sizeY)
        self.textEdit.setStyleSheet("background: rgba(100,0,0,10%)")

        self.textEdit.show()


        self.cancel = QPushButton(QIcon('icons/x.png'),"",parent.pages[i])

        self.cancel.move(QPoint(self.topRightPos.x(), self.topRightPos.y())) 
        self.cancel.resize(20,20)
        self.cancel.show()

        self.cancel.mousePressEvent = lambda event: self.__del__()


    def createDot(self, pos, parent):
        label = QLabel(parent)
        label.move(pos)
        label.resize(10,10)
        label.setStyleSheet("background: rgba(100,0,0,100%)")
        label.show()



        return label

    def addListeners(self, obj):
        obj.mousePressEvent = lambda event: self.saveInitialPosition(event, obj)
        obj.mouseReleaseEvent = lambda event: self.actionDragFin(event, obj)
        obj.mouseMoveEvent = lambda event: self.actionDrag(event, obj);


    def saveInitialOffsetBox(self, event):
        self.clicked = True
        self.initialPosition = self.topLeftPos
        self.movingPosition = self.initialPosition

        self.iTL = self.topLeftPos - event.pos()
        self.iTR = self.topRightPos - event.pos()
        self.iBL = self.bottomLeftPos - event.pos()
        self.iBR = self.bottomRightPos - event.pos()


    def actionDragBox(self, event):
        if self.clicked == True:
            print(self.movingPosition)
            print(event.pos())

            self.topLeftPos = self.iTL + event.pos()
            self.topRightPos = self.iTR + event.pos()
            self.bottomLeftPos = self.iBL + event.pos()
            self.bottomRightPos = self.iBR + event.pos()

            self.topLeft.move(self.iTL + event.pos())
            self.topRight.move(self.iTR + event.pos())
            self.bottomLeft.move(self.iBL + event.pos())
            self.bottomRight.move(self.iBR + event.pos())


    def actionDragFinBox(self, event):
        self.clicked = False
        finPos = self.iTL + event.pos()
        finPos = QPoint(finPos.x()+10, finPos.y()+10)
        self.textEdit.move(finPos)
        self.cancel.move(QPoint(self.topRightPos.x(), self.topRightPos.y()))



    def actionDrag(self, event, obj):


        if(not self.fresh):
   
            self.movingPosition = self.movingPosition + event.pos()
        else:
            self.movingPosition = event.pos()

        obj.move(self.movingPosition)




    def actionDragFin(self, event, obj):
        self.clicked = False

        if(not self.fresh):
            pos = self.movingPosition + event.pos()
        else:
            pos = event.pos()

        obj.move(pos)
        offsetX = pos.x() - self.initialPosition.x()
        offsetY = pos.y() - self.initialPosition.y()
        if(obj is self.topLeft):
            self.topLeftPos = pos
            self.topRightPos = QPoint(self.topRightPos.x(), self.topRightPos.y()+offsetY)
            self.bottomLeftPos = QPoint(self.bottomLeftPos.x()+offsetX, self.bottomLeftPos.y())
            self.topRight.move(self.topRightPos)
            self.bottomLeft.move(self.bottomLeftPos)
            self.textEdit.move(QPoint(self.topLeftPos.x()+10, self.topLeftPos.y()+10))
            self.sizeX = self.sizeX - offsetX
            self.sizeY = self.sizeY - offsetY
            self.textEdit.resize(self.sizeX, self.sizeY)

        elif(obj is self.topRight):
            self.topRightPos = pos
            self.bottomRightPos = QPoint(self.bottomRightPos.x()+offsetX, self.bottomRightPos.y())
            self.topLeftPos = QPoint(self.topLeftPos.x(), self.topLeftPos.y()+offsetY)
            self.bottomRight.move(self.bottomRightPos)
            self.topLeft.move(self.topLeftPos)
            self.textEdit.move(QPoint(self.topLeftPos.x()+10, self.topLeftPos.y()+10))
            self.sizeX = self.sizeX + offsetX
            self.sizeY = self.sizeY - offsetY
            self.textEdit.resize(self.sizeX, self.sizeY)

        elif(obj is self.bottomLeft):
            self.bottomLeftPos = pos
            self.bottomRightPos = QPoint(self.bottomRightPos.x(), self.bottomRightPos.y()+offsetY)
            self.topLeftPos = QPoint(self.topLeftPos.x()+offsetX, self.topLeftPos.y())
            self.bottomRight.move(self.bottomRightPos)
            self.topLeft.move(self.topLeftPos)
            self.textEdit.move(QPoint(self.topLeftPos.x()+10, self.topLeftPos.y()+10))
            self.sizeX = self.sizeX - offsetX
            self.sizeY = self.sizeY + offsetY
            self.textEdit.resize(self.sizeX, self.sizeY)

        elif(obj is self.bottomRight):
            self.bottomRightPos = pos
            self.topRightPos = QPoint(self.topRightPos.x()+offsetX, self.topRightPos.y())
            self.bottomLeftPos = QPoint(self.bottomLeftPos.x(), self.bottomLeftPos.y()+offsetY)
            self.topRight.move(self.topRightPos)
            self.bottomLeft.move(self.bottomLeftPos)
            self.sizeX = self.sizeX + offsetX
            self.sizeY = self.sizeY + offsetY
            self.textEdit.resize(self.sizeX, self.sizeY)

        else:
            print("actionDragFin Error")
        obj.show()
        self.cancel.move(QPoint(self.topRightPos.x(), self.topRightPos.y()))
        print(self.textEdit.toPlainText())

    def saveInitialPosition(self, event, obj):

        if(obj is self.topLeft):
            self.initialPosition = self.topLeftPos
        elif(obj is self.topRight):
            self.initialPosition = self.topRightPos
        elif(obj is self.bottomLeft):
            self.initialPosition = self.bottomLeftPos
        elif(obj is self.bottomRight):
            self.initialPosition = self.bottomRightPos
        else:
            print("saveInitialPosition Error")
        self.movingPosition = self.initialPosition

    def __del__(self):
        print("deleted\n")
        self.topLeft.deleteLater()
        self.topRight.deleteLater()
        self.bottomLeft.deleteLater()
        self.bottomRight.deleteLater()
        self.textEdit.deleteLater()
        self.cancel.deleteLater()
        self.parent.boxFields[self.index] = None
