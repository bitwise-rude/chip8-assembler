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


INSTRUCTIONS = {'cls':      (".",0x00E0,        "Clear the display."),
                "ret":      (".", 0x00EE,       "Return from a subroutine."),

                "jmp" :      ("A.",0x1000,      "Jump to location nnn."),
                "call":     ("A.",0x2000,       "Call subroutine at nnn."),
                "se":       ("XKk.", 0x3000,     "Skip next instruction if Vx = kk."),
                "sne":       ("XKk.", 0x4000,     "Skip next instruction if Vx != kk."),
                "se ^":     ("XX.",0x5000,"Skip next ins if vx = vy"),
                "ld":     ("XKk.",0x6000,"Set Vx = kk."),
                "add":     ("XKk.",0x7000,"Set Vx = Vx + kk."),
                "ld ^":     ("XX.",0x8000,"Set Vx = Vy."),
                "or":     ("XX.",0x8001,"Set Vx = Vx OR Vy."),
                "and":     ("XX.",0x8002,"Set Vx = Vx AND Vy."),
                "xor":     ("XX.",0x8003,"Set Vx = Vx XOR Vy."),
                "add ^":     ("XX.",0x8004,"Set Vx = Vx + Vy, set VF = carry."),
                "sub":     ("XX.",0x8005,"Set Vx = Vx - Vy, set VF = not borrow."),
                "shr":     ("XX.",0x8006,"Set Vx = Vx + Vy, set VF = carry."),
                
                }

# the following code increases tee above dictionary to contain all the register info:
# TODO TODO TODO make it cool
to_pop = []
to_update = []
for ins in INSTRUCTIONS.keys():
    if "^" in ins:
        to_pop.append(ins)

        for i in range(len(REGISTERS)):
        
            new_key = ins.replace("^",REGISTERS[i])
            new_val_0 = INSTRUCTIONS[ins][0]
            new_val_1 = INSTRUCTIONS[ins][1] | (i<<8)
            new_val_2 = INSTRUCTIONS[ins][2] # TODO: new documentation also chagne
            to_update.append({new_key:(new_val_0,new_val_1,new_val_2)})

for update in to_update:
     INSTRUCTIONS.update(update)
     
for ins in to_pop:
        INSTRUCTIONS.pop(ins)


# The instructions are always 4 bytes
INSTRUCTIONS_BYTES = 4