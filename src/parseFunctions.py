from Blocks import *
from Exceptions import *


def codeIterator(code):
    for lineOfCode in code.split("\n"):
        yield lineOfCode

def parse(code):
    codeIter = codeIterator(code)
    return BasicBlock(codeIter)
