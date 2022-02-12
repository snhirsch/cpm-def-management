#!/usr/bin/python3

from lark.lark import Lark
from lark import Transformer, UnexpectedToken, UnexpectedCharacters, UnexpectedEOF
from twotwodisk import TwoTwoDisk, DuplicateParmError, MissingParmError
from twotwodisk_grammer import TWOTWODISK, build_callbacks
from twotwodisk_transform import TwoTwoDiskTransformer, DuplicateDefError, SectorsBeforeNumSidesError, SideListBeforeSectorsError
    
xfm = TwoTwoDiskTransformer()
    
# Instantiate the parser and connect data handlers
parser = Lark(TWOTWODISK,
              lexer = 'contextual',
              lexer_callbacks = build_callbacks(xfm),
              parser = 'lalr',
              transformer = xfm)

with open("22disk", "r") as f:
    # Slurp in the entire file
    data = f.read()
    try:
        # Process the input 
        parser.parse(data)
        
        # If we made it here, the parse succeeded. Get dictionary of
        # 22Disk definitions and print in alphabetical order
        defdict = xfm.get_definitions()
        for key in sorted(defdict.keys()):
            val = defdict[key]
            # A TwoTwoDisk object turns itself into a text representation
            # of the definition when used as a string.
            print(val)
            
    except DuplicateParmError as d:
        print("Duplicate parameter at line: %d, column: %d" % (d.line, d.column))
        ctxt = d.get_context(data)
        print(ctxt)

    except MissingParmError as d:
        print("Required parameters missing from definition %s:" % d.defname)
        for parm in d.missing:
            print("%s " % parm, end="")
        print("\n")

    except DuplicateDefError as d:
        print("Duplicate definition at line: %d, column: %d" % (d.line, d.column))
        ctxt = d.get_context(data)
        print(ctxt)
        
    except SectorsBeforeNumSidesError as d:
        print("SECTORS parameter seen before SIDES at line: %d, column: %d\n" % (d.line, d.column))
        ctxt = d.get_context(data)
        print(ctxt)
        
    except SideListBeforeSectorsError as d:
        print("SIDE1/SIDE2 parameter seen before SECTORS at line: %d, column: %d\n" % (d.line, d.column))
        ctxt = d.get_context(data)
        print(ctxt)
        
    except UnexpectedToken as u:
        print("Unxpected token at line: %d, column: %d" % (u.line, u.column))
        ctxt = u.get_context(data)
        print(ctxt)
        if len(u.expected) > 1:
            print("Expected one of:")
        else:
            print("Expected: ", end="")
        for tok in u.expected:
            name = str(parser.get_terminal(tok).pattern)
            print(name.replace('\\',''))
            
    except UnexpectedCharacters as u:
        print(u)
        
    except UnexpectedEOF as u:
        print("Unexpected EOF at line: %d, column: %d\n" % (u.line, u.column))
        ctxt = u.get_context(data)
        print(ctxt)
