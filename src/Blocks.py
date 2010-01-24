from Exceptions import *

class BasicBlock():
    def __init__(self, codeIterator, ignoreFinalBracket = False):
        self.ignoreFinalBracket = ignoreFinalBracket
        self.openbrackets = 0
        self.code = []
        self.preamble = []
        self.customParsing(codeIterator)
        self.genericParsing(codeIterator)
        self.generateCode()
        self.generatePreamble()

    def __str__(self):
        #self.generateCode()
        if (len(self.code) > 0):
            stringRepresentation = str(self.code[0])
            for codeblock in self.code[1:]:
                stringRepresentation += "\n" + str(codeblock)
        else:
            stringRepresentation = ""
        return stringRepresentation
    def printPreamble(self):
        ownPreamble = "\n".join(self.preamble)
        for internalblock in self.code:
            if not(isinstance(internalblock, str)):
                ownPreamble += internalblock.printPreamble()
        return ownPreamble

    def generateCode(self):
        pass

    def generatePreamble(self):
        pass

    def customParsing(self, codeIterator):
        pass

    def genericParsing(self, codeIterator):
        num = id.next()
        while True:
            try:
                tokens, exactLine = codeIterator.next()
            except StopIteration:
                return False
            if (len(tokens) > 0):
                #print "GENERIC PARSING:",tokens
                # Otherwise if it's the start of a special block, parse that
                if tokenDictionary.has_key(tokens[0]):
                    self.code.append(tokenDictionary[tokens[0]](codeIterator))
                # If the end of a block, stop parsing
                elif (tokens[0][0] == "{"):
                    self.code.append(exactLine)
                    self.openbrackets += 1
                # If the end of a block, stop parsing
                elif (tokens[0] == "}"):
                    self.openbrackets -= 1
                    if self.openbrackets <= 0:
                        if not(self.ignoreFinalBracket):
                            self.code.append(exactLine)
                        return False
                        self.code.append(exactLine)
                    else:
                        self.code.append(exactLine)
                # Otherwise we're just looking at a normal line of code
                else:
                    self.code.append(exactLine)

class Scene(BasicBlock):
    def customParsing(self, codeIterator):
        self.preamble.append("{:Scene")
        line, exact = codeIterator.next()
        while line[0] != ":items":
            self.preamble.append(exact)
            line, exact = codeIterator.next()
        while line[0] != "(":
            self.preamble.append(exact)
            line, exact = codeIterator.next()
        self.preamble.append("(")





class Conditional():
    def __init__(self, conditional):
        validComparisons = {"==":1,"!=":2,"<":3,"<=":4,">":5,">=":6}
        try:
            assert(len(conditional) > 2)
            self.first = conditional[0]
            self.second = " ".join(conditional[2:-1])
            if not(validComparisons.has_key(conditional[1])):
                raise ParseError(conditional[1], "Not one of the accepted comparisons, requires one in "+str(validComparisons))
            else:
                self.comparison = validComparisons[conditional[1]]
        except Exception as e:
            raise ParseError(conditional, "Raised an exception: " + str(e))

class IfBlock(BasicBlock):
    def genericParsing(self, codeIterator):
        self.ignoreFinalBracket = True
        # Get the variable number for the if statement
        self.variableNumber = id.next()
        self.iffalse = None
        try:
            conditionLine = codeIterator.next()[0]
            if conditionLine[0] != ":condition":
                raise ParseError(str(conditionLine), "Should be a condition line starting with :condition")
            #TODO this must actually parse the conditional
            self.condition = Conditional(conditionLine[2:])
            # Now look for the {:iftrue line
            iftrue = codeIterator.next()[0]
            if iftrue[0] != "{:iftrue":
                raise ParseError(str(iftrue), "Should be a line starting with {:iftrue")
            # Parse the block of code within the iftrue statement
            self.iftrue = BasicBlock(codeIterator, True)
            self.preamble.append(self.iftrue.printPreamble())
            # Now look for the {:iffalse line. This is optional so a } might be encountered
            iffalse = codeIterator.next()[0]
            # End of the block?
            if iffalse[0] == "}":
                self.iffalse = None
                return
            elif iffalse[0] != "{:iffalse":
                raise ParseError(str(iffalse), "Should be a line starting with {:iffalse")
            # Parse the block of code within the iffalse statement
            self.iffalse = BasicBlock(codeIterator, True)
            self.preamble.append(self.iffalse.printPreamble())
            line, exact = codeIterator.next()
            if line[0] != "}":
                raise ParseError(exact, "Unexpected line")
        except Exception as e:
            raise ParseError("","Raised an exception: " + str(e))
        return

    def generatePreamble(self):
        self.preamble.append("""
        {:%s %d :OrigValue 0}
        {:Link
            %d
            :EventSource %d          // Source is this test variable
            :EventType TestEvent
            :EventData True          // If condition is true
            :LinkEffect (
                %s
            )
        }
        """ % ("IntegerVar", self.variableNumber, id.next(), self.variableNumber, str(self.iftrue)))
        if (self.iffalse):
            self.preamble.append("""
            {:Link
                %d
                :EventSource %d          // Source is this test variable
                :EventType TestEvent
                :EventData False          // If condition is false
                :LinkEffect (
                    %s
                )
            }
            """ % (id.next(), self.variableNumber, str(self.iffalse)))

    def generateCode(self):
        #Setup the variable
        self.code.append("// Auto-generated if-statement code")
        self.code.append(":SetVariable( %d :GInteger :IndirectRef %s )" % (self.variableNumber, self.condition.first) )
        # Run the test
        #self.code.append(":TestVariable( %d %d :IndirectRef %s )" % (self.variableNumber, self.condition.comparison, self.condition.second))
        self.code.append(":TestVariable( %d %d :GInteger %s )" % (self.variableNumber, self.condition.comparison, self.condition.second))
        self.code.append("// End of auto-generated if-statement code")

class ForBlock(BasicBlock):
    def genericParsing(self, codeIterator):
        # Get the variable name for the if statement
        self.ignoreFinalBracket = True
        self.variableNumber = id.next()
        self.setup = ""
        self.expression = ""
        self.body = None
        self.condition = None
        try:
            # The order of a for loop is setup, conditional, expression (x++, etc) and then body. Only the conditional and body are required
            line, exact = codeIterator.next()
            while line[0] != "}":
                if line[0] == "{:setup":
                    self.setup = BasicBlock(codeIterator, True)
                    self.preamble.append(self.setup.printPreamble())
                elif line[0] == ":condition":
                    self.condition = Conditional(line[2:])
                elif line[0] == "{:expression":
                    self.expression = BasicBlock(codeIterator, True)
                    self.preamble.append(self.expression.printPreamble())
                elif line[0] == "{:body":
                    self.body = BasicBlock(codeIterator, True)
                    self.preamble.append(self.body.printPreamble())
                else:
                    raise ParseError(str(line), "Unexpected line in for loop")
                line, exact = codeIterator.next()
            if self.body == None:
                raise ParseError("", "Missing a body in the for loop")
            if self.condition == None:
                raise ParseError("", "Missing a conditional in the for loop")
        except Exception as e:
            raise ParseError("","Raised an exception: " + str(e))
        return

    def generatePreamble(self):
        self.preamble.append("""
        {:%s %d :OrigValue 0}
        {:Link
            %d
            :EventSource %d          // Source is this test variable
            :EventType TestEvent
            :EventData True          // If condition is true
            :LinkEffect (
                %s
                %s
                :SetVariable( %d :GInteger :IndirectRef %s )
                :TestVariable( %d %d :GInteger %s )
            )
        }
        """ % ("IntegerVar", self.variableNumber, id.next(), self.variableNumber, str(self.body), str(self.expression), self.variableNumber, self.condition.first, self.variableNumber, self.condition.comparison, self.condition.second))


    def generateCode(self):
        #Setup the variable
        self.code.append("// Auto-generated for-loop code")
        self.code.append(str(self.setup))
        self.code.append(":SetVariable( %d :GInteger :IndirectRef %s )" % (self.variableNumber, self.condition.first) )
        # Run the test
        self.code.append(":TestVariable( %d %d :GInteger  %s )" % (self.variableNumber, self.condition.comparison, self.condition.second))
        self.code.append("// End of auto-generated for-loop code")


class Variable(BasicBlock):
    def genericParsing(self, codeIterator):
        self.variableNumber = id.next()
        self.name = None
        self.originalValue = None
        self.type = None
        self.testTrue = None
        self.testFalse = None
        try:
            line, exact = codeIterator.next()
            while line[0] != "}":
                if line[0] == ":name":
                    self.name = line[1]
                elif line[0] == ":type":
                    self.type = line[1]
                elif line[0] == ":origvalue":
                    # Don't lose the whitespace in this line, and don't include any comments
                    self.originalValue = exact.strip().split("//")[0]
                elif line[0] == "{:testedtrue":
                    self.testTrue = BasicBlock(codeIterator)
                elif line[0] == "{:testedfalse":
                    self.testFalse = BasicBlock(codeIterator)
                else:
                    raise ParseError(str(line), "Unexpected line in variable declaration")
                line, exact = codeIterator.next()
            if self.name == None:
                raise ParseError("", "Missing a name in the named variable declaration")
            if self.type == None:
                raise ParseError("", "Missing a type in the named variable declaration")
            if self.originalValue == None:
                raise ParseError("", "Missing an origvalue in the named variable declaration")
        except Exception as e:
            raise ParseError("","Raised an exception: " + str(e))
        return

    def generatePreamble(self):
        if not(self.testTrue == None):
            self.preamble.append("""
            {:Link
                %d
                :EventSource %d          // Source is this test variable
                :EventType TestEvent
                :EventData True          // If condition is true
                :LinkEffect (
                    %s
                )
            }
            """ % (id.next(), self.variableNumber, str(self.testTrue)))
        if not(self.testFalse == None):
            self.preamble.append("""
            {:Link
                %d
                :EventSource %d          // Source is this test variable
                :EventType TestEvent
                :EventData False          // If condition is true
                :LinkEffect (
                    %s
                )
            }
            """ % (id.next(), self.variableNumber, str(self.testFalse)))

    def generateCode(self):
        self.code.append("{:%s %d :OrigValue %s}" % ( self.type, self.variableNumber, self.originalValue ))



tokenDictionary = {
        "{:if" : IfBlock,
        "{:for" : ForBlock,
        "{:namedvar" : Variable,
        "{:scene" : Scene
        }
def uniqueNumbers(number):
    while 1:
        yield number
        number += 1
id = uniqueNumbers(100)

