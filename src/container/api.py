#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from container.internal import SkillState, SkillObject, Mode


class Container(SkillObject):

    def __init__(self, skillID=-1, arr=None, f=None, l=None, s=None, someSet=None, varr=None):
        """
        Create a new unmanaged Container. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Container, self).__init__(skillID)
        self.skillName = "container"
        self.arr: list = arr
        self.f: dict = f
        self.l: list = l
        self.s: set = s
        self.someSet: set = someSet
        self.varr: list = varr

    def getArr(self):
        return self.arr

    def setArr(self, value):
        assert isinstance(value, list) or value is None
        self.arr = value

    def getF(self):
        return self.f

    def setF(self, value):
        assert isinstance(value, dict) or value is None
        self.f = value

    def getL(self):
        return self.l

    def setL(self, value):
        assert isinstance(value, list) or value is None
        self.l = value

    def getS(self):
        return self.s

    def setS(self, value):
        assert isinstance(value, set) or value is None
        self.s = value

    def getSomeSet(self):
        return self.someSet

    def setSomeSet(self, value):
        assert isinstance(value, set) or value is None
        self.someSet = value

    def getVarr(self):
        return self.varr

    def setVarr(self, value):
        assert isinstance(value, list) or value is None
        self.varr = value


class SomethingElse(SkillObject):
    """
     no instance of this is required
    """

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged SomethingElse. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(SomethingElse, self).__init__(skillID)
        self.skillName = "somethingelse"
        


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
        return SkillState.open(path, mode, [Container, SomethingElse])
