# make less clustured
import string

#######
# tokens

NEW_LINE = "\n"
SPACE  = " "
COLON = ":"
COMMENT = ";"
VALID_CHARACTERS = string.ascii_lowercase + "_"

######
# names


# you can change the keys to alias them permanently, please use lowercase
SINGLE_CHAR_NAMES = {"a":"REG_A", "b":"REG_B"}
MULTI_CHAR_NAMES = {} # 



#####
#instructions

# INSTRUCTIONS HAVE THE FOLLOWING TEMPLATE
###
# R deonts the retrunign opcode
# A denotes a 3-bit address, as a parameter
## . denotes skip

# KEYS(NAME) : [(arg_lsit), opcode]


INSTRUCTIONS = {'cls':      ("R.",0x00E0),
                "ret":      ("R.", 0x00EE),
                "jp" :      ("RA.",0x1000),
                }


# The instructions are always 4 bytes
INSTRUCTIONS_BYTES = 4