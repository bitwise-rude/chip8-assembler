# make less clustured
import string

#######
# tokens

NEW_LINE = "\n"
SPACE  = " "
COLON = ":"
COMMENT = ";"
COMMA = ","
VALID_NUMBERS = "0123456789"
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


INSTRUCTIONS = {'cls':      (".",0x00E0,        "Clear the display."),
                "ret":      (".", 0x00EE,       "Return from a subroutine."),

                "jmp" :      ("A.",0x1000,      "Jump to location nnn."),
                "call":     ("A.",0x2000,       "Call subroutine at nnn."),
                "jmpa":     ("A.",0xB000,       "Jump to location address + V0."),
                "ld i":     ("A.", 0xA000,      "The value of register I is set to nnn."),

                "se":       ("XKk.", 0x3000,     "Skip next instruction if Vx = kk."),
                "sne":       ("XKk.", 0x4000,     "Skip next instruction if Vx != kk."),
                # TODO: one with registers
                "ld":       ("XKk.", 0x6000,     "The interpreter puts the value kk into register Vx."),

                }


# The instructions are always 4 bytes
INSTRUCTIONS_BYTES = 4