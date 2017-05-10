import math
from collections import namedtuple
#from numpy import linalg
#from scipy.spatial import distance

class HalmaAI( object ):

    def __init__(self,core):
        self.halma_core = core
        self.fbmode = False

    # return distance to goal from current (manhattan) given tuple coords
    def getGoalDist(self, cur_pos, player_goal):
        distance = float('inf')
        for target in player_goal:
            goal_dist = ((target[0]-cur_pos[0])**2)
            goal_dist = goal_dist + (target[1]-cur_pos[1])**2
            goal_dist = goal_dist**(1/2)
            distance = min(distance,abs(goal_dist))
        return distance

    def getSumOfSquares(self, from_node, to_node):
        sum = 0
        for node in from_node:
            sum = sum + (((to_node[0] -node[0]) ** 2) + ((to_node[1] - node[1])) ** 2)
        return sum

    def getGoalFill(self, player):
        value = 0
        for pawn in player["pawns"]:
            if pawn in player["goal"]:
                value += 20
        return value

    # return the distance to the centerline (nearest centerline coord)
    # see 'Another Formula' https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line)
    def getCenterlineDist(self, cur_pos):
        x = cur_pos[0]
        y = cur_pos[1]
        x_n = 7 #todo: remove hardcoded dimensions
        y_n = -7 #todo: remove hardcoded dimensions

        numerator = abs(y_n * x - (x_n * y) + ((x_n - 1) ** 2))
        denominator = math.sqrt(y_n ** 2 + x_n ** 2)
        distance = numerator / denominator
        return distance

    def getLineDist(self, cur_pos):
        min = 100
        line = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)]
        for center in line:
            cur = 0#distance.euclidean(cur_pos,center)
            if cur<min:
                min = cur

    # evaluate a given board for a given player
    def getBoardValue(self, player):
        value = 0
        for pawn in player["pawns"]:
            pawn_position_val = (5-self.getCenterlineDist( pawn ))
            pawn_position_val = pawn_position_val+(8-self.getGoalDist( pawn, player["goal"]))
            goalFill = self.getGoalFill(player)
            value = value + pawn_position_val + goalFill
        return value

    # return a namedtuple implementation of a minimax tree with the given params
    def getMMTree(self, depth, cur_player, op_player, node_max, move, prune, alpha):
        mm_tree = namedtuple('Tree', ['state', 'score', 'children', 'move'])
        children = []

        if node_max:
            teams = (cur_player, op_player)
            minimax = max
            compVal = -1
            score = 0
        else:
            teams = (op_player, cur_player)
            minimax = min
            compVal = 1
            score = float('inf')

        if not depth == 0:
            for from_pos in cur_player["pawns"]:
                for to_pos in self.halma_core.findMoves(from_pos,cur_player):

                    cpy_goal = cur_player["goal"].copy()
                    cpy_pawns =  cur_player["pawns"].copy()
                    cpy_player = cur_player["player"]
                    cpy_name = cur_player["name"]

                    cur_player_cpy = {"goal":cpy_goal,"pawns":cpy_pawns,"player":cpy_player,"name":cpy_name}

                    self.halma_core.exploreMove(cur_player_cpy, from_pos, to_pos)
                    child = self.getMMTree(depth - 1, op_player, cur_player_cpy, not node_max,
                                           (from_pos, to_pos), prune, score)

                    children.append(child)

                    score = minimax(score, child.score)
                    ab = (score > alpha) - (alpha > score)
                    #print( "!"+str(ab)+":"+str(compVal) + ":"+str(minimax))
                    #print(prune)
                    if prune and ab == compVal:
                        #print("\n\n#$%@%$%#%#%Q@#%@$#% PRUNED #%$%^%$^#\n\n")
                        return mm_tree(teams, score, children, move)
        else:
            score = self.getBoardValue(cur_player) if node_max else self.getBoardValue(op_player)

        #print(score)
        return mm_tree(teams, score, children, move)

    # return a best move (as a tuple coord pair) given parameters, using the minimaxTree
    #(1, self.teams[self.team_turn], self.teams[not self.team_turn], True, True, self.hFuncs[self.team_turn])
    def getBestMove(self, cur_player, op_player, depth, max_node, ab_prune):
        score = math.inf
        if max_node:
            score = 0
        if self.fbmode:
            print("FBMODE")
            return self.fbmove(cur_player)
        mm_tree = self.getMMTree(depth, cur_player, op_player, max_node, (), ab_prune, score)

        for child in mm_tree.children:
            if child.score == mm_tree.score:
                if self.fbmode:
                    print("FBMODE")
                    return self.fbmove(cur_player)

               # print("highest: "+str(child.score))
                #print(child)
                return child.move
        return False

    def fbmove(self, player):
        moves = self.halma_core.findAllMoves(player)
        best_move = None
        min = 100

        if player["name"] == "green":
            p_goal = (7,7)
        else:
            p_goal = (0,0)

        print("Moves available: " + str(moves))
        for move in moves:
            c_val = self.getCenterlineDist(move)
            g_val = self.getGoalDist(move,player["goal"])
            tot_val = c_val + g_val
            print("move: "+ str(move)+ " totval: "+ str(tot_val)+" lineval: " + str(c_val) + " goalval: "+ str(c_val))

            if(tot_val<min):
                min = tot_val
                best_move = move
        print("BestbyFB: "+ str(best_move))
        return best_move
