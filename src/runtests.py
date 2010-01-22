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

validForBlocks = [
        """
        {:for
            :Condition ( X > 3 )
            {:Body
                :Add(Y 2)
            }
        }
        """,
        """
        {:for
            :Condition ( X > 3 )
            {:Expression
                :Add(X 1)
            }
            {:Body
                :Add(Y 2)
            }
        }
        """,
        """
        {:for
            {:Setup
                :SetVariable( X  0 )
            }
            :Condition ( X > 3 )
            {:Body
                :Add(Y 2)
            }
        }
        """,
        """
        {:for
            {:Setup
                :SetVariable( X  0 )
            }
            :Condition ( X > 3 )
            {:Expression
                :Add(X 1)
            }
            {:Body
                :Add(Y 2)
            }
        }
        """
        ]
invalidForBlocks = [
        """
        {:for
            {:Body
                :Add(Y 2)
            }
        }
        """,
        """
        {:for
            :Condition ( X > 3 )
            {:Expression
                :Add(X 1)
            }
        }
        """,
        """
        {:for
            {:Setup
                :SetVariable( X  0 )
            }
            {:Body
                :Add(Y 2)
            }
        }
        """,
        """
        {:for
            {:Setup
                :SetVariable( X  0 )
            }
            {:Expression
                :Add(X 1)
            }
            {:Body
                :Add(Y 2)
            }
        }
        """
        ]


class TestBlockExtraction(unittest.TestCase):
    def testExtractValidIf(self):
        for validBlock in validIfBlocks:
            block = parse(validBlock)
            self.assertTrue(isinstance(block, BasicBlock))
            self.assertTrue(isinstance(block.code[0], IfBlock), "Thinks this isn't an IF block: " + validBlock)
            block.generateCode()
            block.generatePreamble()
    def testExtractInvalidIf(self):
        for invalidBlock in invalidIfBlocks:
            try:
                self.assertRaises(ParseError, parse, invalidBlock)
            except self.failureException as e:
                print invalidBlock
                raise self.failureException
    def testExtractValidFor(self):
        for validBlock in validForBlocks:
            block = parse(validBlock)
            self.assertTrue(isinstance(block, BasicBlock))
            self.assertTrue(isinstance(block.code[0], ForBlock), "Thinks this isn't an FOR block: " + validBlock)
            block.generateCode()
            block.generatePreamble()
    def testExtractInvalidFor(self):
        for invalidBlock in invalidForBlocks:
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
