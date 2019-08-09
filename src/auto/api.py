#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from auto.internal import SkillState, SkillObject, Mode


class A(SkillObject):
    """
     Check subtyping; use single fields only, because otherwise field IDs are underspecified
    """

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


class C(B):

    def __init__(self, skillID=-1, c=None, b=None, a=None):
        """
        Create a new unmanaged C. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(C, self).__init__(skillID)
        self.skillName = "c"
        self.c: C = c
        self.b: B = b
        self.a: A = a

    def getC(self):
        return self.c

    def setC(self, value):
        assert isinstance(value, C) or value is None
        self.c = value


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


class NoSerializedData(SkillObject):
    """
     All fields of this type are auto.
     @author  Timm Felden
    """

    def __init__(self, skillID=-1, age=0, name=None, seen=False, someIntegersInAList=None, someMap=None, someReference=None):
        """
        Create a new unmanaged NoSerializedData. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(NoSerializedData, self).__init__(skillID)
        self.skillName = "noserializeddata"
        self.age: int = age
        self.name: str = name
        self.seen: bool = seen
        self.someIntegersInAList: list = someIntegersInAList
        self.someMap: dict = someMap
        self.someReference: NoSerializedData = someReference

    def getAge(self):
        return self.age

    def setAge(self, value):
        assert isinstance(value, int) or value is None
        self.age = value

    def getName(self):
        return self.name

    def setName(self, value):
        assert isinstance(value, str) or value is None
        self.name = value

    def getSeen(self):
        return self.seen

    def setSeen(self, value):
        assert isinstance(value, bool) or value is None
        self.seen = value

    def getSomeIntegersInAList(self):
        return self.someIntegersInAList

    def setSomeIntegersInAList(self, value):
        assert isinstance(value, list) or value is None
        self.someIntegersInAList = value

    def getSomeMap(self):
        return self.someMap

    def setSomeMap(self, value):
        assert isinstance(value, dict) or value is None
        self.someMap = value

    def getSomeReference(self):
        return self.someReference

    def setSomeReference(self, value):
        assert isinstance(value, NoSerializedData) or value is None
        self.someReference = value


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
        return SkillState.open(path, mode, [A, B, C, D, NoSerializedData])
