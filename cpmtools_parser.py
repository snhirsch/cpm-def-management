#!/usr/bin/python3

import sys
from lark.lark import Lark
from lark import UnexpectedToken, UnexpectedCharacters, UnexpectedEOF

from cpmtools_grammar import CPMTOOLS, build_callbacks
from cpmtools_transform import CPMToolsTransformer
from cpmtools import SkewSkewtabError
from exceptions import DuplicateParmError, DuplicateDefError, MissingParmError, UnknownKeywordError

import re

# A Transformer is a 'data handler' that absorbs input from parser and
# builds a Cpmtools object to represent each definition in the file.
xfm = CPMToolsTransformer(False)

# Instantiate the parser and connect data handlers
parser = Lark(CPMTOOLS,
              lexer           = 'contextual',
              lexer_callbacks = build_callbacks(xfm),
              start           = 'diskdef',
              parser          = 'lalr',
              transformer     = xfm)

defdict = {}

def do_parse(data, linenum):
    global parser, xfm
    xfm.set_start(linenum)
    
    try:
        # Process the input
        parser.parse(data)

        # If we made it here, the parse succeeded. 
        defn = xfm.get_definition()
        if defn.defname in defdict:
            print("WARNING: Duplicate definition '%s' at line %d." % (defn.defname, linenum))
            print("WARNING: Only the first instance will be used")
        else:
            defdict[defn.defname] = defn
            
    except MissingParmError as d:
        print("ERROR: Required parameter(s) missing from definition '%s' (line: %d)" % (d.defname, linenum))
        for parm in d.missing:
            print("%s " % parm, end="")
        print("\n")
        print("ERROR: Skipping this definition")

    except SkewSkewtabError as d:
        print("ERROR: Skew and skewtab both found in definition '%s' (line: %d)" % (d.defname, linenum))
        print("ERROR: Skipping this definition")
        
    except DuplicateParmError as d:
        print("WARNING: Duplicate parameter '%s' in definition '%s' (line: %d)" % (d.parm, d.defname, linenum))
        print("WARNING: Only the first instance will be used")

    # We will only see this if strict checking is enabled
    except UnknownKeywordError as u:
        print("WARNING: Unknown keyword in definition '%s' (line: %d)" % (u.defname, linenum))
        ctxt = u.get_context(data)
        print(ctxt)
        
    except UnexpectedToken as u:
        print("Unxpected token at line: %d, column: %d" % (u.line, u.column))
        ctxt = u.get_context(data)
        print(ctxt)
        if u.expected is not None:
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

dd_rx = re.compile('^diskdef\s+(\S+)')
end_rx = re.compile('^end(\s+|#)?')

try:
    infile = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <diskdef_file>")

state = 'SCAN'

with open(infile, "r") as f:
    data = ""
    defname = None
    linenum = 0
    def_linenum = 0
    for line in f:
        linenum += 1
        dd_m = dd_rx.match(line)
        if dd_m:
            if state == 'DEF':
                print("WARNING: Definition '%s' (line: %d) is missing the end keyword" % (defname, def_linenum))
                print("WARNING: Will fake it, but results may not be correct")
                data += "end\n"
                do_parse(data, def_linenum)
                data = ""
                
            state = 'DEF'
            defname = dd_m.group(1)
            def_linenum = linenum
        elif end_rx.match(line):
            state = 'SCAN'
            data += line
            do_parse(data, def_linenum)
            data = ""
            continue
        
        data += line

    if state == 'DEF':
        print("WARNING: Definition '%s' (line: %d) is missing the end keyword" % (defname, def_linenum))
        print("WARNING: Will fake it, but results may not be correct")
        data += "end\n"
        do_parse(data, def_linenum)

for defname in sorted(defdict.keys()):
    print(defdict[defname])
    
