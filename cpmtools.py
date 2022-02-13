from lark import UnexpectedToken
from exceptions import DuplicateParmError, MissingParmError

class SkewSkewtabError(UnexpectedToken):
    def __init__(self, toks, curdef):
        super().__init__(toks, None)
        self.curdef = curdef

# DiskDef object represents a single cpmtools diskdef stanza, comments
# included.
class CPMTools:
    required = ('seclen',
                'tracks',
                'sectrk',
                'blocksize',
                'maxdir',
                'boottrk',
                'os')
                
    def __init__(self, defname):
        self.defname = defname
        self.parameters = dict()
        self.def_comments = None
        self.parm_comments = None

    # Attach a list of comments to the definition as a whole.
    def add_def_comments(self, list):
        if list is not None and len(list):
            self.def_comments = list

    # Add a parameter keyword and value to the definition
    def add_parameter(self, tok, val):
        name = tok.value
        if name in self.parameters:
            # Flag duplicated keyword
            raise DuplicateParmError(tok,self.defname)
        if (name == 'skew' and 'skewtab' in self.parameters) or \
           name == 'skewtab' and 'skew' in self.parameters:
            raise SkewSkewtabError(tok,self.defname)
        self.parameters[name] = val
        
    # Return a dictionary of parameters
    def get_parameters(self):
        return self.parameters

    # Add an inline comment to a parameter
    def add_parm_comment(self, tok, val):
        if val is not None:
            if self.parm_comments is None:
                self.parm_comments = dict()
            self.parm_comments[tok.value] = val

    def finalize(self):
        missing = []
        for parm in CPMTools.required:
            if not parm in self.parameters:
                missing.append(parm)
        if len(missing):
            raise MissingParmError(self.defname,missing)

    # Render object data into a formatted diskdef stanza
    def __str__(self):
        s = ""
        if self.def_comments is not None:
            for c in self.def_comments:
                s += "%s\n" % c
        s += "diskdef %s\n" % self.defname
        for key, value in self.parameters.items():
            if key == 'skewtab':
                value = ','.join(str(i) for i in value)
            elif key == 'offset':
                if value[1] != 'B':
                    value = ''.join(value)
                else:
                    value = value[0]
            s += "  %s %s" % (key, value)
            if self.parm_comments is not None and key in self.parm_comments:
                s += "\t%s\n" % self.parm_comments[key]
            else:
                s += "\n"
        s += "end\n"
        return s
        
            
