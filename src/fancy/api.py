#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from fancy.internal import SkillState, SkillObject, Mode


class A(SkillObject):

    def __init__(self, skillID=-1, a=None, Parent=None):
        """
        Create a new unmanaged A. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(A, self).__init__(skillID)
        self.skillName = "a"
        self.a: SkillObject = a
        self.Parent: A = Parent

    def getA(self):
        return self.a

    def setA(self, value):
        assert isinstance(value, SkillObject) or value is None
        self.a = value

    def getParent(self):
        return self.Parent

    def setParent(self, value):
        assert isinstance(value, A) or value is None
        self.Parent = value


class B(A):

    def __init__(self, skillID=-1, a=None, Parent=None):
        """
        Create a new unmanaged B. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(B, self).__init__(skillID)
        self.skillName = "b"
        self.a: SkillObject = a
        self.Parent: A = Parent


class C(B):

    def __init__(self, skillID=-1, Value=None, a=None, Parent=None):
        """
        Create a new unmanaged C. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(C, self).__init__(skillID)
        self.skillName = "c"
        self.Value: C = Value
        self.a: SkillObject = a
        self.Parent: A = Parent

    def getValue(self):
        return self.Value

    def setValue(self, value):
        assert isinstance(value, C) or value is None
        self.Value = value


class D(C):

    def __init__(self, skillID=-1, Value=None, a=None, Parent=None):
        """
        Create a new unmanaged D. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(D, self).__init__(skillID)
        self.skillName = "d"
        self.Value: C = Value
        self.a: SkillObject = a
        self.Parent: A = Parent


class G(C):

    def __init__(self, skillID=-1, aMap=None, Value=None, a=None, Parent=None):
        """
        Create a new unmanaged G. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(G, self).__init__(skillID)
        self.skillName = "g"
        self.aMap: dict = aMap
        self.Value: C = Value
        self.a: SkillObject = a
        self.Parent: A = Parent

    def getAMap(self):
        return self.aMap

    def setAMap(self, value):
        assert isinstance(value, dict) or value is None
        self.aMap = value


class H(A):

    def __init__(self, skillID=-1, a=None, Parent=None):
        """
        Create a new unmanaged H. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(H, self).__init__(skillID)
        self.skillName = "h"
        self.a: SkillObject = a
        self.Parent: A = Parent


class I(A):

    def __init__(self, skillID=-1, a=None, Parent=None):
        """
        Create a new unmanaged I. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(I, self).__init__(skillID)
        self.skillName = "i"
        self.a: SkillObject = a
        self.Parent: A = Parent


class J(A):

    def __init__(self, skillID=-1, a=None, Parent=None):
        """
        Create a new unmanaged J. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(J, self).__init__(skillID)
        self.skillName = "j"
        self.a: SkillObject = a
        self.Parent: A = Parent


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
        return SkillState.open(path, mode, [A, B, C, D, G, H, I, J])
