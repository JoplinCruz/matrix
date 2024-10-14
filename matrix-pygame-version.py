
from pygame import *
from dataMatrix import *
from random import *

class Character(sprite.Sprite):

    def __init__(self, char, font, x, y, color, size):
        sprite.Sprite.__init__(self)
        self.char = char
        self.font = font
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.letter = self.font.render(self.char, 1, self.color)
        self.makeBox()
    
    def changeLetter(self, char):
        self.char = char
        self.letter = self.font.render(self.char, 1, self.color)
        self.makeBox()
    
    def changeColor(self, color):
        self.color = color
        self.letter = self.font.render(self.char, 1, self.color)
        self.makeBox()
    
    def opacity(self, opacity):
        self.letter.set_alpha(opacity)
    
    def resize(self, size):
        self.letter = transform.scale_by(self.letter, self.size)
        self.makeBox()
    
    def makeBox(self):
        self.box = self.letter.get_rect()
        self.box.topleft = (self.x, self.y)
    
    def screenBlit(self, screen):
        screen.blit(self.letter, self.box.topleft)

class Matrix:
    
    def __init__(self, width=800, height=600, maxnodes=64, maxlength=32, minlength=8, fontscale=1, fullscreen=False):
        self.width = width
        self.height = height
        self.fps = 30
        self.fullscreen = fullscreen

        self.maxLength = maxlength
        self.minLength = minlength

        self.fontScale = fontscale
        self.charSize = self.fontScale * 16
        self.windowColumns = self.width // self.charSize
        self.maxNodes = maxnodes

        self.x: int
        self.y: int = -self.charSize

        self.velocity: int
        self.trailLength: int
        self.nodes: list = []
        
        self.shareArray()

    def shareArray(self):
        self.shadowColumns: list = []
        self.shareColumns: list = [(column * self.charSize)
                                   for column in range(self.windowColumns)]

    def changeLength(self):
        return randint(self.minLength, self.maxLength)

    def changeVelocity(self):
        getVelocities: list = [int(self.charSize / i)
                               for i in range(1, int(self.charSize / 2))
                               if self.charSize % i == 0]
        return choice(getVelocities)

    def randomColumn(self):
        getColumn: int = self.shareColumns.pop(randrange(self.shareColumns.__len__()))
        self.shadowColumns.append(getColumn)
        return getColumn

    def randomChar(self):
        return choice(SEQUENCE)

    def matrix(self, screen, thisNode):

        char: str = self.randomChar()
        
        if (thisNode[y] > self.height + self.charSize):
            self.shareColumns.append(thisNode[x])
            self.shadowColumns.remove(thisNode[x])
            thisNode[x] = self.randomColumn()
            thisNode[y] = -self.charSize
            thisNode[velocity] = self.changeVelocity()
        
        if (thisNode[y] / self.charSize == int(thisNode[y] / self.charSize)):
            thisChar = Character(char,
                                 self.katakana,
                                 thisNode[x],
                                 thisNode[y],
                                 darkgreen,
                                 self.charSize)
            thisNode[trail].append(thisChar)

        if (thisNode[trail].__len__() > thisNode[trailLength]):
            del thisNode[trail][0]
        
        for i, thisTrail in enumerate(thisNode[trail]):
            opacity = int(255 * (max(i / (thisNode[trail].__len__() / 2), 0)))
            choiceIndex = randint(0, thisNode[trail].__len__()-1)
            if (i > 0 and i == choiceIndex):
                thisTrail.changeLetter(self.randomChar())
            thisTrail.opacity(opacity)
            # thisTrail.screenBlit(screen)
            screen.blit(thisTrail.letter, thisTrail.box.topleft)            # screen.blit
        
        thisNode[y] += thisNode[velocity]

        thisNode[letter].changeLetter(char)
        thisNode[letter].x = thisNode[x]; thisNode[letter].y = thisNode[y]
        # thisNode[letter].screenBlit(screen)
        screen.blit(thisNode[letter].letter, thisNode[letter].box.topleft)      # screen.blit this too.

    def main(self):

        init()
        font.init()
        self.katakana = font.Font(katakanaFont, self.charSize)
        clock = time.Clock()
        display.set_caption("Matrix")
        
        if (self.fullscreen):
            displayInfo = display.Info()
            self.width, self.height = displayInfo.current_w, displayInfo.current_h
            self.windowColumns = self.width // self.charSize
            self.shareArray()
            screen = display.set_mode((self.width, self.height), HWSURFACE|DOUBLEBUF|SCALED|FULLSCREEN)     # pygame.HWSURFACE|pygame.DOUBLEBUF|
        elif (not self.fullscreen):
            screen = display.set_mode((self.width, self.height), HWSURFACE|DOUBLEBUF)                       # pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE
        
        self.maxNodes = self.maxNodes if self.maxNodes <= self.windowColumns * .9 else int(self.windowColumns * .9)

        running = True
        
        while running:

            for console in event.get():
                if (console.type == QUIT):
                    running = False
                if (console.type == KEYDOWN):
                    if (console.key == K_ESCAPE):
                        running = False

            if (self.nodes.__len__() <= self.maxNodes):
                self.x = self.randomColumn()
                self.velocity = self.changeVelocity()
                self.trailLength = self.changeLength()
                
                self.nodes.append(
                    {
                        "letter": Character(self.randomChar(),
                                            self.katakana,
                                            self.x,
                                            self.y,
                                            lightgreen,
                                            self.charSize),
                        "x": self.x,
                        "y": self.y,
                        "trail": [],
                        "trailLength": self.trailLength,
                        "velocity": self.velocity
                    }
                )

            screen.fill(black)
            
            for thisNode in self.nodes:
                self.matrix(screen, thisNode)
            
            display.flip()
            # display.update()
            clock.tick(self.fps)
            
        quit()

if __name__ == "__main__":

    matrix = Matrix(fullscreen=True)
    matrix.main()