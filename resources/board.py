from resources.tile import Tile
import pygame, random, math
from resources.directions import DIRECTION
class Board:
    def __init__ (self, dim, dsize):
        self.dim = dim
        self.dsize = dsize # draw size
        self.tsize = dsize/dim # tile size
        self.tborder = self.tsize*0.05
        self.randRange = [1, 1]
        self.board = [[None for j in range(0, dim)] for i in range(0, dim)]
        self.addRandomTile()
        self.Lost = False
        self.knowledgeOfDeath = False
        self.boardFilled = False
        self.score = 0
        self.lastScore = 0
        self.undone = True
        self.mergedOrSlid = False
        self.background = pygame.Surface((dsize, dsize))
        self.background.fill((150, 150, 150))
        for i in range(self.dim):
            for j in range(self.dim):
                pygame.draw.rect(self.background, (170, 170, 170), (j*self.tsize+self.tborder, i*self.tsize+self.tborder, self.tsize-self.tborder*2, self.tsize-self.tborder*2), 0)
    def printBoard (self):
        for i in self.board:
            s = "|"
            for t in i:
                s += str(t.getNumber() if t is not None else " ")
                s += " "
            s += "|"
            print(s)
    def reset (self):
        self.board = [[None for j in range(0, self.dim)] for i in range(0, self.dim)]
        self.addRandomTile()
        self.Lost = False
        self.score = 0
        self.lastScore = 0
    def randbool (self):
        return bool(random.randint(0, 1))
    def constrain (self, v, x, y):
        return math.min(math.max(v, x), y)
    def draw (self):
        surf = pygame.Surface((self.dsize, self.dsize))
        surf.blit(self.background, (0, 0))
        iy = -1
        for i in self.board:
            iy+=1
            ix = -1
            for t in i:
                ix+=1
                if t is None:
                    continue
                t.run()
                t.drawToSurface(surf, self.tsize - self.tborder*0.9)
        return surf
    def getTile(self, p):
        return self.board[p[0]][p[1]]
    def switchTiles (self, t1, t2):
        temp = self.getTile(t1)
        self.board[t1[0]][t1[1]] = self.getTile(t2)
        self.board[t2[0]][t2[1]] = temp
    def setDestinations (self):
        iy = -1
        for i in self.board:
            iy += 1
            ix = -1
            for t in i:
                ix += 1
                if t is None:
                    continue
                t.destination = [ix*self.tsize, iy*self.tsize]
        #         print("[%d, %d] -> %s"%(iy, ix, t.destination))
        # print("tile size: %s"%self.tsize)
    def resetMerges (self):
        for i in self.board:
            for j in i:
                if j is not None:
                    j.merged = False
    def resetSlides (self):
        for i in self.board:
            for j in i:
                if j is not None:
                    j.slid = False
    def unNewAll (self):
        for i in self.board:
            for j in i:
                if j is not None:
                    j.isNew = False
    def setPastIndicies (self):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j] is not None:
                    self.board[i][j].pastIndexA = [i, j]
    def lost (self):
        l = True
        for i in self.board:
            for j in i:
                if j is None: # there is an empty square
                    l = False
        self.boardFilled = l
        cantwin = l and not self.hasPossibleMerge()
        if cantwin: self.Lost = True
        self.knowledgeOfDeath = False
        return cantwin # there is not an empty square
    def possibleMergeDirection (self, direction):
        dx = direction['x']
        dy = direction['y']
        ri = [max(0, -dy), min(self.dim - dy, self.dim) - 1]
        rj = [max(0, -dx), min(self.dim - dx, self.dim) - 1]
        RI = range(ri[0], ri[1] + 1)
        RJ = range(rj[0], rj[1] + 1)
        for i in RI:
            for j in RJ:
                t = self.board[i][j]
                tn = self.board[i + dy][j + dx]
                if t is None or tn is None:
                    continue
                if t.power == tn.power:
                    return True
        return False
    def hasPossibleMerge (self):
        return self.possibleMergeDirection(DIRECTION['UP']) \
               or self.possibleMergeDirection(DIRECTION['DOWN']) \
               or self.possibleMergeDirection(DIRECTION['LEFT']) \
               or self.possibleMergeDirection(DIRECTION['RIGHT'])

    def addRandomTile (self):
        while True:
            ri = random.randint(0, self.dim-1)
            rj = random.randint(0, self.dim-1)
            if self.getTile([ri, rj]) is None:
                x = rj*self.tsize
                y = ri*self.tsize
                self.board[ri][rj] = Tile([x, y], random.randint(self.randRange[0], self.randRange[1]))
                break

    def unmerge (self):
        newBoard = [[None for j in range(0, self.dim)] for i in range(0, self.dim)]
        for i in range(self.dim):
            for j in range(self.dim):
                t = self.board[i][j]
                if t is None or t.isNew:
                    continue
                nindex = t.pastIndexA
                po = t.power
                newBoard[nindex[0]][nindex[1]] = self.getTile([i, j])
                newPos = self.getTile([i, j]).position
                nt = Tile([newPos[0], newPos[1]], self.getTile([i, j]).power - 1)
                nt.sizePercent = 1.0
                if t.merged:
                    newBoard[nindex[0]][nindex[1]].power = po - 1
                    bindex = t.pastIndexB
                    newBoard[bindex[0]][bindex[1]] = nt
        self.board = newBoard
        self.setDestinations()
        self.undone = True
        self.score = self.lastScore

    def merge (self, direction):
        dx = direction['x']
        dy = direction['y']
        ri = [max(0, -dy), min(self.dim-dy, self.dim)-1]
        rj = [max(0, -dx), min(self.dim-dx, self.dim)-1]
        RI = range(ri[0], ri[1]+1)
        RJ = range(rj[0], rj[1]+1)
        done = False
        self.resetMerges()
        while not done:
            done = True
            for ii in RI:
                i = ii
                if dy>0:
                    i = ri[1]-(ii-ri[0])
                for jj in RJ:
                    j = jj
                    if dx>0:
                        j = rj[1]-(jj-rj[0])
                    t = self.board[i][j]
                    tn = self.board[i+dy][j+dx]
                    if t is None or tn is None:
                        continue
                    if t.merged or tn.merged:
                        continue
                    if t.power == tn.power:
                        # todo:add past indicies, a and b
                        self.board[i+dy][j+dx].position = t.position
                        self.board[i][j] = None
                        tn.power += 1
                        tn.setSizePercent(1.4)
                        tn.pastIndexA = tn.pastIndexA # oh well
                        tn.pastIndexB = t.pastIndexA
                        tn.slid = True
                        tn.merged = True
                        self.score += tn.getNumber()
                        done = False
                        self.mergedOrSlid = True
    def slide (self, direction):
        switched = True
        dx = direction['x']
        dy = direction['y']
        ri = [max(0, -dy), min(self.dim-dy, self.dim)]
        rj = [max(0, -dx), min(self.dim-dx, self.dim)]
        while switched:
            switched = False
            for i in range(ri[0], ri[1]):
                for j in range(rj[0], rj[1]):
                    t = self.board[i][j]
                    tn = self.board[i+dy][j+dx]
                    if tn is None and t is not None:
                        self.board[i+dy][j+dx] = self.board[i][j]
                        if not self.board[i+dy][j+dx].slid:
                            self.board[i + dy][j + dx].slid = True
                            self.board[i+dy][j+dx].pastIndexA = [i, j]
                        self.board[i][j] = None
                        switched = True
                        self.mergedOrSlid = True

    def turn (self, direction):
        self.lastScore = self.score
        self.undone = False
        self.mergedOrSlid = False
        self.setPastIndicies() # set all of the past indicies at the current location
        self.resetSlides() # make all the tiles not have the condition 'slid'
        self.slide(direction) # slide all the tiles in the direction
        self.merge(direction) # merge all the tiles in the direction
        # self.resetSlides() # reset the condition 'slid' again
        self.slide(direction) # slide all the tiles in the direction
        self.lost() # check if lost
        self.unNewAll() # make all the tiles on the board at this point 'not new'
        self.setDestinations() # set physical locations
        if self.Lost or self.boardFilled or not self.mergedOrSlid:
            return
        self.addRandomTile() # add a random tile if the board isn't filled and you haven't lost
