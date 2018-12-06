from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5.QtWidgets import QLabel, QTextEdit

class Console(QWidget):
    def __init__(self):
        super().__init__()
        vblConsole = QVBoxLayout()
        self.setLayout(vblConsole)
        self.teConsole = QTextEdit()
        vblConsole.addWidget(self.teConsole)
    
    def text(self):
        return self.teConsole.toPlainText()
        
    def setText(self, txt):
        self.teConsole.setText(txt)
class Viewer(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.teStdin = Console()
        self.teStdout = Console()

        twStd = QTabWidget()
        twStd.addTab(self.teStdin, "stdin")
        twStd.addTab(self.teStdout, "stdout")

        vblViewer = QVBoxLayout()
        vblViewer.addWidget(twStd)
        self.setLayout(vblViewer)
        self.setMaximumSize(600, 300)