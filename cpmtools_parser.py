#!/usr/bin/python3

import sys
from lark.lark import Lark
from lark import UnexpectedToken, UnexpectedCharacters, UnexpectedEOF

from cpmtools_grammer import CPMTOOLS, build_callbacks
from cpmtools_transform import CPMToolsTransformer
from cpmtools import SkewSkewtabError
from exceptions import DuplicateParmError, DuplicateDefError, MissingParmError

try:
    infile = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <diskdef_file>")

print(infile[::-1])

# A Transformer is a 'data handler' that absorbs input from parser and
# builds a Cpmtools object to represent each definition in the file.
xfm = CPMToolsTransformer()

# Instantiate the parser and connect data handlers
parser = Lark(CPMTOOLS,
              lexer           = 'contextual',
              lexer_callbacks = build_callbacks(xfm),
              parser          = 'lalr',
              transformer     = xfm)

with open(infile, "r") as f:
    # Slurp in the entire file
    data = f.read()
    try:
        # Process the input 
        parser.parse(data)

        # If we made it here, the parse succeeded. Get dictionary of
        # CPMTools and print in alphabetical order
        defdict = xfm.get_definitions()
        for key in sorted(defdict.keys()):
            val = defdict[key]
            # A CPMTools object turns itself into a text representation
            # of the definition when used as a string.
            print(val)

    except MissingParmError as d:
        print("Required parameters missing from definition %s:" % d.defname)
        for parm in d.missing:
            print("%s " % parm, end="")
        print("\n")

    except SkewSkewtabError as d:
        print("Skew and skewtab cannot both be specified (line: %d, column: %d)" % (d.line, d.column))
        ctxt = d.get_context(data)
        print(ctxt)
        
    except DuplicateParmError as d:
        print("Duplicate parameter at line: %d, column: %d" % (d.line, d.column))
        ctxt = d.get_context(data)
        print(ctxt)
        
    except DuplicateDefError as d:
        print("Duplicate definition at line: %d, column: %d" % (d.line, d.column))
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
