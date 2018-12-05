from WordToOpCode import wordToOpCode
import OpCodes
class Interpreter:

    def __init__(self):
        self.opCodes = []

    def interpret(self,Code):
        Words = Code.split()
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
                    self.opCodes[Stack[-1]] = (self.opCodes[Stack[-1]][0], idx)
                    idx = Stack[-1]
                    Stack.pop()

                self.opCodes.append((opCode,idx))
