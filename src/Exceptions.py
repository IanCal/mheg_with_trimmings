class ParseError(Exception):
    """Exception raised if the input cannot be parsed

    Attributes:
        expr -- The code which cannot be parsed
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

    def __str__(self):
        return "ParseError: %s\n%s"%(self.expr,self.msg)
