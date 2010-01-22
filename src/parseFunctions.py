from Blocks import *
from Exceptions import *


def codeIterator(code):
    for lineOfCode in code.split("\n"):
        line = lineOfCode.lower().split()
        # Ignore lines with no tokens
        if len(line) > 0:
            # ignore comments
            if line[0][:2] != "//":
                yield line

def parse(code):
    codeIter = codeIterator(code)
    return BasicBlock(codeIter)
