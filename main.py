# written by Meyan Adhikari
import sys
from constants import *

class ErrorManager:
    def __init__(self,source:list[str]):
        self.source = source
        self.errors = []
    def add_error(self,name:str,line_no:int,char_no:int,description:str):
        self.errors.append(f"""Error!
            {name} at {line_no}:{char_no}
            {description}
        """)


class Token:
    '''Represent Basic Unit'''
    def __init__(self,name:str,line_no:int,char_no:int):
        self.name = name
        self.line_no = line_no
        self.char_no = char_no
      
    def __repr__(self) -> str:
        return f"NAME:{self.name} "

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
            line = self.source_lines[line_count].upper() # making case insensitive
            character_count = 0
            # go through each character 
            while character_count < len(line):
                character = line[character_count]

                # single character check
                if character == NEW_LINE:
                    self.tokens.append(Token("NEW_LINE",line_count,character_count))

                elif character == COLON:
                    self.tokens.append(Token("COLON",line_count,character_count))

                elif character == COMMENT:
                    #skip the whole line 
                    character_count = len(line)
                    continue
                
                elif character == SPACE:
                    # skip the character
                    character_count += 1
                    continue
                elif character in SINGLE_CHAR_NAMES.keys():
                    self.tokens.append(Token(SINGLE_CHAR_NAMES[character],line_count, character_count))

                # multi character check
                elif character in VALID_CHARACTERS:
                    buffer = ""
                    while character in VALID_WORDS:
                        buffer += character
                    
                    if buffer in MULTI_CHAR_NAMES.keys():
                        self.tokens.append(Token(MULTI_CHAR_NAMES[buffer],line_count, character_count))
                    else:
                        self.error_manager.add_error("Unknown Name",line_count,character_count, "This name is not registered as part of a valid syntax")
                else:
                   self.error_manager.add_error("Unknown Name",line_count, character_count, "This name is not registered as part of a valid syntax")

                character_count += 1
            line_count +=1

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

# tokenizer
tokenizer = Tokenizer(error_manager)
tokenizer.tokenize()
print(tokenizer.tokens)

