# written by Meyan Adhikari
import sys
from constants import *
from dataclasses import dataclass

@dataclass
class Token:
    '''Represent Basic Unit'''
    name:str
    line_no:int
    char_index_start:int
    char_index_end:int
    type:str

class ErrorManager:
    '''Shows Error, its type and description neatly'''
    def __init__(self,source:list[str]):
        self.source = source
        self.errors = []

    def add_error(self,
                  name:str,
                  token:Token,
                  description:str) -> None:
        '''Adds error to an error buffer'''
        
        error_message = f"""
            {name} at {token.line_no+1}:{token.char_index_start+1}"""
        
        line_of_error = self.source[token.line_no]

        line_description = " " * (token.char_index_end)
        error_shower = "^" * (token.char_index_end - token.char_index_start+1)

        self.errors.append(f'''{error_message}
                           {line_of_error}
                           {line_description + error_shower}
{description}
                        ''')

    def show_errors(self,_quit:bool=False) -> bool:
        '''
            Shows all the errors stored in the buffer
            quit:bool -> to quit the program if error or not
        '''

        if self.errors:
            for error in self.errors:
                print(error)
            
            if _quit:
                show_err_and_quit("Error(s) Occured.")
            return True
        else:
            return False
        

class Tokenizer:
    '''
        Tokenizer or Lexer produces lexemes or Toknes
        which are assembler interpretation of the code
        and its attributes
    '''

    def __init__(self,error_manager:ErrorManager) -> None:
        self.source_lines = error_manager.source 
        self.tokens = []
        self.errors = []
        self.error_manager = error_manager
        

    def tokenize(self) -> None:
        '''Main tokenizing method'''
        # go through each line
        line_count = 0
    
        while line_count < len(self.source_lines):
            line = self.source_lines[line_count].lower() # making case insensitive
            character_count = 0

            while character_count < len(line):
                character = line[character_count]

                # single character keywords check 
                if character in SINGLE_CHARACTER_TOKENS.keys():
                    # special cases are comments and spaces which need to be discarded
                    tkn_name = SINGLE_CHARACTER_TOKENS[character]

                    if tkn_name == "_COMMENT": # comments
                        #skip the whole line
                        self.tokens.append(Token("_NEW_LINE",
                                                 line_count,
                                                 character_count,
                                                 character_count,
                                                 "KEYWORD"
                                           ) )
                        character_count = len(line)
                        continue
                
                    elif tkn_name == "_SPACE": # spaces
                        # skip the character
                        character_count += 1
                        continue
                    
                    self.tokens.append(Token(tkn_name,
                                       line_count,
                                       character_count,
                                       character_count,
                                       "KEYWORD")) # since single character
                      
                # multi character check and single character names check
                elif character in VALID_CHARACTERS:
                    buffer = ""
                    character_start = character_count

                    while character in VALID_CHARACTERS+VALID_NUMBERS:          
                        buffer += character
                        character_count +=1

                        if character_count < len(line):
                            character = line[character_count]
                        else:
                            break
                    
                    # several types
                    if buffer in REGISTERS:
                        _type = "REGISTER"
                    else:
                        _type = "NAME"

                    self.tokens.append(Token(buffer.strip(),
                                             line_count, 
                                             character_start,
                                             character_count,
                                             _type))
                    continue

                # numbers check

                # decimals
                elif character in VALID_NUMBERS:
                    buffer = ""
                    character_start = character_count

                    while character in VALID_NUMBERS:          
                        buffer += character
                        character_count +=1

                        if character_count < len(line):
                            character = line[character_count]
                        else:
                            break

                    self.tokens.append(Token(buffer.strip(),
                                             line_count, 
                                             character_start,
                                             character_count,
                                             "NUMBER"))
                    continue
                
                # hexdecimal
                elif character == HEX_PREFIX:
                    buffer = ""
                    character_start = character_count

                    while character in VALID_HEX or (character_start == character_count and character == HEX_PREFIX):          
                        buffer += character
                        character_count +=1

                        if character_count < len(line):
                            character = line[character_count]
                        else:
                            break
                    num = buffer.strip()[1:]
                    num = num if num !="" else "0"
                    self.tokens.append(Token(num, # for the dollar
                                             line_count, 
                                             character_start,
                                             character_count,
                                             "HEX"))
                    
                    continue

                # binary TODO ins single time
                
                elif character == BIN_PREFIX:
                    buffer = ""
                    character_start = character_count

                    while character in VALID_BIN or (character_start == character_count and character == BIN_PREFIX):          
                        buffer += character
                        character_count +=1

                        if character_count < len(line):
                            character = line[character_count]
                        else:
                            break
                    num = buffer.strip()[1:]
                    num = num if num !="" else "0"
                    self.tokens.append(Token(num, # for the dollar
                                             line_count, 
                                             character_start,
                                             character_count,
                                             "BIN"))
                    
                    continue
                
                else:
                    self.error_manager.add_error("Unknown Character",
                                                 Token("_",line_count,character_count,character_count,"_"),
                                                 "The above character doesn't belong ot the syntax.")

                character_count += 1
            line_count +=1

class Parser:
    '''Parses tokens into suitable machine codes'''

    def __init__(self,tokens:list[Token],error_manager:ErrorManager) -> None:
        self.tokens = tokens
        self.error_manager = error_manager

        self.labels = {} # stores and labels and the address
        self.unknown_labels = {}
        self.current_address = 0x0200

        self.generated_code = bytearray() # final machine code will be here
    
    def add_ins(self,ins:int,isSingleByte = False) -> None:
        '''
            Converts `ins` a 2 byte instruction to the bytearray
            by seperating into LSB and MSB
        '''
        lsb = ins & 0x00FF
        msb = (ins&0xFF00) >> 8

        if not isSingleByte:
            self.generated_code.append(msb)
            self.generated_code.append(lsb)
            self.current_address += INSTRUCTIONS_BYTES
        else:
            self.generated_code.append(ins & 0xFF)
            self.current_address += 1

        


    def parse(self)->None:
        '''
            Main parsing method
        '''

        tkn_counter = 0
        
        # this also contain two passes first for label detection and next for actual thing
        while tkn_counter < len(self.tokens):
            tkn = self.tokens[tkn_counter]
            if tkn.type == "NAME":
                if tkn_counter+1<len(self.tokens) and self.tokens[tkn_counter+1].name == "_COLON":
                    self.labels.update({tkn.name:None}) # right now address is unknown #TODO: make it nice
                    self.unknown_labels.update({tkn.name:[]})
            tkn_counter += 1

        tkn_counter = 0

        # parsing through all of the token
        while tkn_counter < len(self.tokens):
            tkn = self.tokens[tkn_counter]

            # diff types of tokens 
            if tkn.name in INSTRUCTIONS.keys():
                # if is an instructions

                fullparams = self._get_param(tkn_counter)  # get paramter
                fullparams.reverse()

                # check for opcode based on the parameters name
                opcodes_data = INSTRUCTIONS[tkn.name]

                for opcode_data in opcodes_data:
                    _template = opcode_data[0].split()
                    _opcode = opcode_data[1]
        
                    # if skip
                    to_skip = False

                    # I call the following way, the Ks way of assembling 
                    i = 0
                    param_counter = 0
                    print(_opcode)
                    result = 0x0000 | _opcode

                    params = fullparams.copy()
            
                    while i < len(_template): 
                        k = _template[i]
                        print(params)
                        if (k == "A"):  # for address
                            # for A we need (nnn)
                            if (len(params)>0):
                                _p = params.pop()
                                if _p.type == "NUMBER":
                                    nnn = int(_p.name) & 0x0FFF # getting those nnn only
                                    result |=nnn
                                else:
                                    to_skip = True
                                    break
                            else:
                                to_skip = True
                                break
            
                        elif (k == "X"):
                            # X is a single nibble for a register
                            if (len(params)>0):
                                x = params.pop()
                               
                                # could be register or a number
                        
                                if x.type == "REGISTER":
                                    t = REGISTERS.index(x.name)
                                elif x.type == "NUMBER":
                                    t = int(x.name) &  0x000F
                                else:
                                    to_skip = True
                                    break
                            # & 0x000F # getting those X only
                            # i denots the position, actually i+1 does since 1st is always constant
                           
                                result |= (t<<(((2-param_counter))*4)) #TODO this 2 and 1 wont' work properyl please not
                                # param counter is only use TODO there for ld dt,5 to work please fix
                            else:
                                to_skip = True
                                break
                        
                        elif (k == "N"):
                            # N is a nibble
                            if (len(params)>0):
                                _p = params.pop()
                                if _p.type == "NUMBER":
                                    x = int(_p.name) & 0x000F # getting those n only

                                    result |= x
                                else:
                                    to_skip  = True
                                    break
                            else:
                                to_skip = True
                                break
                            
                            

                            
                        elif (k == "K"):
                            # K is a single byte
                            if (len(params)>0):
                                _p = params.pop()
                                
                                if _p.type == "NUMBER":
                                    x = int(_p.name) & 0x00FF # getting those kk only
                                # i denots the position, actually i+1 does since 1st is always constant

                                    result |= (x<<(((1-i))*4))
                                else:
                                    to_skip  = True
                                    break
                            else:
                                to_skip = True
                                break
                        
                        else:
                            if (len(params)>0):
                                _p = params.pop()
                                if _p.name != k:
                                    to_skip = True
                                else:
                                    param_counter -=1
                            else:
                                to_skip = True
                                break

                        i+=1 
                        param_counter += 1 # see this

                    if (to_skip): # this is not correct
                        continue  
                    else: # this is the correct
                        
                        break
                else:
                    # if no correct found 
                    # TODO: show correct parameters
                    self.error_manager.add_error("Incorrect Paramter",
                                                 tkn,
                                                 f"{tkn.name} expects paramters. No correct paramter has been passed"
                                                 )
                self.add_ins(result)
            
            elif tkn.type == "NAME":
                # if is a label
                if tkn_counter+1<len(self.tokens) and self.tokens[tkn_counter+1].name == "_COLON":
                    self.labels.update({tkn.name:self.current_address})

                if tkn.name == "db":
                    # define bytes thing
                    params = self._get_param(tkn_counter)
                    
                    for param in params:
                        if param.type == "NUMBER":
                            self.add_ins(int(param.name),isSingleByte=True)
                        else:
                            self.error_manager.add_error("Define Bytes failed",
                                                         param,
                                                         f'{param.name} cannot be defined in the memory')
    
            tkn_counter +=1
        
    # helper functions for parsing
    def _get_param(self,tkn_counter) -> list[Token]:
        params = []

        i = 0
        while (tkn_counter  + i + 1 < len(self.tokens)):

            param_token = self.tokens[tkn_counter  + i + 1]
            if param_token.name == "_NEW_LINE":
                break

            if i%2 !=0:
                if param_token.name != "_COMMA":
                    self.error_manager.add_error(f"Expected a comma",
                                            param_token,
                                            f"'{param_token.name}' isn't a valid parameter seperator")
                else:
                    i +=1
                    continue
            
            if param_token.type == "NAME":
                # is an address?
                if param_token.name in self.labels.keys():
                    
                    param_token.name  = str(self.labels[param_token.name])

                    # if param_token == "None":
                    #     self.unknown_labels[param_token.name].append(self.current_address)
                    #     pass

                    param_token.type = "NUMBER"
            
            elif param_token.type == "HEX":
                param_token.type ="NUMBER"
                param_token.name = str(int(param_token.name, base =16))
            
            elif param_token.type == "BIN":
                param_token.type ="NUMBER"
                param_token.name = str(int(param_token.name, base =2))

            params.append(param_token)
            
            # if param_token.type == "NUMBER" or param_token.type == "REGISTER":
            #     params.append(param_token)
            # else:
            #     self.error_manager.add_error(f"Invalid Paramter",
            #                                 param_token,
            #                                 f"'{param_token.name}' isn't a valid parameter")
            #     param_token.name = "1"
            #     param_token.type = "NUMBER"
            #     params.append(param_token)

            # TODO: varaible checking do  
            # TODO: ERROR
       
            
            i += 1

        return params
            

def show_err_and_quit(err:str):
    '''
        Prints error `err` and quits.
    '''
    print("\tch8asm:\nError:\t",err)
    quit()

def read_file_contents(file_name : str) -> list[str]:
    '''Reads and returns the file contents'''
    try:
        file_handler = open(file_name,'r')
        return file_handler.readlines()
    except FileNotFoundError:
        show_err_and_quit("The source file wasn't found")
    #handle other erros as well

def save_in_file(file_name:str, data:bytearray) -> None:
    ''' Saves the byte array in the file'''
    try:
        file_handler = open(file_name,'wb')
        file_handler.write(data)
    except FileNotFoundError:
        show_err_and_quit("The destination file wasn't found")

if len(sys.argv) < 2: 
    show_err_and_quit("Source File Needed")

# read the file 
source_lines = read_file_contents(sys.argv[1])

# error manager
error_manager = ErrorManager(source_lines)

# tokenizer (first pass)
tokenizer = Tokenizer(error_manager)
tokenizer.tokenize()
print(tokenizer.tokens)

# show errors in tokenizing phase
if error_manager.show_errors():
    show_err_and_quit("Syntax Error")

# parser (second pass)
parser = Parser(tokenizer.tokens,error_manager)
parser.parse()

if error_manager.show_errors():
    show_err_and_quit("Parsing Error")
print(parser.generated_code.hex(sep="-"))

# save it out in a file
if (len(sys.argv)>2):
    save_file = sys.argv[2]
else:
    save_file = "out.bin"

save_in_file(save_file,parser.generated_code)
