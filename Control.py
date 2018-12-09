from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLineEdit,
                             QLabel, QToolButton)

class FileControl (QWidget):
    def __init__(self, parent=None):
        super().__init__()
        hblControl = QHBoxLayout()

        lbFilename = QLabel("Filename : ")
        hblControl.addWidget(lbFilename)

        self.leFilename = QLineEdit()
        hblControl.addWidget(self.leFilename)

        controlTexts = ["Save", "Load"]
        controlMethods = [parent.saveFile, parent.loadFile]

        for text, method in zip(controlTexts, controlMethods):
            tbControl = QToolButton()
            tbControl.setText(text)
            tbControl.clicked.connect(method)
            hblControl.addWidget(tbControl)
        
        self.setLayout(hblControl)
        self.setMaximumWidth(400)
    
    def getFilename(self):
        return self.leFilename.text()
    
    def setMessage(self, text):
        self.leFilename.setText(text)

class BlockControl(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.hblBox1 = QHBoxLayout()

        controlTexts = ["AddBlock", "DeleteBlock", "Run", "Pause", "Reset"]
        controlMethods = [parent.newCodeBlock, parent.deleteCodeBlock,
                          parent.startProcess, parent.stopProcess,
                          parent.restartProcess]

        for text, method in zip(controlTexts, controlMethods):
            tbControl = QToolButton()
            tbControl.setText(text)
            tbControl.clicked.connect(method)
            self.hblBox1.addWidget(tbControl)

        self.lbRunning = QLabel()
        self.lbRunning.setAlignment(Qt.AlignCenter)
        self.hblBox1.addWidget(self.lbRunning)

        self.setLayout(self.hblBox1)


    def changeStatus(self, active=False):
        text = "Running..." if active else "Pauesd"
        color = "lime" if active else "red"
        self.lbRunning.setText("Status : " + text)
        self.lbRunning.setStyleSheet("QLabel { background-color : " + color + ";}")
