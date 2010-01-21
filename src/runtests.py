import unittest
import parseFunctions

class IfTests(unittest.TestCase):
    def testIfExists(self):
        self.assertFalse(parseFunctions.lineContainsIf(""))
        self.assertFalse(parseFunctions.lineContainsIf("  "))
        self.assertFalse(parseFunctions.lineContainsIf("                              "))
        self.assertFalse(parseFunctions.lineContainsIf("{:ifs"))
        #Passing cases
        self.assertTrue(parseFunctions.lineContainsIf("{:if"))
        self.assertTrue(parseFunctions.lineContainsIf("{:IF"))
        self.assertTrue(parseFunctions.lineContainsIf("{:If"))
        self.assertTrue(parseFunctions.lineContainsIf("{:iF"))
        self.assertTrue(parseFunctions.lineContainsIf("    {:if"))
        self.assertTrue(parseFunctions.lineContainsIf("    {:if  #comment"))

class VariableTests(unittest.TestCase):
    def testSingle(self):
        self.failUnless(False)
    def testRestrictedKeyword(self):
        self.failUnless(False)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
