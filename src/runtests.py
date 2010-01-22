import unittest
from parseFunctions import *

validIfBlocks = [
        """
        {:if
            :condition ( X < 3 )
            {:iftrue
                Y = 3;
                X = 2;
            }
            {:iffalse
                Y = 10;
                X = 3;
            }
        ]
        """,
        """
        {:If
            :Condition ( Y  >= 2 )
            {:ifTrue
                X = 3;
            }
        }
        """
        ]
invalidIfBlocks = [
        """
        {:If
        }
        """,
        """
        {:If
            :Condition
            {:ifTrue
                X = 3;
            }
        }
        """,
        """
        {:If
            :Conditional ( x < 3 )
            {:ifTrue
                X = 3;
            }
        }
        """,
        """
        {:If
            :Condition (x>4)
            {:ifTrue
                X = 3;
            }
        }
        """,
        """
        {:If
            :Condition ( X < 4)
        }
        """,
        ]

validConditionals = [
        ["X",">","Y"],
        ["X","<","Y"],
        ["X","==","Y"],
        ["X","!=","Y"],
        ["X",">=","Y"],
        ["X","<=","Y"]
        ]
invalidConditionals = [
        [">","Y"],
        ["X","<"],
        ["X","Y"],
        ["X","!!=","Y"],
        ["X","<>=","Y"],
        ["X","<==","Y"]
        ]


class TestBlockExtraction(unittest.TestCase):
    def testExtractValidIf(self):
        for validBlock in validIfBlocks:
            block = parse(validBlock)
            self.assertTrue(isinstance(block, BasicBlock))
            self.assertTrue(isinstance(block.code[0], IfBlock), "Thinks this isn't an IF block: " + validBlock)
    def testExtractInvalidIf(self):
        for invalidBlock in invalidIfBlocks:
            try:
                self.assertRaises(ParseError, parse, invalidBlock)
            except self.failureException as e:
                print invalidBlock
                raise self.failureException


class TestConditionalParsing(unittest.TestCase):
    def testParseValidConditional(self):
        for validConditional in validConditionals:
            conditional = Conditional(validConditional)
    def testParseInvalidConditional(self):
        for invalidConditional in invalidConditionals:
            try:
                self.assertRaises(ParseError, Conditional, invalidConditional)
            except self.failureException as e:
                print invalidConditional, e
                raise self.failureException



def main():
    unittest.main()

if __name__ == '__main__':
    main()
