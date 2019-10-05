import pygame, sys
from resources.board import Board
from resources.tile import Tile
from resources.text import Text
from resources.button import Button
from resources.directions import DIRECTION
from pygame.locals import *
pygame.init()

# constants

WIDTH = 500
HEIGHT = 500
TWIDTH = WIDTH*3/4
THEIGHT = HEIGHT*3/4
TBORDER = 3
TX = (WIDTH-TWIDTH)/2
TY = (HEIGHT-THEIGHT)/2
CLOCK = pygame.time.Clock()
FPS = 60

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 by Veggiebob")
TILESURF = pygame.Surface((TWIDTH, THEIGHT))

mainBoard = Board(4, TWIDTH)
T = Text()

DISPLAYSURF.blit(mainBoard.draw(), (TX, TY))
def getDirection (k):
    if k==K_DOWN:
        return DIRECTION['DOWN']
    elif k==K_UP:
        return DIRECTION['UP']
    elif k==K_RIGHT:
        return DIRECTION['RIGHT']
    elif k==K_LEFT:
        return DIRECTION['LEFT']
    return DIRECTION['UP']

def alert (message):
    global frozen
    global warnButton
    global mousedown, click
    frozen = True
    click = False
    mousedown = False
    warnButton.text = message
def unfreeze ():
    global frozen
    global mousedown
    global mainBoard
    mousedown = False
    frozen = False
    if mainBoard.Lost:
        mainBoard.knowledgeOfDeath = True
        # mainBoard.reset()

def printTest ():
    print("print test")

def pause ():
    alert("paused")

def reset ():
    alert("reset")
    mainBoard.reset()

def undo ():
    if mainBoard.undone:
        alert("Can only undo once")
    else:
        mainBoard.unmerge()

def youdied ():
    alert("you died")

def help ():
    alert('arrow keys move')



click = False
button = -1
mousedown = False
frozen = False
warnButton = Button((WIDTH/4, HEIGHT/4, WIDTH/2, HEIGHT/2), unfreeze, "no error?")


buttonWidth = (WIDTH-TWIDTH)/2
fullb = buttonWidth
buttons = [
    # [ text, function, height ]
    # ["test", printTest, fullb],
    # ["pause", pause, fullb],
    ["reset", reset, fullb],
    ["undo", undo, fullb],
    ['help', help, fullb]
]
buttonobj = []
buttonMargin = 2
buttonY = fullb + 0
for b in buttons:
    buttonobj.append(Button((buttonMargin, buttonY, buttonWidth-buttonMargin*2, b[2]), b[1], b[0]))
    buttonY += b[2] + buttonMargin

DISPLAYSURF.fill((230, 230, 230))
T.drawToSurface(DISPLAYSURF, (WIDTH / 2, (HEIGHT - THEIGHT) / 4), "2048", 30, (200, 200, 0))
while True:
    k = -1
    mrel = [0, 0]
    button = -1
    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            k = event.key
        elif event.type == MOUSEMOTION:
            mrel = event.rel
            button = 0 if event.buttons[0]>0 else (1 if event.buttons[1]>0 else (2 if event.buttons[2]>0 else -1))
            mouse = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            button = event.button-1
            mouse = event.pos
            click = True
            mousedown = True
        elif event.type == MOUSEBUTTONUP:
            mousedown = False

    if frozen:
        warnButton.run(DISPLAYSURF, mouse, mousedown, click)
    else:
        TILESURF.blit(mainBoard.draw(), (0, 0))
        DISPLAYSURF.blit(TILESURF, (TX, TY))
        for b in buttonobj:
            b.run(DISPLAYSURF, mouse, mousedown, click)
        if not k==-1:
            mainBoard.turn(getDirection(k))
        pygame.draw.rect(DISPLAYSURF, (230, 230, 230), (0, HEIGHT-(HEIGHT-THEIGHT)/2, WIDTH, (HEIGHT-THEIGHT)/2), 0)
        T.drawToSurface(DISPLAYSURF, (WIDTH/2, HEIGHT-(HEIGHT-THEIGHT)/4), str(mainBoard.score), 30, (50, 50, 50))
        if mainBoard.Lost and not mainBoard.knowledgeOfDeath:
            youdied()
    CLOCK.tick(FPS)
    pygame.display.update()
