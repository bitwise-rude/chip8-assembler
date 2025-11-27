# written by Meyan Adhikari
import sys
import constants

class Tokenizer:
    def __init__(self,lines:list[str]) -> None:
        self.source_lines = lines 

    def tokenize(self) -> None:
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
