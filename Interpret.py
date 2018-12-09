import time
from WordToOpCode import wordToOpCode
import OpCodes
class Interpreter:

    def __init__(self):
        self.stdout = str()
        self.typePointer = 0
        self.memoryPointer = 0
        self.memory = [[], [], []]
        self.calculatorMemory = []
    
    def getText(self):
        return self.stdout

    def setText(self, text):
        self.stdout = text
    
    def getMemory(self):
        returnMemory = []
        returnMemory.append(self.getDoubleMemory())
        returnMemory.append(self.getIntMemory())
        returnMemory.append(self.getCharMemory())
        returnMemory.append(self.getCalculatorMemory())
        return returnMemory
    
    def getPointer(self):
        return (self.typePointer, self.memoryPointer)

    def getDoubleMemory(self):
        return [str(num) for num in self.memory[0]]

    def getIntMemory(self):
        return [str(num) for num in self.memory[1]]

    def getCharMemory(self):
        return [chr(num) + "(" + str(num) + ")" for num in self.memory[2]]

    def getCalculatorMemory(self):
        return [str(num) for num in reversed(self.calculatorMemory)]

    def interpret(self, codes):
        Words = codes.split()
        codes = []
        Stack = []
        checkRemark = False
        for idx, word in enumerate(Words):
            try:
                code = wordToOpCode[word]
            except:
                if not checkRemark:
                    raise Exception("Syntax Error")
                continue
            
            if code == OpCodes.Op_Remark:
                checkRemark = not checkRemark
            
            if checkRemark:
                continue

            if code == OpCodes.Op_Condition_Begin:
                Stack.append(len(codes))
            elif code == OpCodes.Op_Condition_End:
                codes[Stack[-1]] = (codes[Stack[-1]][0], len(codes))
                idx = Stack[-1]
                Stack.pop()
            else:
                idx = 0

            codes.append((code, idx))
            
        return codes

    def execute(self, codes, stdin=""):
        stdout = str()
        codes = self.interpret(codes)
        isNumCode = lambda c: c in (OpCodes.Op_Num_0, OpCodes.Op_Num_1)
        typeDouble = 0
        typeInt = 1
        typeChar = 2
        charMax = 65536
        idx = 0
        while idx < len(codes):
            code, nextIdx = codes[idx]
            if isNumCode(code):
                idx += 1
                continue
            temp = 0
            if code == OpCodes.Op_Add:
                # raise if CM has no elements
                if not self.calculatorMemory:
                    raise Exception("Segment Fault Error")
                
                # add all elements of CM
                while self.calculatorMemory:
                    temp += self.calculatorMemory[-1]
                    self.calculatorMemory.pop()
                self.calculatorMemory.append(temp)
            elif code == OpCodes.Op_Substract:
                # raise if CM has no elements
                if not self.calculatorMemory:
                    raise Exception("Segment Fault Error")
                
                # subtract all elements of CM at CM.top
                temp = 2 * self.calculatorMemory[-1]
                while self.calculatorMemory:
                    temp -= self.calculatorMemory[-1]
                    self.calculatorMemory.pop()
                self.calculatorMemory.append(temp)
            elif code == OpCodes.Op_Multiply:
                # raise if CM has no elements
                if not self.calculatorMemory:
                    raise Exception("Segment Fault Error")
                
                # multiply all elements of CM
                temp = 1
                while self.calculatorMemory:
                    temp *= self.calculatorMemory[-1]
                    self.calculatorMemory.pop()
                self.calculatorMemory.append(temp)
            elif code == OpCodes.Op_Divide:
                # raise if CM has no elements
                if not self.calculatorMemory:
                    raise Exception("Segment Fault Error")
                
                # divide all elemnet of CM at CM.top
                temp = self.calculatorMemory[-1] ** 2
                while self.calculatorMemory:
                    temp /= self.calculatorMemory[-1]
                    self.calculatorMemory.pop()
                self.calculatorMemory.append(temp)
            elif code == OpCodes.Op_Type_Move_Left:
                self.typePointer = (self.typePointer + 2) % 3
                self.memoryPointer = 0
            elif code == OpCodes.Op_Type_Move_Right:
                self.typePointer = (self.typePointer + 1) % 3
                self.memoryPointer = 0
            elif code == OpCodes.Op_Memory_Move_Up:
                self.memoryPointer -= 1
            elif code == OpCodes.Op_Memory_Move_Down:
                self.memoryPointer += 1
            elif code == OpCodes.Op_Stack_Push:
                self.calculatorMemory.append(self.memory[self.typePointer][self.memoryPointer])
            elif code == OpCodes.Op_Stack_Pop:
                # raise if CM has no elements
                if not self.calculatorMemory:
                    raise Exception("Segment Fault Error")
                
                temp = self.calculatorMemory[-1]
                if self.typePointer == typeDouble:
                    self.memory[self.typePointer][self.memoryPointer] = temp
                elif self.typePointer == typeInt:
                    self.memory[self.typePointer][self.memoryPointer] = int(temp)
                else:
                    self.memory[self.typePointer][self.memoryPointer] = int(temp) % charMax
                self.calculatorMemory.pop()
            elif code == OpCodes.Op_List_Insert:
                if idx + 1 < len(codes) and isNumCode(codes[idx + 1][0]):
                    num = 0 if codes[idx + 1][0] == OpCodes.Op_Num_0 else 1
                    self.memory[self.typePointer].insert(self.memoryPointer, num)
                else:
                    raise Exception("Syntax Error")
            elif code == OpCodes.Op_List_Delete:
                # raise error if pointer out of index
                if self.memoryPointer < 0 or self.memoryPointer >= len(self.memory[self.typePointer]):
                    raise Exception("Index Error")
                del self.memory[self.typePointer][self.memoryPointer]
            elif code == OpCodes.Op_Condition_Begin:
                # raise error if pointer out of index
                if self.memoryPointer < 0 or self.memoryPointer >= len(self.memory[self.typePointer]):
                    raise Exception("Index Error")
                if self.memory[self.typePointer][self.memoryPointer] <= 0:
                    idx = nextIdx
            elif code == OpCodes.Op_Condition_End:
                idx = nextIdx - 1
            elif code == OpCodes.Op_Input:
                # raise error if pointer out of index
                if self.memoryPointer < 0 or self.memoryPointer >= len(self.memory[self.typePointer]):
                    raise Exception("Index Error")
                try:
                    if self.typePointer == typeChar:
                        temp = ord(stdin[0])
                        stdin = stdin[1:]
                    else:
                        stdin = stdin.lstrip()
                        temp = stdin.split()[0]
                        stdin = stdin[stdin.find(temp) + len(temp):]
                        if self.typePointer == typeDouble:
                            temp = float(temp)
                        else:
                            temp = int(temp)
                    self.memory[self.typePointer][self.memoryPointer] = temp
                except:
                    raise Exception("Input Error")
            elif code == OpCodes.Op_Ouput:
                text = str()
                temp = self.memory[self.typePointer][self.memoryPointer]
                if self.typePointer == typeChar:
                    text = chr(temp)
                else:
                    text = str(temp)
                stdout += text
            idx += 1
        return stdout
