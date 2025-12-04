import pygame

######################
# Some constants
######################
WIDTH = 800
HEIGHT = 500
TITLE = "Krian - Chip8 Sprite Kreator"

# Colors
FILL_COLOR = (0,0,0)
SPRITE_FILL_COLOR = (255,255,255)


########################
# Classes and Tools
########################

class Spriter:
    '''Main Sprite creator class'''
    def __init__(self,screen:pygame.Surface,x:int,y:int) -> None:
        self.screen = screen

        # some handy intialization
        self.row_count = 8 
        self.col_count = 5

        self.x = x # start of the top-left cell
        self.y = y

        self.size = 20 # default

        # For a standard CHIP8, 8x15 is the max.
        # while the character sprites are 8x5

        self.display_matrix = [[0]*self.row_count]*self.col_count
    
    def update(self) -> None:
        for i in range(len(self.display_matrix)):
            for j in range(len(self.display_matrix[i])):
                pygame.draw.rect(self.screen,SPRITE_FILL_COLOR,
                                 (self.x+i*self.size,self.y+j*self.size, self.size, self.size),
                                 width=1
                                 )



class App:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.spriter = Spriter(self.screen,10,100)
        
        #screen attributes
        pygame.display.set_caption(TITLE)
        self.running = True

    
    def mainloop(self) -> None:
        self.screen.fill(FILL_COLOR)

        while self.running:
            for evs in pygame.event.get():
                if evs.type == pygame.QUIT:
                    self.running = False

            self.spriter.update()

            pygame.display.update()
        


def init() -> None:
    '''Initializes everything'''
    pygame.init()
    pygame.display.init()

def deinit() -> None:
    '''Deinitialize everything'''
    pygame.quit()


if __name__ == "__main__":
    init()
    app = App()
    app.mainloop()
    deinit()

