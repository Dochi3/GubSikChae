from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QTextEdit, QLabel
from PyQt5.QtGui import QFontMetrics
import time

class CodeBlock(QWidget):
    def __init__(self, parent=None, code=str()):
        super().__init__()
        self.parent = parent
        self.focusedTime = time.time()
        # GridLayout for CodeBlock
        glCodeBlock = QGridLayout()

        # Label for focused
        self.lbIsFocused = QLabel(" ")

        # Label for Block Execute Number
        self.lbBlockNumber = QLabel()
        self.lbBlockNumber.setAlignment(Qt.AlignTop)
        self.setNumber()

        # TextEdit for editing code
        self.teCodeBox = QTextEdit()
        self.teCodeBox.setMinimumWidth(800)
        self.teCodeBox.mousePressEvent = self.mousePressEvent
        self.teCodeBox.textChanged.connect(self.fixedHeight)
        self.fixedHeight()

        glCodeBlock.addWidget(self.lbIsFocused, 0, 0)
        glCodeBlock.addWidget(self.lbBlockNumber, 0, 1)
        glCodeBlock.addWidget(self.teCodeBox, 0, 2)

        self.setCode(code)
        self.setLayout(glCodeBlock)

    def setNumber(self, num=0):
        num = str(num) if num > 0 else str()
        text = "bn [" + num + "] : "
        self.lbBlockNumber.setText(text)

    def mousePressEvent(self, event):
        self.focusedTime = time.time()
        if self.parent:
            self.parent.mousePressEvent(event)
    
    def fixedHeight(self):
        nRows = max(self.teCodeBox.toPlainText().count('\n') + 1, 5)
        qFontMetrics = QFontMetrics(self.teCodeBox.font())
        rowHeight = qFontMetrics.lineSpacing() + 5
        self.teCodeBox.setFixedHeight(rowHeight * nRows + 10)

    def focusIn(self):
        self.lbIsFocused.setStyleSheet("QLabel{ background-color : red;}")

    def focusOut(self):
        self.lbIsFocused.setStyleSheet("QLabel{ background-color : gray;}")
    
    def getCode(self):
        return self.teCodeBox.toPlainText()
    
    def setCode(self, code):
        self.teCodeBox.setText(code)
