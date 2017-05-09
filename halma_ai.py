import math
from collections import namedtuple

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

#return a namedtuple implementation of a minimax tree with the given params
def getMMTree(self, depth, friendly, opfor, node_max, team_info, opp_info, move, prune, alpha, evalFunc):
    mm_tree = namedtuple('Tree', ['state', 'score', 'children', 'move'])
    children = []
    
    if node_max:
        teams = (friendly, opfor)
        minimax = max
        compVal = -1
        score = 0
    else:
        teams = (opfor, friendly)
        minimax = min
        compVal = 1
        score = float('inf')

    if not depth == 0:
        for src in friendly:
            for dest in self.board.get_valid_moves(src, team_info):
                teamC = friendly.copy()
                self.halma_core.sub_move(dest, src, team_info, teamC)
                child = self.getMMTree(depth - 1, opfor, teamC, not node_max, opp_info,
                                      team_info, (src, dest), prune, score, evalFunc)
                children.append(child)
                score = minimax(score, child.score)
                if prune and self.compare(score, alpha) == compVal:
                    return mm_tree(teams, score, children, move)
    else:
        score = evalFunc(team_info, friendly, opfor) if node_max else evalFunc(opp_info, opfor, friendly)

        return mm_tree(teams, score, children, move)

