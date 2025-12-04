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
    def __init__(self,screen:pygame.Surface,y_level:int) -> None:
        self.screen = screen

        # some handy intialization
        self.row_count = 8 
        self.col_count = 5

        self.size = 50# default

        self.x = (WIDTH - (self.size * self.row_count))//2 # start of the top-left cell making in middle
        self.y = y_level


        # For a standard CHIP8, 8x15 is the max.
        # while the character sprites are 8x5

        self.display_matrix = [[0]*self.row_count]*self.col_count
    
    def update(self,is_holding_left : bool) -> None:
        if is_holding_left:
            _pos = pygame.mouse.get_pos()
             
             # check if lies inside any cell

        for j in range(len(self.display_matrix)):
            for i in range(len(self.display_matrix[j])):
                pygame.draw.rect(self.screen,SPRITE_FILL_COLOR,
                                 (self.x+i*self.size,self.y+j*self.size, self.size, self.size),
                                 width=1)
    

class App:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.spriter = Spriter(self.screen,50)
        
        #screen attributes
        pygame.display.set_caption(TITLE)
        self.running = True

    
    def mainloop(self) -> None:
        self.screen.fill(FILL_COLOR)

        is_holding_left = False

        while self.running:
            for evs in pygame.event.get():
                if evs.type == pygame.QUIT:
                    self.running = False
                
                elif evs.type == pygame.MOUSEBUTTONDOWN:
                    if evs.button == 1: # left button
                        is_holding_left = True
                
                elif evs.type == pygame.MOUSEBUTTONUP:
                    if evs.button == 1:
                        is_holding_left = False


            self.spriter.update(is_holding_left)

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

