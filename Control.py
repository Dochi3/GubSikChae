from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout,QHBoxLayout,QApplication,QLabel,
                             QComboBox,QTextEdit,QToolButton)
class Control(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.hblBox1 = QHBoxLayout()

        self.tbExcuteButton = QToolButton('Run')
        self.tbExcuteButton.clicked.connect(parent.startProcess)
        self.hblBox1.addWidget(self.tbExcuteButton)

        self.tbPauseButton = QToolButton('Pause')
        self.tbPauseButton.clicked.connect(parent.stopProcess)
        self.hblBox1.addWidget(self.tbPauseButton)

        self.tbResetMemoryButton = QToolButton("ResetMenory")
        self.tbResetMemoryButton.clicked.connect(parent.restartProcess)
        self.hblBox1.addWidget(self.tbResetMemoryButton)

        self.lbRunningLabel = QLabel("Status:Paused") #????????
        self.hblBox1.addWidget(self.lRunningLabel)


    def changeStatus(self,status):
        self.lbRunningLabel.setText("Status:"+status)

