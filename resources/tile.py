from resources.text import Text
import pygame, math
class Tile:
    def __init__ (self, pos, power):
        self.position = pos
        self.destination = None
        self.power = power

        self.sizePercent = 0.0

        self.merged = False
        self.slid = False
        self.pastIndexA = [-1, -1]
        self.pastIndexB = [-1, -1]
        self.isNew = True

        self.t = Text()
        self.BGcolor = (100, 50, 50)
        self.border = 0
        self.colors = [
            (0, 0, 0), # 1
            (150, 150, 150), # 2
            (200, 180, 180), # 4
            (200, 150, 100), # 8
            (200, 100, 100), # 16
            (200, 100, 100), # 32
            (230, 150, 150), # 64
            (230, 230, 150), # 128
            (230, 230, 180), # 256
            (240, 240, 210), # 512
            (200, 200, 90), # 1024
            (200, 200, 0), # 2048

        ]
    def run (self):
        if self.destination is not None:
            dx = (self.destination[0] - self.position[0])
            dy = (self.destination[1] - self.position[1])
            self.position[0] += dx * 0.3
            self.position[1] += dy * 0.3
            if abs(dx) < 5 and abs(dy) < 5:
                self.position = self.destination
        self.sizePercent += (1.0-self.sizePercent)*0.2
        if self.sizePercent>0.98 and self.sizePercent<1.02:
            self.sizePercent = 1.0
    def setSizePercent (self, n):
        self.sizePercent = n
    def getNumber (self):
        return int(math.pow(2, self.power))
    def drawToSurface (self, surface, s):
        # pygame.draw.rect(surface, self.BGcolor, (self.position[0], self.position[1], s, s), 0)
        self.border = s*(1.0-self.sizePercent)/2
        col = self.colors[self.power] if self.power < len(self.colors) else (255, 0, 0)
        pygame.draw.rect(surface, col, (self.position[0]+self.border, self.position[1]+self.border, s-self.border*2, s-self.border*2), 0)
        self.t.drawToSurface(
            surface,
            (self.position[0]+(s-self.border*2)/2+self.border, self.position[1]+(s-self.border*2)/2+self.border),
            self.getNumber(),
            s*self.sizePercent*0.7 / math.sqrt(math.floor(math.log(self.getNumber(), 10))+1),
            (255, 255, 255)
        )
