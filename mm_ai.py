class AlphaBetaMM:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        return

    def abSearch(self, node):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            value = self.getMinValue(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        print("util score of root: " + str(best_val))
        print("best move: " + best_state.Name)
        return best_state

    def getMaxValue(self, node, alpha, beta):
        #print("max at: " + node.Name)
        if self.isTerminal(node):
            return self.getScore(node)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.getMinValue(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def getMinValue(self, node, alpha, beta):
        print ("min at: " + node.Name)
        if self.isTerminal(node):
            return self.getScore(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.getMaxValue(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    # successor states (children)
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    # return true if the node has no children, false otherwise
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getScore(self, node):
        assert node is not None
        return node.value