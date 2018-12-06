from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout,QHBoxLayout,QApplication,QLabel,
                             QComboBox,QTextEdit,QToolButton)
class Control(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.hblBox1 = QHBoxLayout()

        self.tbExcuteButton = QToolButton()
        self.tbExcuteButton.setText("Run")
        self.tbExcuteButton.clicked.connect(parent.startProcess)
        self.hblBox1.addWidget(self.tbExcuteButton)

        self.tbPauseButton = QToolButton()
        self.tbPauseButton.setText("Pause")
        self.tbPauseButton.clicked.connect(parent.stopProcess)
        self.hblBox1.addWidget(self.tbPauseButton)

        self.tbResetMemoryButton = QToolButton()
        self.tbResetMemoryButton.setText("ResetMemory")
        self.tbResetMemoryButton.clicked.connect(parent.restartProcess)
        self.hblBox1.addWidget(self.tbResetMemoryButton)

        self.lbRunning = QLabel()
        self.hblBox1.addWidget(self.lbRunning)

        self.setLayout(self.hblBox1)


    def changeStatus(self, status):
        self.lbRunning.setText("Status : " + status)

