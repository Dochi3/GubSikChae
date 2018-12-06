from CodeBlock import CodeBlock
from Viewer import Viewer
from Interpret import Interpreter
import Shortcuts

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QLabel

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.keyPressed = set()
        self.codeBlocks = list()
        self.index = -1
        self.excuteNumber = 0
        self.interpreter = None
        self.restartProcess()

        self.initUI()

    def initUI(self):
        # Widget of CodeBlocks
        wgCodeBlocks = QWidget()

        saCodeBlocks = QScrollArea()
        saCodeBlocks.setWidget(wgCodeBlocks)
        saCodeBlocks.setWidgetResizable(True)
        saCodeBlocks.setAlignment(Qt.AlignTop)

        self.vblCodeBlocks = QVBoxLayout()
        self.vblCodeBlocks.setAlignment(Qt.AlignTop)
        wgCodeBlocks.setLayout(self.vblCodeBlocks)
        self.newCodeBlock()

        # Widget of Control

        # Widget of Viewer
        self.viewer = Viewer()

        # Layout of Editor
        glEditor = QGridLayout()
        glEditor.addWidget(saCodeBlocks, 0, 0, 1, 3)
        glEditor.addWidget(self.viewer, 0, 3, 1, 1)

        # Widget of Editor
        wgEditor = QWidget()
        wgEditor.setLayout(glEditor)
        self.setCentralWidget(wgEditor)
        self.mousePressEvent(None)
        self.showMaximized()

    def setCodeBoxLayout(self):
        # remove all items of vblCodeBlocks
        for i in reversed(range(self.vblCodeBlocks.count())): 
            self.vblCodeBlocks.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.vblCodeBlocks.count())): 
            self.vblCodeBlocks.itemAt(i).widget().deleteLater()

        for codeBlock in self.codeBlocks:
            self.vblCodeBlocks.addWidget(codeBlock)

    # add new CodeBlock
    def newCodeBlock(self):
        codeBlock = CodeBlock(self)
        self.codeBlocks.insert(self.index + 1, codeBlock)
        self.index += 1
        self.setCodeBoxLayout()
    
    # excute CodeBlock
    def executeCodeBlock(self):
        self.excuteNumber += 1
        self.codeBlocks[self.index].setNumber(self.excuteNumber)
        
        code = self.codeBlocks[self.index].getCode()
        stdin = self.viewer.teStdin.text()
        stdout = self.interpreter.execute(code, stdin)
        self.viewer.teStdout.setText(stdout)

    # restart Process
    def restartProcess(self):
        self.excuteNumber = 0
        self.interpreter = Interpreter()
        for codeBlock in self.codeBlocks:
            codeBlock.setNumber()

    # remove CodeBlock
    def removeCodeBlock(self):
        if len(self.codeBlocks) <= 1:
            return
        focusedTime = self.codeBlocks[self.index].focusedTime
        self.codeBlocks.remove(self.codeBlocks[self.index])
        self.index = min(len(self.codeBlocks) - 1, self.index)
        self.codeBlocks[self.index].focusedTime = focusedTime
        self.setCodeBoxLayout()

    # focus which textEdit to fix
    def setCodeBoxFocus(self, index):
        self.index = index
        self.codeBlocks[self.index].teCodeBox.setFocus()

    def mousePressEvent(self, event):
        maxTime = 0
        selectedCodeBlock = None
        for index, codeBlock in enumerate(self.codeBlocks):
            codeBlock.focusOut()
            maxTime = max(maxTime, codeBlock.focusedTime)
            if maxTime == codeBlock.focusedTime:
                selectedCodeBlock = codeBlock
                self.setCodeBoxFocus(index)
        selectedCodeBlock.focusIn()

    # process shortcut
    def keyPressEvent(self, event):
        self.keyPressed.add(event.key())
        key = Shortcuts.shortcuts.get(frozenset(self.keyPressed), "No Matching")
        if key == Shortcuts.Key_Ctrl_Enter:
            self.executeCodeBlock()
        elif key == Shortcuts.Key_Ctrl_R:
            self.restartProcess()
        elif key == Shortcuts.Key_Alt_Enter:
            self.executeCodeBlock()
            self.newCodeBlock()
        elif key == Shortcuts.Key_Alt_BackSpace:
            self.removeCodeBlock()
        self.mousePressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() in self.keyPressed:
            self.keyPressed.remove(event.key())
    
    def executeBtn(self):
        pass
    
    def pauseBtn(self):
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
