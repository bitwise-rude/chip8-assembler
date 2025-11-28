# written by Meyan Adhikari
import sys
from constants import *

class ErrorManager:
    def __init__(self,source:list[str]):
        self.source = source
        self.errors = []

    def add_error(self,name:str,line_no:int,char_no_start:int,char_no_end:int,description:str):
        error_message = f"""
            {name} at {line_no+1}:{char_no_start+1}"""
        
        line_of_error = self.source[line_no]

        line_description = " " * (char_no_start)
        error_shower = "^" * (char_no_end - char_no_start+1)

        self.errors.append(f'''{error_message}
                           {line_of_error}
                           {line_description + error_shower}
{description}
                        ''')

    def show_errors(self,_quit=False) -> bool:
        if self.errors:
            for error in self.errors:
                print(error)
            
            if _quit:
                show_err_and_quit("Error(s) Occured.")
            return True
        else:
            return False

class Token:
    '''Represent Basic Unit'''
    def __init__(self,name:str,line_no:int,char_index_start:int, char_index_end:int, isNumber = False)->None:
        '''

        '''
        self.name = name
        self.line_no = line_no
        self.char_index_start = char_index_start
        self.char_index_end = char_index_end
        self.is_number = isNumber
      
    def __repr__(self) -> str:
        return f"NAME:{self.name} IS NUMBER: {self.is_number}"


class Tokenizer:
    def __init__(self,error_manager:ErrorManager) -> None:
        self.source_lines = error_manager.source 
        self.tokens = []
        self.errors = []
        self.error_manager = error_manager

    def tokenize(self) -> None:
        # go through each line
        line_count = 0
    
        while line_count < len(self.source_lines):
            line = self.source_lines[line_count].lower() # making case insensitive
            character_count = 0
            # go through each character 
            while character_count < len(line):
                character = line[character_count]

                # single character check , TODO: use a loop to do these all 
                if character == NEW_LINE:
                    self.tokens.append(Token("_NEW_LINE",line_count,character_count,character_count))

                elif character == COLON:
                    self.tokens.append(Token("_COLON",line_count,character_count,character_count))
                
                elif character == COMMA:
                    self.tokens.append(Token("_COMMA",line_count,character_count,character_count))

                elif character == COMMENT:
                    #skip the whole line 
                    character_count = len(line)
                    continue
                
                elif character == SPACE:
                    # skip the character
                    character_count += 1
                    continue
                
                # multi character check and single character names check
                elif character in VALID_CHARACTERS:
                    buffer = ""
                    character_start = character_count
                    while character in VALID_CHARACTERS:
                        buffer += character
                        character_count +=1

                        if character_count < len(line):
                            character = line[character_count]
                        else:
                            break

                    is_number = True if len([i for i in buffer if i in VALID_NUMBERS]) == len(buffer) else False

                    self.tokens.append(Token(buffer,line_count, character_start,character_count,is_number))
                else:
                    self.error_manager.add_error("Unknown Character",line_count,character_count,character_count,"The above character doesn't belong ot the syntax.")

                character_count += 1
            line_count +=1

class Parser:
    def __init__(self,tokens:list[Token],error_manager:ErrorManager) -> None:
        self.tokens = tokens
        self.error_manager = error_manager

        self.generated_code = bytearray()
    
    # def _show_err(des):
    #         self.error_manager.add_error("Expected a parameter.",
    #                                      crnt_token.line_no,
    #                                      crnt_token.char_index_start,
    #                                      crnt_token.char_index_end,
    #                                      des
    #                                      )
    #         self.error_manager.show_errors(_quit = True)
    
    def add_ins(self,ins:int):
        lsb = ins & 0x00FF
        msb = (ins&0xFF00) >> 8

        self.generated_code.append(msb)
        self.generated_code.append(lsb)

    def parse(self)->None:
        tkn_counter = 0
        # parsing through all of the token
        while tkn_counter < len(self.tokens):
            tkn = self.tokens[tkn_counter]
            # diff types of tokens 
            if tkn.name in INSTRUCTIONS.keys():
                # if is an instructions
                _ins = INSTRUCTIONS[tkn.name]
                _template = _ins[0]
                _opcode = _ins[1]

                # I call the following way, the Ks way of assembling 
                i = 0 
                result = 0x0000 | _opcode

                params = self._get_param(tkn_counter)  # get paramter
                params.reverse() # done for convinience sake
                # TODO: check if paramters are more than needed (maybe a third pass for warnings?)
            
                while i < INSTRUCTIONS_BYTES:
                    k = _template[i]

                    if(k=="."):break
                    
                    elif (k == "A"):  # for address
                        # for A we need (nnn)
                        if (len(params)>0):
                            nnn = params.pop() & 0x0FFF # getting those nnn only
                            result |=nnn
                        else:
                            error_manager.add_error("Expected a parameter",
                                                    tkn.line_no,
                                                    tkn.char_index_start,
                                                    tkn.char_index_end,
                                                    f"'{tkn.name}' expects an Address (nnn) parameter. None were provided"
                                                  )
                    # else show an error?

                    i+=1;   

                self.add_ins(result)
            
            tkn_counter +=1
        
    # helper functions for parsing
    def _get_param(self,tkn_counter) -> list[Token]:
        params = []
        i = 0

        while (tkn_counter  + i + 1 < len(self.tokens)):
            param_token = self.tokens[tkn_counter  + 1]

            if param_token.is_number:
                params.append(int(param_token.name))
            elif param_token.name == "_COMMA":
                pass
            elif param_token.name == "_NEW_LINE":
                break
            # TODO: varaible checking do 
            # else:
            #     self.error_manager.add_error("Incorrect Parameter",
            #                                  param_token.line_no,
            #                                  param_token.char_index_start,
            #                                  param_token.char_index_end,
            #                                  f"'{param_token.name}' is not a valid parameter")
            
            i = i + 1
        return params
            

def show_err_and_quit(err:str):
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
    show_err_and_quit("Syntax Error")
print(parser.generated_code.hex(sep="-"))
