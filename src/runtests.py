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
        {if
        :condition
        }""",
        """
        {:If
            :Condition
            {:ifTrue
                X = 3;
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
    def testExtractInvalidIf(self):
        for invalidBlock in invalidIfBlocks:
            block = parse(invalidBlock)
            self.assertTrue(isinstance(block, BasicBlock))
            self.assertFalse(isinstance(block.code[0], IfBlock), "Thinks this is a valid IF block: " + invalidBlock)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
