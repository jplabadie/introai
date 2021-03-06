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


        self.redstart = set([(0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (2,0), (2,1), (3,0)])
        self.greenstart = set([(7,4), (7,5), (7,6), (7,7), (6,5), (6,6), (6,7), (5,6), (5,7), (4,7)])
        self.green = {"goal" : self.greenstart.copy(), "pawns" : self.greenstart, "player" : 1, "name" : "Green"}
        self.red = {"goal" : self.greenstart.copy(), "pawns" : self.redstart, "player" : 0, "name" : "Red"}

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

    def checkWinState(self,player):
        return set(player["goal"]) == set(player["pawns"])

    def findMoves(self, pawn):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if( i == 0 and j == 0):
                    continue
                posx = pawn[0] + i
                posy = pawn[1] + j
                if not ( posx < 0 or posx >= self.xy_dim or posy < 0 or posy >= self.xy_dim ):
                    if ((posx, posy) not in self.red["pawns"]):
                        if((posx, posy) not in self.green["pawns"]):
                            moves.append((posx,posy))

        for jump in self.findJumps(pawn, [pawn]):
            moves.append(jump)


        return moves

    def findJumps(self, pawn, path):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if( i == 0 and j == 0):
                    continue
                posx = pawn[0] + 2*i
                posy = pawn[1] + 2*j
                if not ( posx < 0 or posx >= self.xy_dim or posy < 0 or posy >= self.xy_dim ):
                    if ((posx, posy) not in self.red["pawns"]):
                        if((posx, posy) not in self.green["pawns"]):
                            jumpx = pawn[0] + i
                            jumpy = pawn[1] + j
                            if not ( jumpx < 0 or jumpx >= self.xy_dim or jumpy < 0 or jumpy >= self.xy_dim ):
                                if(self.board[jumpx][jumpy] != -1 and (jumpx,jumpy) != pawn):
                                    if (posx, posy) not in path:
                                        path.append((pawn[0], pawn[1]))
                                        jumps = self.findJumps((posx, posy), path)
                                        for jump in jumps:
                                            moves.append(jump)
                                        moves.append((posx,posy))
                                        print("jump at " + str(posx) + ", " + str(posy) + " over node" + str(jumpx) + ", " + str(jumpy))

        return moves

    def findAllMoves(self, player, moves_as_coords=False):
        moves = []
        for pawn in player["pawns"]:
            for move in self.findMoves(pawn):
                moves.append(move)
        return set(moves)

    def move(self, player, from_node, to_node):
        if(player != None and player["player"] == self.turn):
            if to_node in self.findMoves(from_node):

                player["pawns"].remove(from_node)
                player["pawns"].add(to_node)

                self.board[from_node[0]][from_node[1]] = -1
                self.board[to_node[0]][to_node[1]] = self.turn
                self.pawnMovedEvent(None)

                if(self.checkWinState(player)):
                    print("Player "+ player["name"] + " wins!")
                    self.setStatusMessage("Player "+ player["name"] + " wins!")
                    self.gui.winStatusEvent()
                    return True

                if(self.turn == 0):
                    self.turn = 1
                else :
                    self.turn = 0

                self.setStatusMessage("Move completed. Now player "+ self.teams[self.turn]["name"]+ "'s turn.")
                return True
        return False


def main():
    board = HalmaCore()
    #board.printBoard()
    #board.moveXY(3,0,5,0,1)
    #board.printBoard()
    #print(board.findAllMoves(0,moves_as_coords=True))

if __name__ == "__main__":
    main()
