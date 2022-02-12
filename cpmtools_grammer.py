CPMTOOLS = r"""

// Bring in some standard notions
%import common.INT
%import common.CNAME
%import common.LETTER
%import common.DIGIT
%import common.CR
%import common.LF
%import common.WS_INLINE

// Discard WS between tokens
%ignore WS_INLINE

// Newline placement is significant to grammar
EOL: CR? LF

// FF + EOL + WS_INLINE account for all WS
FF: /\f/
%ignore FF

// Track comments with lexer callback
COMMENT: /#.*/
%ignore COMMENT

// Parser grammar starts here
//
start: diskdef+ EOL*

diskdef: EOL* DISKDEF defname EOL (pair|EOL)+ END EOL -> end

defname: DEFNAME

DISKDEF: "diskdef"
DEFNAME: (LETTER|DIGIT) ("."|"_"|"-"|LETTER|DIGIT)*
END: "end"

pair:  IPARM INT EOL                          -> intparm
     | SKEWTAB LISTVAL EOL                    -> listparm
     | OFFSET INT [MULTIPLIER [TRAILING]] EOL -> unitparm
     | LIBDISK CNAME EOL                      -> strparm
     | OS OSVAL EOL                           -> strparm

IPARM: "seclen"
     | "tracks"
     | "sectrk"
     | "dirblks"
     | "blocksize"
     | "boottrk"
     | "maxdir"
     | "skew"
     | "logicalextents"

// Give 'skewtab' higher priority than 'skew'
SKEWTAB.1: "skewtab"
OFFSET:    "offset"
LIBDISK:   "libdsk:format"
OS:        "os"

LISTVAL: INT ("," INT)*
OSVAL: "2.2"|"3"|"isx"|"p2dos"|"zsys"

MULTIPLIER: /(k|m|t|s)/i
TRAILING: /\S+/
"""

# Create dictionary to hook lexer actions
def build_callbacks(obj):
    return {'COMMENT': obj.lex_comment,
            'INLINE': obj.lex_comment,
            'EOL': obj.lex_eol,
            'DISKDEF': obj.lex_identifier,
            'IPARM': obj.lex_identifier,
            'SKEWTAB': obj.lex_identifier,                               
            'OFFSET': obj.lex_identifier,
            'LIBDISK': obj.lex_identifier,
            'OS': obj.lex_identifier}
