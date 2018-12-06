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
        codes = []
        Stack = []
        check_Remark = True
        for idx, word in enumerate(Words):
            try:
                code = wordToOpCode[word]
            except:
                raise Exception("Syntax Error")

            if code == OpCodes.Op_Remark:
                check_Remark = not check_Remark

            if check_Remark:
                if code == OpCodes.Op_Condition_Begin:
                    Stack.append(idx)
                if code == OpCodes.Op_Condition_End:
                    codes[Stack[-1]] = (codes[Stack[-1]][0], idx)
                    idx = Stack[-1]
                    Stack.pop()

                codes.append((code, idx))
            
        return codes

    def execute(self, codes, stdin):
        codes = self.interpret(codes)
        data = stdin.split()
        isNumCode = lambda c: c == OpCodes.Op_Num_0 or c == OpCodes.Op_Num_1

        for idx, code in enumerate(codes):
            if isNumCode(code):
                continue

            if code == OpCodes.Op_List_Insert:
                if idx + 1 < len(codes) and isNumCode(codes[idx + 1][1]):
                    pass
                else:
                    raise Exception("Syntax Error")
