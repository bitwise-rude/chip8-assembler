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

        self.generated_code = bytearray() # final machine code will be here
    
    def add_ins(self,ins:int) -> None:
        '''
            Converts `ins` a 2 byte instruction to the bytearray
            by seperating into LSB and MSB
        '''
        lsb = ins & 0x00FF
        msb = (ins&0xFF00) >> 8

        self.generated_code.append(msb)
        self.generated_code.append(lsb)

    def parse(self)->None:
        '''
            Main parsing method
        '''

        tkn_counter = 0

        # parsing through all of the token
        while tkn_counter < len(self.tokens):
            tkn = self.tokens[tkn_counter]

            # diff types of tokens 
            if tkn.name in INSTRUCTIONS.keys():
                # if is an instructions

                params = self._get_param(tkn_counter)  # get paramter

                # check for opcode based on the parameters name
                opcodes_data = INSTRUCTIONS[tkn.name]

                for opcode_data in opcodes_data:
                    _template = opcode_data[0]



                        
                if i ==1:
                    tkn_name = tkn_name[:-1] 

                #TODO: check if exist, TODO remove this?
                if tkn_name in INSTRUCTIONS.keys():
                    _ins = INSTRUCTIONS[tkn_name]  
                    tkn.name = tkn_name
                elif tkn.name in INSTRUCTIONS.keys():
                    _ins = INSTRUCTIONS[tkn.name] 
                else:
                    self.error_manager.add_error("Invalid Paramter",
                                                 p,
                                                 f"{p.name} isn't a valid parameter for {tkn.name}")
                    tkn_counter +=1
                    continue
                
                _template = _ins[0]
                _opcode = _ins[1]


                # I call the following way, the Ks way of assembling 
                i = 0
                result = 0x0000 | _opcode

                # print(_template,hex(_opcode))
                # quit()
                 # done for convinience sake
            
                # TODO: check if paramters are more than needed (maybe a third pass for warnings?)
            
                while i < INSTRUCTIONS_BYTES:
                    k = _template[i]

                    if(k=="."):break
                    
                    elif (k == "A"):  # for address
                        # for A we need (nnn)
                        if (len(params)>0):
                            nnn = int(params.pop().name) & 0x0FFF # getting those nnn only
                            result |=nnn
                        else:
                            error_manager.add_error("Expected a parameter",
                                                    tkn.line_no,
                                                    tkn.char_index_start,
                                                    tkn.char_index_end,
                                                    f"'{tkn.name}' expects an Address (nnn) parameter. None were provided"
                                                  )
                            
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
                            # & 0x000F # getting those X only
                            # i denots the position, actually i+1 does since 1st is always constant
                           
                            result |= (t<<(((2-i))*4))
                            
                        else:
                        
                            error_manager.add_error("Expected a parameter",
                                                    tkn,
                                                    f"'{tkn.name}' expects an Register (x) parameter. None were provided"
                                                  )
                            break
                            
                    elif (k == "K"):
                        # K is a single byte
                        if (len(params)>0):
                            x = int(params.pop().name) & 0x00FF # getting those kk only
                            # i denots the position, actually i+1 does since 1st is always constant

                            result |= (x<<(((1-i))*4))
                        else:
                            error_manager.add_error("Expected a parameter",
                                                    tkn,
                                                    f"'{tkn.name}' expects an immediate value parameter (kk). None were provided"
                                                  )
                            break
                            
                           
                    # else show an error?

                    i+=1;   
                self.add_ins(result)
            
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
            
            if param_token.type == "NUMBER" or param_token.type == "REGISTER":
                params.append(param_token)
            else:
                self.error_manager.add_error(f"Invalid Paramter",
                                            param_token,
                                            f"'{param_token.name}' isn't a valid parameter")
                param_token.name = "1"
                param_token.type = "NUMBER"
                params.append(param_token)

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
