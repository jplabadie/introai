
# return distance to goal from current (manhattan) given tuple coords
def getGoalDist(self, cur_pos, targ_zone):
    dist = float('inf')
    for target in targ_zone:
        goal_dist = ((target[0]-cur_pos[0])**2)
        goal_dist = goal_dist + target[1]-cur_pos[1]**2
        goal_dist = goal_dist**(1/2)

    return min(dist,goal_dist)

