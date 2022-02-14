TWOTWODISK = r"""

// Bring in some standard notions
%import common.INT
%import common.LETTER
%import common.DIGIT
%import common.WS
%import common.HEXDIGIT

// Discard WS
%ignore WS

// Track comments with lexer callback
COMMENT: /NOTE.*/
%ignore COMMENT

// Parser grammar starts here
//
start: diskdef+

diskdef: "BEGIN"i defname [description] _contents

description: DESCRIPTION
DESCRIPTION: /.+/

defname: DEFNAME
DEFNAME: (LETTER|DIGIT)~1..4

_contents: real 
        | reference

real: parm+ "END"i

reference: /SEE/i DEFNAME                  -> label

parm: /DENSITY/i /FM|MFM/i "," /LOW|HIGH/i -> density
    | /COMPLEMENT/i                        -> flag
    | /SKIP/i                              -> flag
    | IPARM num                            -> intparm
    | /SECTORS/i num "," num               -> sectors
    | /SIDE1/i num numlist ("," numlist)*  -> side 
    | /SIDE2/i num numlist ("," numlist)*  -> side 
    | /ORDER/i /CYLINDERS|EAGLE|COLUMBIA/i -> order
    | /ORDER/i /SIDES/i /EVEN-ODD/i?       -> order
    | /LABEL/i DEFNAME                     -> label 

IPARM: "CYLINDERS"i
     | "SIDES"i
     | "SKEW"i
     | "BSH"i
     | "BLM"i
     | "EXM"i
     | "DSM"i
     | "DRM"i
     | "AL0"i
     | "AL1"i
     | ["S"i] "OFS"i

numlist: INT ("," INT)+

num: INT -> intval
   | HEXVAL -> hexval
   | BINVAL -> binval

HEXVAL.1: HEXDIGIT+ "H"i
BINVAL: /0|1/+ "B"i

"""

def build_callbacks(obj):
    return {'IPARM': obj.lex_sofs,
            'COMMENT': obj.lex_comment}
