
from pyray import *
from dataMatrix import *
from random import *

class Character:

    def __init__(self, char, font, x, y, color, size):
        self.font = font
        self.char = ord(char)
        self.x = x
        self.y = y
        self.position = Vector2(self.x, self.y)
        self.opacity = color[3] if color.__len__() == 4 else 255
        self.color = color if color.__len__() == 4 else (color[0], color[1], color[2], self.opacity)
        self.size = size
        self.letter = char
    
    def changeLetter(self, char):
        self.char = ord(char)
        self.letter = char
    
    def changeColor(self, color):
        self.color = color if color.__len__() == 4 else (color[0], color[1], color[2], self.opacity)
    
    def changeOpacity(self, opacity):
        self.opacity = opacity
        self.color = (self.color[0], self.color[1], self.color[2], self.opacity)
    
    def resize(self, size):
        self.size = size

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
        self.shareColumns: list = [(column * self.charSize) for column in range(self.windowColumns)]

    def changeLength(self):
        return randint(self.minLength, self.maxLength)

    def changeVelocity(self):
        getVelocities: list = [int(self.charSize / i) for i in range(1, int(self.charSize / 2)) if self.charSize % i == 0]
        return choice(getVelocities)

    def randomColumn(self):
        getColumn: int = self.shareColumns.pop(randrange(self.shareColumns.__len__()))
        self.shadowColumns.append(getColumn)
        return getColumn

    def randomChar(self):
        return choice(SEQUENCE)

    def matrix(self, thisNode):

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
        
        thisLength = thisNode[trail].__len__()
        if (thisLength > thisNode[trailLength]):
            del thisNode[trail][0]
        
        choiceIndex = randrange(thisLength)
        for i, thisTrail in enumerate(thisNode[trail]):
            opacity = int( min( ( 255 * ( max( i / (thisLength / 2), 0 ) ) ), 255 ) )
            if (i > 0 and i == choiceIndex):
                thisTrail.changeLetter(self.randomChar())
            thisTrail.changeOpacity(opacity)
            draw_text_codepoint(thisTrail.font,
                                thisTrail.char,
                                thisTrail.position,
                                thisTrail.size, 
                                thisTrail.color)
        
        thisNode[letter].changeLetter(char)
        thisNode[letter].position.x = thisNode[x]; thisNode[letter].position.y = thisNode[y]
        draw_text_codepoint(thisNode[letter].font,
                            thisNode[letter].char,
                            thisNode[letter].position,
                            thisNode[letter].size,
                            thisNode[letter].color)

        thisNode[y] += thisNode[velocity]

    def main(self):

        init_window(self.width, self.height, "Matrix")
        # set_window_icon("path/to/icon.png")
        self.katakana = load_font(katakanaFont)
        
        if (self.fullscreen):
            # toggle_fullscreen()
            toggle_borderless_windowed()
            self.width = get_screen_width()
            self.height = get_screen_height()
            set_window_size(self.width, self.height)
            self.windowColumns = self.width // self.charSize
            self.shareArray()
        
        self.maxNodes = self.maxNodes if self.maxNodes <= self.windowColumns * .9 else int(self.windowColumns * .9)

        while (not window_should_close()):
            set_target_fps(self.fps)

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

            clear_background(black)
            begin_drawing()

            for thisNode in self.nodes:
                self.matrix(thisNode)
            
            end_drawing()

if __name__ == "__main__":

    matrix = Matrix(fullscreen=True)
    matrix.main()