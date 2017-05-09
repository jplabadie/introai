from ast import literal_eval

def parseFileToList(fname):
    with open(fname, "r") as file:
        data_as_string = file.read()
        print(data_as_string)
        data_list = literal_eval(data_as_string)
    return data_list


class HalmaNode:
    def __init__(self, name, value=0, parent=None):
        self.Name = name      # a char
        self.value = value    # an int
        self.parent = parent  # a node reference
        self.children = []    # a list of nodes

    def addChild(self, childNode):
        self.children.append(childNode)

class HalmaTree:
    def __init__(self):
        self.root = None

    def buildTree(self, data_list):

        self.root = HalmaNode(data_list.pop(0))
        for elem in data_list:
            self.parseSubtree(elem, self.root)

    def parseSubtree(self, data_list, parent):
        # base case
        if type(data_list) is tuple:
            # make connections
            leaf_node = HalmaNode(data_list[0])
            leaf_node.parent = parent
            parent.addChild(leaf_node)
            # if we're at a leaf, set the value
            if len(data_list) == 2:
                leaf_node.value = data_list[1]
            return

        # recursive case
        tree_node = HalmaNode(data_list.pop(0))
        # make connections
        tree_node.parent = parent
        parent.addChild(tree_node)
        for elem in data_list:
            self.parseSubtree(elem, tree_node)

        # return from entire method if base case and recursive case both done running
        return