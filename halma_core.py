#Contains code for the core game model of Halma
from math import ceil
from random import randint
import functools



class HalmaCore():
    global gui
    global board,turn,turn_count
    global dimensions,pieces,players
    global pawns

    def __init__(self, xy_dim=8, pieces=10, players=2, start_shape='triangle'):
        super().__init__()
        self.xy_dim = xy_dim


        self.greenstart = set([(0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (2,0), (2,1), (3,0)])
        self.redstart = set([(7,4), (7,5), (7,6), (7,7), (6,5), (6,6), (6,7), (5,6), (5,7), (4,7)])
        self.green = {"goal" : self.redstart, "pawns" : self.greenstart, "player" : 1, "name" : "Green"}
        self.red = {"goal" : self.greenstart, "pawns" : self.redstart, "player" : 0, "name" : "Red"}

        self.teams = [self.red, self.green]

        self.board = [[-1] * self.xy_dim for i in range(self.xy_dim)]
        for pawn in self.greenstart:
            self.board[pawn[0]][pawn[1]] = 1
        for pawn in self.redstart:
            self.board[pawn[0]][pawn[1]] = 0

        self.status_message = ""
        self.gui = None
        self.turn = 1

        print("First move: player ", self.teams[self.turn]["name"])
        self.setStatusMessage("Player "+self.teams[self.turn]["name"] +" gets the first move.")


    def setStatusMessage(self,string):
        self.status_message = string
        self.statusChangedEvent()

    def getStatusMessage(self):
        return self.status_message

    def statusChangedEvent(self):
        if self.gui is not None:
            self.gui.statusChangedEvent()

    def pawnMovedEvent(self,pawn):
        if self.gui is not None:
            self.gui.pawnMovedEvent()

    def checkWinState(self, board, check_player=None):
        if( self.green["goal"] == self.green["pawns"]):
            return 1
        elif(self.red["goal"] == self.red["pawns"]):
            return 0
        else:
            return False

    def findMoves(self, pawn):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                posx = pawn[0] + i
                posy = pawn[1] + j
                if not ( posx < 0 or posx >= self.xy_dim or posy < 0 or posy >= self.xy_dim ):
                    if ((posx, posy) not in self.red["pawns"]):
                        if((posx, posy) not in self.green["pawns"]):
                            moves.append((posx,posy))

        for i in range(-1, 2):
            for j in range(-1, 2):
                posx = pawn[0] + 2*i
                posy = pawn[1] + 2*j
                if not ( posx < 0 or posx >= self.xy_dim or posy < 0 or posy >= self.xy_dim ):
                    if ((posx, posy) not in self.red["pawns"]):
                        if((posx, posy) not in self.green["pawns"]):
                            if((i,j) in self.red["pawns"] or (i,j) in self.green["pawns"]):
                                path = [(pawn[0], pawn[1])]
                                jumps = self.findJumps((posx, posy), path)
                                for jump in jumps:
                                    moves.append(jump)
                                print()
                                print(moves)
                                moves.append((posx,posy))

        return moves

    def findJumps(self, pawn, path):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                posx = pawn[0] + 2*i
                posy = pawn[1] + 2*j
                if not ( posx < 0 or posx >= self.xy_dim or posy < 0 or posy >= self.xy_dim ):
                    if ((posx, posy) not in self.red["pawns"]):
                        if((posx, posy) not in self.green["pawns"]):
                            if((i,j) in self.red["pawns"] or (i,j) in self.green["pawns"]):
                                if (posx, posy) not in path:
                                    path.append((pawn[0], pawn[1]))
                                    jumps = self.findJumps((posx, posy), path)
                                    for jump in jumps:
                                        moves.append(jump)
                                    moves.append((posx,posy))

        return moves

    def findAllMoves(self, player):
        moves = []
        for pawn in player["pawns"]:
            moves.append(findMoves(pawn))
        return moves

    def move(self, player, from_node, to_node):
        if(player != None and player["player"] == self.turn):
            if to_node in self.findMoves(from_node):
                player["pawns"].remove(from_node)
                player["pawns"].add(to_node)
                self.board[from_node[0]][from_node[1]] = -1
                self.board[to_node[0]][to_node[1]] = self.turn

                if(self.turn == 0):
                    self.turn = 1
                else :
                    self.turn = 0

                self.setStatusMessage("Move completed. Now player "+ self.teams[self.turn]["name"]+ "'s turn.")
                victor = self.checkWinState(self.board)
                if(victor):
                    self.setStatusMessage("Player "+ rt[victor]+ " wins!")
                    self.gui.winStatusEvent()
                self.pawnMovedEvent(None)
                return True
        return False

    def validateMove(self, from_node, to_node, player):
        if( player != None and player["player"] == self.turn):
            if to_node in self.findMoves(from_node):
                return True
        else:
            return False

def main():
    board = HalmaCore()
    #board.printBoard()
    #board.moveXY(3,0,5,0,1)
    #board.printBoard()
    #print(board.findAllMoves(0,moves_as_coords=True))

if __name__ == "__main__":
    main()
