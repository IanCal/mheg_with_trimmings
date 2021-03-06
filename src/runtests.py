import unittest
import os
import sys
from parseFunctions import *
from commands import getstatusoutput

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
        }
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

validVariables = [
        """
        {:NamedVar
            :Type OStringVar
            :Name NamedVariable
            :OrigValue "hello"
            {:TestedTrue
                :Add( OtherVariable 2 )
            }
            {:TestedFalse
                :Add( YetAnotherVariable 3)
            }
        }
        """,
        """
        {:NamedVar
            :Type IntegerVar
            :Name NamedVariable_2
            :OrigValue 3
            {:TestedTrue
                :Add( OtherVariable 2 )
            }
        }
        """,
        """
        {:NamedVar
            :Type IntegerVar
            :Name NamedVariable_2
            :OrigValue 3
        }
        """,
        """
        {:NamedVar
            :Type IntegerVar
            :Name NamedVariable_2
            :OrigValue 3
        }
        """
        ]
invalidVariables = [
        """
        {:NamedVar
            :Name NamedVariable
            :OrigValue "hello"
            {:TestedTrue
                :Add( OtherVariable 2 )
            }
            {:TestedFalse
                :Add( YetAnotherVariable 3)
            }
        }
        """,
        """
        {:NamedVar
            :Type IntegerVar
            :OrigValue 3
            {:TestedTrue
                :Add( OtherVariable 2 )
            }
        }
        """,
        """
        {:NamedVar
        }
        """,
        """
        {:NamedVar
            :Type IntegerVar
            :OrigValue 3
            {:TestedTrue
                :Add( OtherVariable 2 )
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
            self.assertTrue(isinstance(block.code[0], ForBlock), "Thinks this isn't a FOR block: " + validBlock)
            block.generateCode()
            block.generatePreamble()
    def testExtractInvalidFor(self):
        for invalidBlock in invalidForBlocks:
            try:
                self.assertRaises(ParseError, parse, invalidBlock)
            except self.failureException as e:
                print invalidBlock
                raise self.failureException
    def testExtractValidVariables(self):
        for validVar in validVariables:
            block = parse(validVar)
            self.assertTrue(isinstance(block, BasicBlock))
            self.assertTrue(isinstance(block.code[0], Variable), "Thinks this isn't a variable: " + validVar)
            block.generateCode()
            block.generatePreamble()
    def testExtractInvalidVar(self):
        for invalidVariable in invalidVariables:
            try:
                self.assertRaises(ParseError, parse, invalidVariable)
            except self.failureException as e:
                print invalidVariable
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

class TestFullFiles(unittest.TestCase):
    def testValidCodeCompiles(self):
        currentDirectory = sys.path[0]
        for validFile in os.listdir(currentDirectory+"/tests/"):
            if "-valid" in validFile:
                if getstatusoutput("python %s/parseFile.py %s/tests/%s > scratch-convertedfile.mhg.txt"%(currentDirectory, currentDirectory, validFile))[0] != 0:
                    self.fail("Could not parse %s"%(validFile))
                if getstatusoutput("mhegc -o scratchcompiled scratch-convertedfile.mhg.txt")[0] != 0:
                    self.fail("Could not compile %s"%(validFile))
    def testInvalidCodeCompiles(self):
        currentDirectory = sys.path[0]
        for invalidFile in os.listdir(sys.path[0]+"/tests/"):
            if "-invalid" in invalidFile:
                if getstatusoutput("python %s/parseFile.py %s/tests/%s > scratch-convertedfile.mhg.txt"%(currentDirectory, currentDirectory, validFile))[0] == 0:
                    self.fail("Parsed invalid file: %s"%(validFile))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
