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

# DONOT CHANGE THIS, this defines what each instruction do

#INSTRUCTIONS HAVE THE FOLLOWING TEMPLATE
# KEYS(NAME) : [(arg_lsit), (function_that_returns the opcode)]

INSTRUCTIONS = {'cls':[(),lambda : 0x00E0],
                "ret": [(), lambda : 0x00EE],
                }