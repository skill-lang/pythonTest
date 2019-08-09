#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from graphInterface.internal import SkillState, SkillObject, Mode


class ColorHolder(SkillObject):
    """
     check that abstract colors are in fact annotations
    """

    def __init__(self, skillID=-1, anAbstractNode=None, anAnnotation=None):
        """
        Create a new unmanaged ColorHolder. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(ColorHolder, self).__init__(skillID)
        self.skillName = "colorholder"
        self.anAbstractNode: AbstractNode = anAbstractNode
        self.anAnnotation: SkillObject = anAnnotation

    def getAnAbstractNode(self):
        return self.anAbstractNode

    def setAnAbstractNode(self, value):
        assert isinstance(value, AbstractNode) or value is None
        self.anAbstractNode = value

    def getAnAnnotation(self):
        return self.anAnnotation

    def setAnAnnotation(self, value):
        assert isinstance(value, SkillObject) or value is None
        self.anAnnotation = value


class AbstractNode(SkillObject):

    def __init__(self, skillID=-1, edges=None, Zmap=None):
        """
        Create a new unmanaged AbstractNode. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(AbstractNode, self).__init__(skillID)
        self.skillName = "abstractnode"
        self.edges: set = edges
        self.Zmap: dict = Zmap

    def getEdges(self):
        return self.edges

    def setEdges(self, value):
        assert isinstance(value, set) or value is None
        self.edges = value

    def getMap(self):
        return self.Zmap

    def setMap(self, value):
        assert isinstance(value, dict) or value is None
        self.Zmap = value


class Node(AbstractNode):
    """
     a graph of colored nodes
    """

    def __init__(self, skillID=-1, Znext=None, color=None, mark=None, edges=None, Zmap=None):
        """
        Create a new unmanaged Node. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Node, self).__init__(skillID)
        self.skillName = "node"
        self.Znext: SkillObject = Znext
        self.color: str = color
        self.mark: str = mark
        self.edges: set = edges
        self.Zmap: dict = Zmap

    def getNext(self):
        return self.Znext

    def setNext(self, value):
        assert isinstance(value, SkillObject) or value is None
        self.Znext = value

    def getColor(self):
        return self.color

    def setColor(self, value):
        assert isinstance(value, str) or value is None
        self.color = value

    def getMark(self):
        return self.mark

    def setMark(self, value):
        assert isinstance(value, str) or value is None
        self.mark = value


class SubNode(Node):
    """
     check that projection wont interfere with regular subtyping
    """

    def __init__(self, skillID=-1, f=None, n=None, Znext=None, color=None, mark=None, edges=None, Zmap=None):
        """
        Create a new unmanaged SubNode. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(SubNode, self).__init__(skillID)
        self.skillName = "subnode"
        self.f: SkillObject = f
        self.n: Node = n
        self.Znext: SkillObject = Znext
        self.color: str = color
        self.mark: str = mark
        self.edges: set = edges
        self.Zmap: dict = Zmap

    def getF(self):
        return self.f

    def setF(self, value):
        assert isinstance(value, SkillObject) or value is None
        self.f = value

    def getN(self):
        return self.n

    def setN(self, value):
        assert isinstance(value, Node) or value is None
        self.n = value


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
        return SkillState.open(path, mode, [ColorHolder, AbstractNode, Node, SubNode])
