from WordToOpCode import wordToOpCode
import OpCodes
class Interpreter:

    def __init__(self):
        self.typePointer = 0
        self.memoryPointer = 0
        self.memory = [[], [], []]
        self.calculatorMemory = []

    def interpret(self, codes):
        Words = codes.split()
        opCodes = []
        Stack = []
        check_Remark = True
        for idx, word in enumerate(Words):
            try:
                opCode = wordToOpCode[word]
            except:
                raise Exception("Syntax Error")

            if opCode == OpCodes.Op_Remark:
                check_Remark = ~check_Remark

            if check_Remark:
                if opCode == OpCodes.Op_Condition_Begin:
                    Stack.append(idx)
                if opCode == OpCodes.Op_Condition_End:
                    opCodes[Stack[-1]] = (opCodes[Stack[-1]][0], idx)
                    idx = Stack[-1]
                    Stack.pop()

                opCodes.append((opCode,idx))
        return opCodes

    def execute(self, codes):