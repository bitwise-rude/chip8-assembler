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


INSTRUCTIONS = {'cls':      (("",0x00E0,        "Clear the display."),),
                "ret":      (("", 0x00EE,       "Return from a subroutine."),),

                "jmp" :      (("A",0x1000,      "Jump to location nnn."),),
                "call":    ( ("A",0x2000,       "Call subroutine at nnn."),),
                "se":       (("XK", 0x3000,     "Skip next instruction if Vx = kk."),
                             "XX",0x5000, "Skip next ins if vx = xy"),

                "sne":       ("XKk.", 0x4000,     "Skip next instruction if Vx != kk."),

                ("se","v0"):     ("XX.",0x5000,"Skip next ins if vx = vy"),
                ("se","v1"):     ("XX.",0x5100,"Skip next ins if vx = vy"),
                ("se","v2"):     ("XX.",0x5200,"Skip next ins if vx = vy"),
                ("se","v3"):     ("XX.",0x5300,"Skip next ins if vx = vy"),
                ("se","v4"):     ("XX.",0x5400,"Skip next ins if vx = vy"),
                ("se","v5"):     ("XX.",0x5500,"Skip next ins if vx = vy"),
                ("se","v6"):     ("XX.",0x5600,"Skip next ins if vx = vy"),
                ("se","v7"):     ("XX.",0x5700,"Skip next ins if vx = vy"),
                ("se","v8"):     ("XX.",0x5800,"Skip next ins if vx = vy"),
                ("se","v9"):     ("XX.",0x5900,"Skip next ins if vx = vy"),
                ("se","va"):     ("XX.",0x5a00,"Skip next ins if vx = vy"),
                ("se","vb"):     ("XX.",0x5b00,"Skip next ins if vx = vy"),
                ("se","vc"):     ("XX.",0x5c00,"Skip next ins if vx = vy"),
                ("se","vd"):     ("XX.",0x5d00,"Skip next ins if vx = vy"),
                ("se","ve"):     ("XX.",0x5e00,"Skip next ins if vx = vy"),
                ("se","vf"):     ("XX.",0x5f00,"Skip next ins if vx = vy"),

                ("ld",""):     ("XKk.",0x6000,"Set Vx = kk."),
                ("add",""):     ("XKk.",0x7000,"Set Vx = Vx + kk."),

                ("ld","v0"):     ("XX.",0x8000,"Set Vx = Vy."),
                ("ld","v1"):     ("XX.",0x8100,"Set Vx = Vy."),
                ("ld","v2"):     ("XX.",0x8200,"Set Vx = Vy."),
                ("ld","v3"):     ("XX.",0x8300,"Set Vx = Vy."),
                ("ld","v4"):     ("XX.",0x8400,"Set Vx = Vy."),
                ("ld","v5"):     ("XX.",0x8500,"Set Vx = Vy."),
                ("ld","v6"):     ("XX.",0x8600,"Set Vx = Vy."),
                ("ld","v7"):     ("XX.",0x8700,"Set Vx = Vy."),
                ("ld","v8"):     ("XX.",0x8800,"Set Vx = Vy."),
                ("ld","v9"):     ("XX.",0x8900,"Set Vx = Vy."),
                ("ld","va"):     ("XX.",0x8a00,"Set Vx = Vy."),
                ("ld","vb"):     ("XX.",0x8b00,"Set Vx = Vy."),
                ("ld","vc"):     ("XX.",0x8c00,"Set Vx = Vy."),
                ("ld","vd"):     ("XX.",0x8d00,"Set Vx = Vy."),
                ("ld","ve"):     ("XX.",0x8e00,"Set Vx = Vy."),
                ("ld","vf"):     ("XX.",0x8f00,"Set Vx = Vy."),

                ("or",""):     ("XX.",0x8001,"Set Vx = Vx OR Vy."),
                ("and",""):     ("XX.",0x8002,"Set Vx = Vx AND Vy."),

                ("xor",""):     ("XX.",0x8003,"Set Vx = Vx XOR Vy."),
                

                ("add","v0"):     ("XX.",0x8004,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","v1"):     ("XX.",0x8104,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","v2"):     ("XX.",0x8204,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","v3"):     ("XX.",0x8304,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","v4"):     ("XX.",0x8404,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","v5"):     ("XX.",0x8504,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","v6"):     ("XX.",0x8604,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","v7"):     ("XX.",0x8704,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","v8"):     ("XX.",0x8804,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","v9"):     ("XX.",0x8904,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","va"):     ("XX.",0x8a04,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","vb"):     ("XX.",0x8b04,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","vc"):     ("XX.",0x8c04,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","vd"):     ("XX.",0x8d04,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","ve"):     ("XX.",0x8e04,"Set Vx = Vx + Vy, set VF = carry."),
                ("add","vf"):     ("XX.",0x8f04,"Set Vx = Vx + Vy, set VF = carry."),
                

                ("sub",""):     ("XX.",0x8005,"Set Vx = Vx - Vy, set VF = not borrow."),
                ("shr",""):     ("XX.",0x8006,"Set Vx = Vx SHR 1."),
                ("subn",""):     ("XX.",0x8007,"Set Vx = Vy - Vx, set VF = NOT borrow."),
                ("shl",""):      ("XX.",0x800e,"Set Vx = Vx SHL 1."),
                ("sne",""):      ("XX.",0x9000,"Skip next instruction if Vx != Vy."),
                ("ld","i"):     ("A.",0xA000,"Set I = nnn.")
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