from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout,QHBoxLayout,QApplication,QLabel,
                             QComboBox,QTextEdit,QToolButton)
class Control(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.hblBox1 = QHBoxLayout()

        controlTexts = ["AddBlock", "DeleteBlock", "Run", "Pause", "Reset"]
        controlMethods = [parent.newCodeBlock, parent.removeCodeBlock,
                          parent.startProcess, parent.stopProcess,
                          parent.restartProcess]

        for text, method in zip(controlTexts, controlMethods):
            btnControl = QToolButton()
            btnControl.setText(text)
            btnControl.clicked.connect(method)
            self.hblBox1.addWidget(btnControl)

        self.lbRunning = QLabel()
        self.lbRunning.setAlignment(Qt.AlignCenter)
        self.hblBox1.addWidget(self.lbRunning)

        self.setLayout(self.hblBox1)


    def changeStatus(self, active=False):
        text = "Running..." if active else "Pauesd"
        color = "lime" if active else "red"
        self.lbRunning.setText("Status : " + text)
        self.lbRunning.setStyleSheet("QLabel { background-color : " + color + ";}")
