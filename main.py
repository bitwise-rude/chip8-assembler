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
        error_shower = "^" * (char_no_end - char_no_start)

        self.errors.append(f'''{error_message}
                           {line_of_error}
                           {line_description + error_shower}
                        ''')

    def show_errors(self) -> bool:
        if self.errors:
            for error in self.errors:
                print(error)
        else:
            return False

class Token:
    '''Represent Basic Unit'''
    def __init__(self,name:str,type:str,line_no:int,char_no:int)->None:
        '''
            type:str ->
            RES - Reserved Keywords
            VAR - Variables
            OTH - Others 
        '''
        self.name = name
        self.line_no = line_no
        self.char_no = char_no
        self.type =  type
      
    def __repr__(self) -> str:
        return f"NAME:{self.name} TYPE:{self.type} "


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

                # single character check
                if character == NEW_LINE:
                    self.tokens.append(Token("NEW_LINE","OTH",line_count,character_count))

                elif character == COLON:
                    self.tokens.append(Token("COLON","OTH",line_count,character_count))

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
                    char_start = character_count
                    while character in VALID_CHARACTERS:
                        buffer += character
                        character_count +=1

                        if character_count < len(line):
                            character = line[character_count]
                        else:
                            break

                    if len(buffer) > 1:
                        # multi character
                        if buffer in MULTI_CHAR_NAMES.keys():
                            self.tokens.append(Token(MULTI_CHAR_NAMES[buffer],"RES",line_count, character_count))

                            continue
                        else:
                            self.error_manager.add_error("Unknown Name",line_count,char_start,character_count, "This name is not registered as part of a valid syntax")

                    else:
                        # single character
                        if buffer in SINGLE_CHAR_NAMES.keys():
                            self.tokens.append(Token(SINGLE_CHAR_NAMES[buffer],"RES",line_count, character_count))
                        else:
                            self.error_manager.add_error("Unknown Name",line_count, character_count,character_count+1, "This name is not registered as part of a valid syntax")


                character_count += 1
            line_count +=1

class Parser:
    def __init__(self,tokens:list[Token]) -> None:
        self.tokens = tokens

        self.generated_code = bytearray()
    
    def add_ins(self,ins:int):
        lsb = ins & 0x00FF
        msb = (ins&0xFF00) >> 8

        self.generated_code.append(msb)
        self.generated_code.append(lsb)

    def parse(self)->None:
        for tkns in self.tokens:
            if tkns.name in INSTRUCTIONS.keys():
                self.add_ins(INSTRUCTIONS[tkns.name][2]())

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
parser = Parser(tokenizer.tokens)
parser.parse()
print(parser.generated_code)
