#Contains code for the core game model of Halma
from math import ceil
from random import randint
import functools

# observer update function
def event(func):
    def modified(obj,*arg,**kwargs):
        func(obj,*arg,**kwargs)
        obj._Observer__fireCallback(func.__name__,*arg,**kwargs)
    functools.update_wrapper(modified,func)
    return modified

class Observer(object):
    def __init__(self):
        self.__observers = {}  # Method name -> observers

    def addObserver(self, methodName, observer):
        s = self.__observers.setdefault(methodName, set())
        s.add(observer)

    def __fireCallback(self, methodName, *arg, **kw):
        if methodName in self.__observers:
            for o in self.__observers[methodName]:
                o(*arg, **kw)


# object representation of a board piece
class Pawn(object):
    global player,pawn_id,node
    global x,y
    def __init__(self,player,pawn_id,node,y,x):
        self.player = player
        self.pawn_id = pawn_id
        self.y = y
        self.x = x
        self.node=node
    def getPlayer(self):
        return self.player
    def setPlayer(self,player):
        self.player = player
    def getNode(self):
        return self.node
    def setNode(self,node):
        self.node = node
    def getPawnId(self):
        return self.pawn_id
    def setPawnId(self,pawn_id):
        self.pawn_id = pawn_id;
    def setCoords(self,x,y):
        self.x = x
        self.y = y
    def getCoords(self):
        return (self.x,self.y)

#object representation of board tiles
class Node(Observer):
    global x_coord, y_coord, up_node, right_node, down_node, left_node, pawn
    def __init__(self, x_coord, y_coord, up_node=None, right_node=None, down_node=None, left_node=None, pawn=None):
        super().__init__()
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.up_node = up_node
        self.right_node = right_node
        self.down_node = down_node
        self.left_node = left_node
        self.pawn = pawn

    def getCoords(self):
        return (self.x_coord,self.y_coord)
    def setCoords(self,x,y):
        self.x_coord = x
        self.y_coord = y

    def setUpNode(self,node):
        self.up_node = node
    def setRightNode(self,node):
        self.right_node = node
    def setLeftNode(self,node):
        self.left_node = node
    def setDownNode(self,node):
        self.down_node = node

    def getUpNode(self):
        return self.up_node
    def getRightNode(self):
        return self.right_node
    def getLeftNode(self):
        return self.left_node
    def getDownNode(self):
        return self.down_node

    @event
    def setPawn(self,pawn):
        if pawn is not None:
            pawn.setCoords(self.x_coord,self.y_coord)
            pawn.setNode(self)
        self.pawn = pawn
    def getPawn(self):
        return self.pawn

class HalmaCore(object):
    global gui
    global board,turn,turn_count
    global dimensions,pieces,players

    def __init__(self,xy_dim=16,pieces=19,players=2):
        self.gui = None
        self.turn_count=0
        self.turn = randint(0,players-1)
        print("First move: player ", self.turn)
        self.dimensions = xy_dim
        self.pieces = pieces
        self.players = players
        self.board = [[0] * self.dimensions for i in range(self.dimensions)]
        #create all board tiles as Nodes and place in 2D list
        for y in range(0,xy_dim):
            for x in range(0,xy_dim):
                tile = Node(x,y)
                tile.addObserver( "setPawn",self.pawnMovedEvent )
                self.board[y][x]=tile
        #iterate through all tiles and link to neighbors
        for y in range(0,xy_dim):
            for x in range(0,xy_dim):
                tile = self.board[y][x]
                #set right-left node links
                try:
                    tile_right = self.board[y][x+1]
                    tile_right.setLeftNode(tile)
                    tile.setRightNode(tile_right)
                except Exception:
                    pass # out of bounds should just not execute
                #set up-down node links
                try:
                    tile_up = self.board[y-1][x]
                    tile_up.setDownNode(tile)
                    tile.setUpNode(tile_up)
                except Exception:
                    pass # out of bounds should just not execute

        #initialize and place player pawns
        start_row = 0
        start_col = 0
        longest_pawn_row = ceil( pieces * 0.25 )
        col_len = longest_pawn_row
        pawn_id = 0
        for player in range(0,players):
            for row in range(start_row,start_row+longest_pawn_row):
                for col in range(start_col,start_col+col_len):
                    node = self.board[row][col]
                    pawn = Pawn(player,pawn_id,node,row,col)
                    node.setPawn(pawn)
                    pawn_id = pawn_id+1
                if row > start_row and player == 0:
                    col_len = col_len - 1
                elif (row >= start_row) and (row <self.dimensions-2) and (player ==1):
                    col_len = col_len + 1
                    start_col = self.dimensions - col_len
            col_len = 2
            start_row = self.dimensions - longest_pawn_row
            start_col = self.dimensions - col_len

    def setGui(self,ui):
        self.gui = ui

    def pawnMovedEvent(self,pawn):
        if self.gui is not None:
            self.gui.pawnMovedEvent()

    def checkLocationXY(self,x_pos,y_pos):
        node = self.board[y_pos][x_pos]
        pawn = node.getPawn()
        if pawn is None:
            return None
        else:
            return (pawn.getPawnId(),pawn.getPlayer())

    def checkMoveValid(self,from_node,to_node):
        pawn = from_node.getPawn()
        if pawn is None:
            print('no pawn to be moved')
            return False
        player = pawn.getPlayer()
        print('player',player)
        if player != self.turn:
            print('not players turn')
            return False
        to_pawn = to_node.getPawn()
        if to_pawn is not None:
            print('to space occupied')
            return False

        x_dist = abs(from_node.getCoords()[0] - to_node.getCoords()[0])
        y_dist = abs(from_node.getCoords()[1] - to_node.getCoords()[1])
        if(x_dist<2 and y_dist<2):
            return True
        elif(x_dist<3 and y_dist<3):
            if self.existsPawnBetween(from_node,to_node):
                return True
            else:
                print('no adjoining piece to jump')
                return False
        else: return self.checkMoveValidRecursive(from_node,to_node)

    def existsPawnBetween(self,from_node,to_node):
        from_x = from_node.getCoords()[0]
        from_y = from_node.getCoords()[1]
        to_x = to_node.getCoords()[0]
        to_y = to_node.getCoords()[1]
        internode = None
        if to_x > from_x and to_y > from_y:
            internode = self.board[from_y+1][from_x+1]
        elif to_x > from_x and to_y == from_y:
            internode = self.board[from_y][from_x+1]
        elif to_x > from_x and to_y < from_y:
            internode = self.board[from_y-1][from_x+1]
        elif to_x == from_x and to_y < from_y:
            internode = self.board[from_y-1][from_x]
        elif to_x < from_x and to_y < from_y:
            internode = self.board[from_y-1][from_x-1]
        elif to_x < from_x and to_y == from_y:
            internode = self.board[from_y][from_x-1]
        elif to_x < from_x and to_y > from_y:
            internode = self.board[from_y+1][from_x-1]
        elif to_x == from_x and to_y > from_y:
            internode = self.board[from_y+1][from_x]
        pawn = internode.getPawn()
        if pawn is None:
            return False
        return True

    def checkMoveValidRecursive(self,from_node,to_node):
        return False

    def moveXY(self,x_from,y_from,x_to,y_to):
        from_node = self.board[y_from][x_from]
        to_node = self.board[y_to][x_to]
        return self.move(from_node, to_node)

    def move(self,from_node,to_node):
        if( self.checkMoveValid(from_node,to_node) ):
            pawn = from_node.getPawn()
            to_node.setPawn(pawn)
            from_node.setPawn(None)
            self.updateTurn()
            return True
        else:
            return False

    def getTurn(self):
        return self.turn
    def getTurnCount(self):
        return self.turn_count

    def updateTurn(self):
        self.turn = self.turn +1
        if self.turn >= self.players:
            self.turn = 0
        self.turn_count = self.turn_count +1

    def printBoard(self):
        print()
        for y in range(0, self.dimensions):
            for x in range(0, self.dimensions):
                tile_node = self.board[y][x]
                if tile_node.getPawn() is None:
                    print(' '+u"\u25A0", end="")
                else:
                    tile_pawn = tile_node.getPawn()
                    print(' '+str(tile_pawn.getPlayer()), end="")
            print()
        print()

def main():
    board = HalmaCore()
    board.printBoard()
    board.moveXY(3,0,5,0,1)
    board.printBoard()

if __name__ == "__main__":
    main()