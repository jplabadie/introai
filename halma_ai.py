import math
from collections import namedtuple

inf = float('inf')

def __init__(self,core):
    self.halma_core = core

# return distance to goal from current (manhattan) given tuple coords
def getGoalDist(self, cur_pos, player):
    distance = float('inf')
    for target in player.goal:
        goal_dist = ((target[0]-cur_pos[0])**2)
        goal_dist = goal_dist + target[1]-cur_pos[1]**2
        goal_dist = goal_dist**(1/2)
        distance = min(distance,goal_dist)
    return distance

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

# evaluate a given board for a given player
def getBoardValue(self, player):
    value = 0
    for pawn in player.pawns:
        pawn_position_val = self.getCenterlineDist( pawn )
        pawn_position_val + self.getGoalDist( pawn, player.goal)
        value = value + pawn_position_val
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
            for to_pos in self.board.findAllMoves(from_pos, cur_player):
                cur_player_cpy = cur_player.copy()
                self.halma_core.move(cur_player_cpy, from_pos, to_pos)
                child = self.getMMTree(depth - 1, op_player, cur_player_cpy, not node_max,
                                       (from_pos, to_pos), prune, score)
                children.append(child)
                score = minimax(score, child.score)
                if prune and ((score>alpha)-(alpha>score) == compVal):
                    return mm_tree(teams, score, children, move)
    else:
        score = getBoardValue(cur_player) if node_max else getBoardValue(op_player)

    return mm_tree(teams, score, children, move)

# return a best move (as a tuple coord pair) given parameters, using the minimaxTree
def getBestMove(self, cur_player, op_player, depth, max_node, ab_prune):
    alpha = inf
    if max_node:
        alpha = 0

    mm_tree = self.getMMTree(depth, cur_player, op_player, max_node, (), ab_prune, alpha)

    for child in mm_tree.children:
        if child.score == mm_tree.score:
            return child.move
    return ((0, 0), (0, 0))
