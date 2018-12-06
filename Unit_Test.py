import unittest

from Interpret import Interpreter

class TestGuess(unittest.TestCase):


    def setUp(self):
        self.interpreter = Interpreter()

    def tearDown(self):
        pass

    def testDisplayCurrent(self):
        f = open("Test_Code.txt", "r")
        Data = f.read()
        Data = Data.replace('\n', ' ')
        Samples = Data.split("#")
        for i in range(len(Samples)):
            Samples[i] = Samples[i].split('_')
            Samples[i][1] = Samples[i][1].rstrip()
            print(Samples[i])

        for i in range(len(Samples)):
            self.assertEqual(self.interpreter.execute(Samples[i][0]), Samples[i][1])  # 답은 3

    def testDisplayGuessed(self):
        f = open("Test_Code.txt", "r")
        Data = f.read()
        Data = Data.replace('\n', '')
        Samples = Data.split("#")
        for i in range(len(Samples)):
            Samples[i] = Samples[i].split('_')
            print(Samples[i])
        self.assertEqual(self.interpreter.execute(Samples[0][0]), Samples[0][1])  # 답은 3
        self.assertEqual(self.interpreter.execute(Samples[1][0]), Samples[1][1])  # 답은 3
        pass

if __name__ == '__main__':
    unittest.main()

