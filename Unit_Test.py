import unittest
import sys
from Interpret import Interpreter

class TestGuess(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTestCode(self):
        f = open("Test_Code.txt", "r")
        Data = f.read()
        Data = Data.replace('\n', ' ')
        Samples = Data.split("#")
        for i in range(len(Samples)):
            Samples[i] = Samples[i].split('_')
            Samples[i][1] = Samples[i][1].rstrip()

        for i in range(len(Samples)):
            self.interpreter = Interpreter()
            a = self.interpreter.execute(Samples[i][0])
            self.assertEqual(a, Samples[i][1])
        f.close()

    def testDecode_Sample(self):
        f = open("Decode_Sample.txt", "r")
        Data = f.read()
        Data = Data.replace('\n', '')
        Samples = Data.split("#")
        for i in range(len(Samples)):
            Samples[i] = Samples[i].split('-')

        for i in range(len(Samples)):
            self.interpreter = Interpreter()
            a = self.interpreter.interpret(Samples[i][0])
            print(a)
            self.assertEqual(str(a).replace(' ', ''), Samples[i][1])  # 답은 3
        pass

if __name__ == '__main__':
    unittest.main()

