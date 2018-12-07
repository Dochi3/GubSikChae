from CodeBlock import CodeBlock
from Control import FileControl, BlockControl
from Viewer import Viewer
from Interpret import Interpreter
import Shortcuts

from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QScrollArea
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.keyPressed = set()
        self.codeBlocks = list()
        self.index = -1
        self.excuteNumber = 0
        self.process = None
        self.interpreter = None
        BaseManager.register('Interpreter', Interpreter)
        self.interpreterManager = BaseManager()
        self.interpreterManager.start()

        self.initUI()
        self.restartProcess()

        self.timer = QTimer(self)
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.checkProcess) 
        self.timer.start()

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

        # Widget of FileControl
        self.fileControl = FileControl(self)

        # Widget of BlockControl
        self.blockContorl = BlockControl(self)

        # Widget of Viewer
        self.viewer = Viewer()

        # Layout of Editor
        glEditor = QGridLayout()
        glEditor.addWidget(saCodeBlocks, 0, 0, 10, 1)
        glEditor.addWidget(self.fileControl, 0, 1, 1, 1)
        glEditor.addWidget(self.blockContorl, 1, 1, 1, 1)
        glEditor.addWidget(self.viewer, 2, 1)

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
        
    def displayMemory(self):
        memory = self.interpreter.getMemory()
        pointer = self.interpreter.getPointer()
        self.viewer.consistMemoryDisplay(memory, pointer)

    # add new CodeBlock
    def newCodeBlock(self):
        codeBlock = CodeBlock(self)
        self.codeBlocks.insert(self.index + 1, codeBlock)
        self.index += 1
        self.setCodeBoxLayout()

    # remove CodeBlock
    def removeCodeBlock(self):
        if len(self.codeBlocks) <= 1:
            return
        focusedTime = self.codeBlocks[self.index].focusedTime
        self.codeBlocks.remove(self.codeBlocks[self.index])
        self.index = min(len(self.codeBlocks) - 1, self.index)
        self.codeBlocks[self.index].focusedTime = focusedTime
        self.setCodeBoxLayout()
    
    # excute CodeBlock
    def executeCodeBlock(self):
        code = self.codeBlocks[self.index].getCode()
        stdin = self.viewer.teStdin.text()
        try:
            stdout = self.interpreter.execute(code, stdin)
        except Exception as e:
            stdout = str(e)
        self.viewer.teStdout.setText(stdout)
        print("finish")

    # restart Process
    def restartProcess(self):
        self.excuteNumber = 0
        self.interpreter = self.interpreterManager.Interpreter()
        for codeBlock in self.codeBlocks:
            codeBlock.setNumber()
        self.stopProcess()

    def startProcess(self):
        if self.process and self.process.is_alive():
            return
        self.excuteNumber += 1
        self.codeBlocks[self.index].setNumber(self.excuteNumber)
        self.blockContorl.changeStatus(True)
        self.process = Process(target=self.executeCodeBlock)
        self.process.daemon = True
        self.process.start()

    def stopProcess(self):
        self.blockContorl.changeStatus(False)
        if self.process:
            self.process.terminate()
        self.process = None
        if self.interpreter:
            self.displayMemory()
    
    @pyqtSlot()
    def checkProcess(self):
        if self.process and self.process.is_alive():
            return
        if self.process:
            print("join")
            self.process.join()
            self.process.terminate()
            self.process = None
        self.blockContorl.changeStatus(False)
        if self.interpreter:
            self.displayMemory()

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
            self.startProcess()
        elif key == Shortcuts.Key_Ctrl_R:
            self.restartProcess()
        elif key == Shortcuts.Key_Alt_Enter:
            self.startProcess()
            self.newCodeBlock()
        elif key == Shortcuts.Key_Alt_BackSpace:
            self.removeCodeBlock()
        self.mousePressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() in self.keyPressed:
            self.keyPressed.remove(event.key())
    
    def openFile(self, mode):
        try:
            filename = self.fileControl.getFilename()
            if not filename:
                raise Exception("Invalid Filename")
            fileMode = open("./" + filename + ".gsc", mode)
            return fileMode
        except:
            self.fileControl.setMessage("Please Give Valid Filename")

    def loadFile(self):
        fileInput = self.openFile("r")
        if not fileInput:
            return
        codes = fileInput.read().split("##CodeBlock##\n")
        if len(codes) > 1:
            codes = codes[1:]
        while len(self.codeBlocks) > 1:
            self.removeCodeBlock()
        for idx, code in enumerate(codes):
            code = code.strip()
            self.codeBlocks[idx].setCode(code)
            self.newCodeBlock()
        fileInput.close()

    def saveFile(self):
        fileOutput = self.openFile("w")
        if not fileOutput:
            return
        code = str()
        for codeBlcok in self.codeBlocks:
            code += ("##CodeBlock##\n" + codeBlcok.getCode() + "\n")
        fileOutput.write(code)
        fileOutput.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
