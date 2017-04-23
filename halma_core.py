#Contains code for the core game model of Halma
from math import ceil
from random import randint

#object representation of a board piece
class Pawn(object):
    global player,pawn_id,node
    global x,y
    def __init__(self,player,pawn_id,node,y,x):
        self.player = player
        self.pawn_id = pawn_id
        self.y = y
        self.x = x
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
class Node(object):
    global x_coord, y_coord, up_node, right_node, down_node, left_node, pawn
    def __init__(self,x_coord,y_coord,up_node=None,right_node=None,down_node=None,left_node=None,pawn=None):
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

    def setPawn(self,pawn):
        self.pawn = pawn
    def getPawn(self):
        return self.pawn

class HalmaCore(object):
    global board,turn,turn_count
    global dimensions,pieces,players

    def __init__(self,xy_dim=16,pieces=19,players=2):
        self.turn_count=0
        self.turn = randint(0,players)
        self.dimensions = xy_dim
        self.pieces = pieces
        self.players = players
        self.board = [[0] * self.dimensions for i in range(self.dimensions)]
        #create all board tiles as Nodes and place in 2D list
        for y in range(0,xy_dim):
            for x in range(0,xy_dim):
                tile = Node(x,y)
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

    def move(self,x_from,y_from,x_to,y_to):
        from_node = self.board[y_from][x_from]
        pawn = from_node.getPawn()
        if pawn is None:
            print('no pawn to be moved')
            return False
        player = pawn.getPlayer()
        if player != self.turn:
            print('not players turn')
            return False

        to_node = self.board[y_to][x_to]
        to_pawn = to_node.getPawn()
        if to_pawn is not None:
            print('to space occupied')
            return False

        to_node.setPawn(pawn)
        from_node.setPawn(None)

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
    board.move(4,0,5,0)
    board.printBoard()

if __name__ == "__main__":
    main()