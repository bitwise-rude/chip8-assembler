# make less clustured
import string

#######
# tokens

SINGLE_CHARACTER_TOKENS  = {    "\n":"_NEW_LINE",
                                " " :"_SPACE",
                                ";" : "_COMMENT",
                                "," : "_COMMA",
                            }

VALID_NUMBERS = "0123456789"
VALID_CHARACTERS = string.ascii_lowercase + "_"

REGISTERS = ["v"+hex(i)[2:] for i in range(0,16)] # v0, v1,...vf


#####
#instructions

# INSTRUCTIONS HAVE THE FOLLOWING TEMPLATE
###
# R deonts the retrunign opcode
# A denotes a 3-bit address, as a parameter
## . denotes skip
# ^ denotes that this needs to be expanded for all the registers

# KEYS(NAME) : [(arg_lsit), opcode]


INSTRUCTIONS = {'cls':      (("",0x00E0,        "Clear the display."),)     ,
                "ret":      (("", 0x00EE,       "Return from a subroutine."),)  ,
                "jmp" :      (("A",0x1000,      "Jump to location nnn."),)      ,
                "call":    (( "A",0x2000,       "Call subroutine at nnn."),)      ,

                "se":       (("XK", 0x3000,     "Skip next instruction if Vx = kk."),
                             ("XX",0x5000, "Skip next ins if vx = xy")),

                "sne":       (("XK", 0x4000,     "Skip next instruction if Vx != kk."),)    ,

                "ld":     (("XK",0x6000,"Set Vx = kk."),
                            ("XX",0x8000,"Set vx = vy")),

                "add":     (("XK",0x7000,"Set Vx = Vx + kk."),
                            ("XX",0x8004, "Set Vx = Vx  + Vy")),

                "or":    ( ("XX",0x8001,"Set Vx = Vx OR Vy."),),
                "and":     (("XX",0x8002,"Set Vx = Vx AND Vy."),),
                "xor":     (("XX",0x8003,"Set Vx = Vx XOR Vy."),),
                "sub":     (("XX",0x8005,"Set Vx = Vx - Vy, set VF = not borrow."),),
                "shr":     (("XX",0x8006,"Set Vx = Vx SHR 1."),),
                "subn":    ( ("XX",0x8007,"Set Vx = Vy - Vx, set VF = NOT borrow."),),
                "shl":     ( ("XX",0x800e,"Set Vx = Vx SHL 1."),),
               "sne":      (("XX.",0x9000,"Skip next instruction if Vx != Vy."),),
                # ("ld","i"):    ( ("A.",0xA000,"Set I = nnn."),)
                }


# The instructions are always 4 bytes
INSTRUCTIONS_BYTES = 4