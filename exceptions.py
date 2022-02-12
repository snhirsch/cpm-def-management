from lark import UnexpectedToken

class DuplicateDefError(UnexpectedToken):
    pass

class DuplicateParmError(UnexpectedToken):
    pass

class MissingParmError(Exception):
    def __init__(self, defname, parms):
        self.defname = defname
        self.missing = parms
