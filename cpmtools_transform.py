from lark import Transformer
from cpmtools import CPMTools, SkewSkewtabError
from exceptions import UnknownKeywordError,  DuplicateParmError, MissingParmError

class CPMToolsTransformer(Transformer):
    def __init__(self, strict=False):
        # Starting line of current def in document
        self.start = None
        # True if last token seen was EOL
        self.eol = None
        # Name of current diskdef
        self.curdef = None
        # current definition object
        self.diskdef = None
        # accumulate definition comments during parse
        self.comments = []
        # current inline comment
        self.inline = None
        # per-def parameters
        self.strict = strict

    def set_start(self, linenum):
        self.start = linenum
        
    def unknown(self, toks):
        if self.strict:
            raise UnknownKeywordError(toks[0],self.curdef)
        else:
            tok = toks[0]
            print("WARNING: Unknown keyword '%s' in definition '%s' (line: %d)"
                  % (tok.value, self.curdef, self.start))
            
    def get_definition(self):
        return self.diskdef
        
    # EOL was most recent terminal
    def lex_eol(self, toks):
        self.eol = True
        return toks
    
    # Flag EOL as not most recent. Used to determine whether a comment
    # is in-line or full-line (see 'lex_comment').
    def lex_identifier(self, toks):
        self.eol = False
        return toks

    # Capture a comment
    def lex_comment(self, tok):
        if self.eol:
            # free-standing comment
            self.comments.append(tok.value)
        else:
            # something was between EOL and us so this is inline
            # comment
            self.inline = tok.value
        # Grammar ignores comments, so no return value

    # This will be reduced before any attributes
    def defname(self, toks):
        # Set current definition name
        self.curdef = toks[0].value

        # Create top-level dictionary entries
        self.diskdef = CPMTools(self.curdef)
 
        # Move def-level inline into collection
        if self.inline is not None:
            self.comments.append(self.inline)
            self.inline = None

    def _add_parameter(self, tok, value):
        name = tok.value
        self.diskdef.add_parameter(name, value)
        
    # Capture parameters and values
    def intparm(self, toks):
        (a, b, eol) = toks
        self._add_parameter(a, int(b.value))
        self.diskdef.add_parm_comment(a.value, self.inline)
        self.inline = None

    def strparm(self, toks):
        (a, b, eol) = toks
        self._add_parameter(a, b.value)
        self.diskdef.add_parm_comment(a.value, self.inline)
        self.inline = None
        
    def listparm(self, toks):
        (a, b, eol) = toks
        # Split comma-separated list of strings into list of ints
        self._add_parameter(a, [int(item) for item in b.value.split(',')])
        self.diskdef.add_parm_comment(a.value, self.inline)
        self.inline = None
        
    def unitparm(self, toks):
        (a, b, c, d, eol) = toks
        if c is None:
            units = "B"
        else:
            units = c.upper()
        self._add_parameter(a, [b.value, units])
        self.diskdef.add_parm_comment(a.value, self.inline)
        self.inline = None

    # Finalize data for current diskdef
    def end(self, tok):
        # Add in possible inline on 'end' token
        if self.inline is not None:
            self.comments.append(self.inline)
            self.inline = None
        # Store comment collection
        self.diskdef.add_def_comments(self.comments)
        # Tell object to finalize
        self.diskdef.finalize()
        # Clean up for next def
        self.comments = []
        
