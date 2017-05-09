import math
from collections import namedtuple

mm_tree = namedtuple('Tree', ['state', 'score', 'children', 'move'])

def __init__(self):
    self.centerline = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)]
    
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
        pawn_position_val = getCenterlineDist( pawn )
        pawn_position_val + getGoalDist( pawn, player.goal)
        value = value + pawn_position_val
    return value


