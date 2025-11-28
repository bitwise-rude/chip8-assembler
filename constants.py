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
MULTI_CHAR_NAMES = {"cls":"CLS"} # 

# DONOT CHANGE THIS, this defines what each instruction do
INSTRUCTIONS = {'CLS':[0,(),lambda : 0x00E0]}