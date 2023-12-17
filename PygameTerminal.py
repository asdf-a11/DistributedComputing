import threading

FONT_SIZE = 14
FONT_OFFSET = 3
BACKGROUND_COLOUR = (0,0,0)
TEXT_COLOUR = (255,255,255)

class Cam():
    def __init__(self):
        self.yPos = 0
    def UpdatePos(self):
        pass

class Line():
    def __init__(self, content, colour, bgColour):
        self.content = content
        self.colour = colour
        self.bg = bgColour
    def Draw(self,window, font, yPos, cam):
        a = font.render(self.content, True, self.colour, self.bg)
        window.blit(a, (2, yPos - cam.yPos))
        return yPos + a.get_height() + FONT_OFFSET

lineList = []

def UpdateTerminal():
    import pygame 
    import os, signal

    screenx,screeny = 400, 300


    pygame.init()
    pygame.display.set_caption("Pygame Terminal")
    #window = pygame.display.set_mode()
    #MAX_SCREENX, MAX_SCREENY = window.get_size()
    font = pygame.font.SysFont(pygame.font.get_fonts()[0], FONT_SIZE)#pygame.font.Font(
    clock = pygame.time.Clock()

    #screenx = min(MAX_SCREENX, screenx)
    #screeny = min(MAX_SCREENY, screeny)

    pygame.display.quit()
    window = pygame.display.set_mode((screenx, screeny))
        
    cam = Cam()
    
    run = True
    while run:         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                os.kill(os.getpid(), signal.SIGTERM)
        pygame.event.pump()    
        clock.tick(10)
        pygame.draw.rect(window,(0,0,0),(0,0,screenx,screeny))
        cam.UpdatePos()
        yPos = 0
        for ldx,l in enumerate(lineList):
            yPos = l.Draw(window, font, yPos, cam)
        if yPos-cam.yPos > screeny - FONT_SIZE * 2:
            cam.yPos += FONT_SIZE * 2
        pygame.display.update()


updateThread = threading.Thread(target=UpdateTerminal, args=())
updateThread.start()


def Print(content, colour = TEXT_COLOUR, bgColour = BACKGROUND_COLOUR):
    l = Line(content, colour, bgColour)
    lineList.append(l)
    print(content)
