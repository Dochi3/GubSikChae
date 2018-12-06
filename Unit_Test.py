import unittest

from Interpret import Interpreter

class TestGuess(unittest.TestCase):


    def setUp(self):
        pass

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
            #print(Samples[i])
        print(Samples)
        #a = self.interpreter.execute(Samples[1][0])
        #self.assertEqual(a,Samples[1][1])

        for i in range(len(Samples)):
            self.interpreter = Interpreter()
            a = ""
            a = self.interpreter.execute(Samples[i][0])
            print(a)
            self.assertEqual(a, Samples[i][1])

    def testDisplayGuessed(self):
        pass

if __name__ == '__main__':
    unittest.main()

