import pygame

######################
# Some constants
######################
WIDTH = 800
HEIGHT = 500
TITLE = "Krian - Chip8 Sprite Kreator"


########################
# Main App
########################

class App:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        
        #screen attributes
        pygame.display.set_caption(TITLE)
        self.running = True

    
    def mainloop(self) -> None:
        while self.running:
            for evs in pygame.event.get():
                if evs.type == pygame.QUIT:
                    self.running = False


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

