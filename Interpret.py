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
        checkRemark = False
        for idx, word in enumerate(Words):
            try:
                code = wordToOpCode[word]
            except:
                raise Exception("Syntax Error")

            if code == OpCodes.Op_Remark:
                checkRemark = not checkRemark

            if not checkRemark:
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

    def execute(self, codes, stdin, stdout):
        codes = self.interpret(codes)
        isNumCode = lambda c: c in (OpCodes.Op_Num_0, OpCodes.Op_Num_1)

        for idx, code in enumerate(codes):
            if isNumCode(code):
                continue
            temp = 0
            if code == OpCodes.Op_Add:
                if not self.calculatorMemory:
                    raise Exception("Segment Fault")
                while self.calculatorMemory:
                    temp += self.calculatorMemory[-1]
                    self.calculatorMemory.pop()
                self.calculatorMemory.append(temp)
            elif code == OpCodes.Op_Substract:
                pass
            elif code == OpCodes.Op_Multiply:
                pass
            elif code == OpCodes.Op_Divide:
                pass
            elif code == OpCodes.Op_Type_Move_Left:
                pass
            elif code == OpCodes.Op_Type_Move_Right:
                pass
            elif code == OpCodes.Op_Memory_Move_Up:
                pass
            elif code == OpCodes.Op_Memory_Move_Down:
                pass
            elif code == OpCodes.Op_Stack_Push:
                pass
            elif code == OpCodes.Op_Stack_Pop:
                pass
            elif code == OpCodes.Op_List_Insert:
                if idx + 1 < len(codes) and isNumCode(codes[idx + 1][0]):
                    num = 0 if codes[idx + 1][0] == OpCodes.Op_Num_0 else 1
                    self.memory[self.typePointer].insert(self.memoryPointer, num)
                else:
                    raise Exception("Syntax Error")
            elif code == OpCodes.Op_List_Delete:
                pass
            elif code == OpCodes.Op_Condition_Begin:
                pass
            elif code == OpCodes.Op_Condition_End:
                pass
            elif code == OpCodes.Op_Input:
                pass
            elif code == OpCodes.Op_Ouput:
                pass
