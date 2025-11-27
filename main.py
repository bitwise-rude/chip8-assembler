# written by Meyan Adhikari
import sys
from constants import *

class Token:
    '''Represent Basic Unit'''
    def __init__(self,name,line_no,char_no):
        pass

class Tokenizer:
    def __init__(self,lines:list[str]) -> None:
        self.source_lines = lines 
        self.tokens = []

    def tokenize(self) -> None:
        
        # go through each line
        for i in range(len(self.source_lines)):
            line = self.source_lines[i].upper() # making case insensitive

            # go through each character 
            for j in range(len(line)):
                character = line[j]

                # single character check
                if character == NEW_LINE:
                    self.tokens.append(Token(NEW_LINE,i,j);

                elif character == COLON:
                    self.tokens.append(Token(COLON,i,j));

                elif character == COMMENT:
                    # skip the whole line 
                    continue
                
                # multi character check
                if character in VALID_CHARACTERS:
                    pass



def show_err_and_quit(err:str):
    print("\tch8asm:\nError:\t",err)
    quit()

def read_file_contents(file_name : str) -> list[str]:
    '''Reads and returns the file contents'''
    try:
        file_handler = open(file_name,'r')
        return file_handler.readlines();
    except FileNotFoundError:
        show_err_and_quit("The source file wasn't found")
    #handle other erros as well

if len(sys.argv) < 2: 
    show_err_and_quit("Source File Needed")

# read the file 
source_lines = read_file_contents(sys.argv[1])

# tokenizer
tokenizer = Tokenizer(source_lines)
