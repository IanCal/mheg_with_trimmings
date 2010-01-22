from Exceptions import *

class BasicBlock():
    def __init__(self, codeIterator):
        self.code = []
        self.preamble = []
        self.customParsing(codeIterator)
        self.genericParsing(codeIterator)

    def __str__(self):
        self.generateCode()
        stringRepresentation = str(self.code[0])
        for codeblock in self.code[1:]:
            stringRepresentation += "\n" + codeblock
        return stringRepresentation

    def printPreamble(self):
        self.generatePreamble()
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
        while True:
            try:
                line = codeIterator.next()
            except StopIteration:
                return
            # Get each token (separated from each other by spaces and ignoring whitespace)
            tokens = line
            if (len(tokens) > 0):
                # If the end of a block, stop parsing
                if (tokens[0] == "}"):
                    return
                # Otherwise if it's the start of a special block, parse that
                elif tokenDictionary.has_key(tokens[0]):
                    self.code.append(tokenDictionary[tokens[0]](codeIterator))
                # Otherwise we're just looking at a normal line of code
                else:
                    self.code.append(line)


class Conditional():
    def __init__(self, conditional):
        #TODO find the actual ordering of these
        validComparisons = {"<":1,">":2,"==":3,"!=":4,">=":5,"<=":6}
        try:
            self.first = conditional[0]
            self.second = conditional[2]
            if not(validComparisons.has_key(conditional[1])):
                raise ParseError(conditional[1], "Not one of the accepted comparisons, requires one in "+str(validComparisons))
            else:
                self.comparison = validComparisons[conditional[1]]
        except Exception as e:
            raise ParseError(conditional, "Raised an exception: " + str(e))

class IfBlock(BasicBlock):
    def customParsing(self, codeIterator):
        # Get the variable name for the if statement
        self.conditionalVariableName = "IfStatement%d" % (conditionalVariableNumber.next())
        try:
            conditionLine = codeIterator.next()
            if conditionLine[0] != ":condition":
                raise ParseError(str(conditionLine), "Should be a condition line starting with :condition")
            #TODO this must actually parse the conditional
            self.condition = Conditional(conditionLine[2:])
            # Now look for the {:iftrue line
            iftrue = codeIterator.next()
            if iftrue[0] != "{:iftrue":
                raise ParseError(str(iftrue), "Should be a line starting with {:iftrue")
            # Parse the block of code within the iftrue statement
            self.iftrue = BasicBlock(codeIterator)

            # Now look for the {:iffalse line. This is optional so a } might be encountered
            iffalse = codeIterator.next()
            # End of the block?
            if iffalse[0] == "}":
                self.iffalse = None
                return
            elif iffalse[0] != "{:iffalse":
                raise ParseError(str(iffalse), "Should be a line starting with {:iffalse")
            # Parse the block of code within the iffalse statement
            self.iffalse = BasicBlock(codeIterator)

        except Exception as e:
            raise ParseError("","Raised an exception: " + str(e))
        return

    def generatePreamble(self):
        self.preamble.append("""
        {:Link
            %d
            :EventSource %s          // Source is this test variable
            :EventType TestEvent
            :EventData True          // If condition is true
            :LinkEffect (
                %s
            )
        }
        """ % (id.next(), self.conditionalVariableName, str(self.iftrue)))
        if (self.iffalse):
            self.preamble.append("""
            {:Link
                %d
                :EventSource %s          // Source is this test variable
                :EventType TestEvent
                :EventData False          // If condition is false
                :LinkEffect (
                    %s
                )
            }
            """ % (id.next(), self.conditionalVariableName, str(self.iffalse)))

    def generateCode(self):
        #Setup the variable
        self.code.append("// Auto-generated if-statement code")
        self.code.append(":SetVariable( %s :IndirectRef %s )" % (self.conditionalVariableName, self.condition.first) )
        # Run the test
        self.code.append(":TestVariable( %s %d :IndirectRef %s )" % (self.conditionalVariableName, self.condition.comparison, self.condition.second))
        self.code.append("// End of auto-generated if-statement code")

class ForBlock(BasicBlock):
    def customParsing(self, codeIterator):
        # Get the variable name for the if statement
        self.conditionalVariableName = "ForStatement%d" % (conditionalVariableNumber.next())
        self.setup = ""
        self.expression = ""
        self.body = None
        self.condition = None
        try:
            # The order of a for loop is setup, conditional, expression (x++, etc) and then body. Only the conditional and body are required
            line = codeIterator.next()
            while line[0] != "}":
                if line[0] == "{:setup":
                    self.setup = BasicBlock(codeIterator)
                elif line[0] == ":condition":
                    self.condition = Conditional(line[2:])
                elif line[0] == "{:expression":
                    self.expression = BasicBlock(codeIterator)
                elif line[0] == "{:body":
                    self.body = BasicBlock(codeIterator)
                else:
                    raise ParseError(str(line), "Unexpected line in for loop")
                line = codeIterator.next()
            if self.body == None:
                raise ParseError("", "Missing a body in the for loop")
            if self.condition == None:
                raise ParseError("", "Missing a conditional in the for loop")
        except Exception as e:
            raise ParseError("","Raised an exception: " + str(e))
        return

    def generatePreamble(self):
        self.preamble.append("""
        {:Link
            %d
            :EventSource %s          // Source is this test variable
            :EventType TestEvent
            :EventData True          // If condition is true
            :LinkEffect (
                %s
                %s
                :SetVariable( %s :IndirectRef %s )
                :TestVariable( %s %d :IndirectRef %s )
            )
        }
        """ % (id.next(), self.conditionalVariableName, str(self.body), str(self.expression), self.condition.first, self.conditionalVariableName, self.condition.comparison, self.condition.second))


    def generateCode(self):
        #Setup the variable
        self.code.append("// Auto-generated for-loop code")
        self.code.append(str(self.setup))
        self.code.append(":SetVariable( %s :IndirectRef %s )" % (self.conditionalVariableName, self.condition.first) )
        # Run the test
        self.code.append(":TestVariable( %s %d :IndirectRef %s )" % (self.conditionalVariableName, self.condition.comparison, self.condition.second))
        self.code.append("// End of auto-generated for-loop code")



tokenDictionary = {
        "{:if" : IfBlock,
        "{:for" : ForBlock
        }
def uniqueNumbers():
    number = 0
    while 1:
        yield number
        number += 1
conditionalVariableNumber = uniqueNumbers()
id = uniqueNumbers()

