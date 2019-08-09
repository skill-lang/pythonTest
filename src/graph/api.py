#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from graph.internal import SkillState, SkillObject, Mode


class Node(SkillObject):
    """
     a graph of colored nodes
    """

    def __init__(self, skillID=-1, color=None, edges=None):
        """
        Create a new unmanaged Node. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Node, self).__init__(skillID)
        self.skillName = "node"
        self.color: str = color
        self.edges: set = edges

    def getColor(self):
        return self.color

    def setColor(self, value):
        assert isinstance(value, str) or value is None
        self.color = value

    def getEdges(self):
        return self.edges

    def setEdges(self, value):
        assert isinstance(value, set) or value is None
        self.edges = value


class SkillFile:
    """
    An abstract skill file that is hiding all the dirty implementation details
    from you.
    """

    @staticmethod
    def open(path, *mode):
        """
        Create a new skill file based on argument path and mode.
        """
        return SkillState.open(path, mode, [Node])
