from lark import Transformer, UnexpectedToken
from twotwodisk import TwoTwoDisk
from exceptions import DuplicateDefError

class SectorsBeforeNumSidesError(UnexpectedToken):
    pass

class SideListBeforeSectorsError(UnexpectedToken):
    pass

class TwoTwoDiskTransformer(Transformer):

    def __init__(self):
        self.curdef = None
        self.defn = None
        self.comments = []
        self.definitions = dict()

    def get_definitions(self):
        return self.definitions
        
    def lex_sofs(self, tok):
        # Fix pervasive spelling error in legacy defs
        if tok.value.upper() == 'SOFS':
            tok.value = 'OFS'
        return tok

    def lex_comment(self, tok):
        self.comments.append(tok.value)

    def diskdef(self, tok):
        if len(self.comments):
            self.defn.add_def_comments(self.comments)
            self.comments = []

    def real(self, tok):
        self.defn.finalize()
        
    def defname(self, toks):
        self.curdef = toks[0].value

        if self.curdef in self.definitions:
            raise DuplicateDefError(toks[0],None)
        
        self.defn = self.definitions[self.curdef] = TwoTwoDisk(self.curdef)
        
    def intparm(self, toks):
        self.defn.add_parameter(toks[0], toks[1])

    def density(self, toks):
        self.defn.add_parameter(toks[0], [toks[1].value.lower(), toks[2].value.lower()])

    # Flags are significant by presence or absence - value is
    # irrelevant
    def flag(self, toks):
        self.defn.add_parameter(toks[0], True)

    def sectors(self, toks):
        if not 'sides' in self.defn.get_parameters():
            raise SectorsBeforeNumSidesError(toks[0],None)
        self.defn.add_parameter(toks[0], [toks[1], toks[2]])

    def side(self, toks):
        if not 'sectors' in self.defn.get_parameters():
            raise SideListBeforeSectorsError(toks[0],None)
        (parm, hd, lst) = toks[0:3]
        if len(toks) > 3:
            lst.extend(toks[3])
        self.defn.add_parameter(parm, [int(hd), lst])

    def order(self, toks):
        (parm, layout) = toks[0:2]
        extra = None
        if len(toks) > 2:
            extra = toks[2].lower()
        self.defn.add_parameter(parm, [layout.lower(), extra])

    def label(self, toks):
        (parm, val) = toks
        self.defn.add_parameter(parm, val.lower())

    def description(self, toks):
        self.defn.add_description(toks[0].value)

    # Convert tokens to values
    def intval(self, toks):
        return int(toks[0].value)

    def hexval(self, toks):
        s = toks[0].value[:-1]
        return int(s, 16)

    def binval(self, toks):
        s = toks[0].value[:-1]
        return int(s, 2)

    def numlist(self, toks):
        return [ int(t.value) for t in toks ]
