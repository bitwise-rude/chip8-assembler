import pygame

######################
# Some constants
######################
WIDTH = 800
HEIGHT = 500
TITLE = "Krian - Chip8 Sprite Kreator"

# Colors
FILL_COLOR = (0,0,0)
SPRITE_FILL_COLOR_0 = (255,255,255)
SPRITE_FILL_COLOR_1 = (255,0,0)



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

        self.display_matrix = [[0 for _ in range(self.row_count)] for _ in range(self.col_count)]
    
    def update(self,is_holding_left : bool) -> None:

        for j in range(len(self.display_matrix)):
            for i in range(len(self.display_matrix[j])):
            
                place_x = self.x+i*self.size
                place_y = self.y+j*self.size

                if is_holding_left:
                    x,y = pygame.mouse.get_pos()
                    if (x>=place_x and x<=place_x+self.size) and (y>=place_y and y<=place_y+self.size):
                        self.display_matrix[j][i] = 1

                pygame.draw.rect(self.screen,
                                 SPRITE_FILL_COLOR_1 if self.display_matrix[j][i]==1 else SPRITE_FILL_COLOR_0,
                                 (place_x,place_y, self.size, self.size),
                                 width=0)
    

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

