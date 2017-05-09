def getGoalDist(self, cur_pos, targ_zone):
    dist = float('inf')
    for target in targ_zone:
        goal_dist = ((targ_zone[0]-cur_pos[0])**2)
        goal_dist = goal_dist + targ_zone[1]-cur_pos[1]**2
        goal_dist