import pygame
class Text:
    def __init__ (self):
        self.fontPath = "assets/number_font.TTF"
        self.font = pygame.font.Font(self.fontPath, 20)
        self.fonts = {
            20:self.font
        }
    def draw (self, txt="sample text", size=20, color=(0,0,0)):
        size = int(size)
        try:
            self.fonts[size]
        except:
            self.fonts[size] = pygame.font.Font(self.fontPath, size)

        fo = self.fonts[size]
        surf = fo.render(str(txt), True, color)
        return surf
    def drawToSurface (self, surface, position, txt="sample text", size=20, color=(0,0,0)):
        surf = self.draw(txt, size, color)
        surface.blit(surf, (int(position[0]-surf.get_width()/2), int(position[1]-surf.get_height()/2)))