import unittest

class VariableTests(unittest.TestCase):

    def testSingle(self):
        self.failUnless(False)
    def testRestrictedKeyword(self):
        self.failUnless(False)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
