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

OTHERS = ["st","dt","i"]


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

                "se":       (("X K", 0x3000,     "Skip next instruction if Vx = kk."),
                             ("X X",0x5000, "Skip next ins if vx = xy")),

                "sne":       (("X K", 0x4000,     "Skip next instruction if Vx != kk."),)    ,

                "ld":     (("X K",0x6000,"Set Vx = kk."),
                            ("X X",0x8000,"Set vx = vy"),
                            ("i A",0xA000,"Set I = nnn"),
                            ("X dt",0XF007,"The value of DT is placed into Vx."),
                            ("X k",0xF00A,"Wait for a key press, store the value of the key in Vx."),
                            ("dt X",0XF015,"Set delay timer = Vx."),),


                "add":     (("X K",0x7000,"Set Vx = Vx + kk."),
                            ("X X",0x8004, "Set Vx = Vx  + Vy")),

                "or":    ( ("X X",0x8001,"Set Vx = Vx OR Vy."),),
                "and":     (("X X",0x8002,"Set Vx = Vx AND Vy."),),
                "xor":     (("X X",0x8003,"Set Vx = Vx XOR Vy."),),
                "sub":     (("X X",0x8005,"Set Vx = Vx - Vy, set VF = not borrow."),),
                "shr":     (("X X",0x8006,"Set Vx = Vx SHR 1."),),
                "subn":    ( ("X X",0x8007,"Set Vx = Vy - Vx, set VF = NOT borrow."),),
                "shl":     ( ("X X",0x800e,"Set Vx = Vx SHL 1."),),
               "sne":      (("X X",0x9000,"Skip next instruction if Vx != Vy."),),
                "jumpa":      (("A",0xB000,"Jump to location nnn + V0."),),
                "rnd":      (("X K",0xC000,"Set Vx = random byte AND kk."),),
                "drw":      (("X X N",0xD000,"Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision."),),
                "skp":      (("X",0xE09E,"Skip next instruction if key with the value of Vx is pressed."),),
                "sknp":      (("X",0xE091,"Skip next instruction if key with the value of Vx is not pressed."),),
                # "jumpa":      (("A",0xB000,"Jump to location nnn + V0."),),
                # "jumpa":      (("A",0xB000,"Jump to location nnn + V0."),),
                # "jumpa":      (("A",0xB000,"Jump to location nnn + V0."),),
                # "jumpa":      (("A",0xB000,"Jump to location nnn + V0."),),
                # "jumpa":      (("A",0xB000,"Jump to location nnn + V0."),),
                # "jumpa":      (("A",0xB000,"Jump to location nnn + V0."),),
                # "jumpa":      (("A",0xB000,"Jump to location nnn + V0."),),
                # "jumpa":      (("A",0xB000,"Jump to location nnn + V0."),),

                
                }


# The instructions are always 4 bytes
INSTRUCTIONS_BYTES = 4