#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from unknown.internal import SkillState, SkillObject, Mode


class A(SkillObject):

    def __init__(self, skillID=-1, a=None):
        """
        Create a new unmanaged A. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(A, self).__init__(skillID)
        self.skillName = "a"
        self.a: A = a

    def getA(self):
        return self.a

    def setA(self, value):
        assert isinstance(value, A) or value is None
        self.a = value


class C(A):

    def __init__(self, skillID=-1, a=None):
        """
        Create a new unmanaged C. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(C, self).__init__(skillID)
        self.skillName = "c"
        self.a: A = a


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
        return SkillState.open(path, mode, [A, C])
