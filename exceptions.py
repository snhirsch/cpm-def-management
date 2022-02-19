from lark import UnexpectedToken

class UnknownKeywordError(UnexpectedToken):
    def __init__(self, toks, curdef):
        super().__init__(toks, None)
        self.defname = curdef

class DuplicateDefError(UnexpectedToken):
    def __init__(self, toks, curdef):
        super().__init__(toks, None)
        self.defname = curdef

class DuplicateParmError(Exception):
    def __init__(self, defname, parm):
        self.defname = defname
        self.parm = parm

class MissingParmError(Exception):
    def __init__(self, defname, parms):
        self.defname = defname
        self.missing = parms
