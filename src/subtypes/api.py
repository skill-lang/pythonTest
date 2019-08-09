#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from subtypes.internal import SkillState, SkillObject, Mode


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


class B(A):

    def __init__(self, skillID=-1, b=None, a=None):
        """
        Create a new unmanaged B. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(B, self).__init__(skillID)
        self.skillName = "b"
        self.b: B = b
        self.a: A = a

    def getB(self):
        return self.b

    def setB(self, value):
        assert isinstance(value, B) or value is None
        self.b = value


class D(B):

    def __init__(self, skillID=-1, d=None, b=None, a=None):
        """
        Create a new unmanaged D. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(D, self).__init__(skillID)
        self.skillName = "d"
        self.d: D = d
        self.b: B = b
        self.a: A = a

    def getD(self):
        return self.d

    def setD(self, value):
        assert isinstance(value, D) or value is None
        self.d = value


class C(A):

    def __init__(self, skillID=-1, c=None, a=None):
        """
        Create a new unmanaged C. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(C, self).__init__(skillID)
        self.skillName = "c"
        self.c: C = c
        self.a: A = a

    def getC(self):
        return self.c

    def setC(self, value):
        assert isinstance(value, C) or value is None
        self.c = value


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
        return SkillState.open(path, mode, [A, B, D, C])
