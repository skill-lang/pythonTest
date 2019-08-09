#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from floats.internal import SkillState, SkillObject, Mode


class DoubleTest(SkillObject):
    """
     check some double values.
    """

    def __init__(self, skillID=-1, minusZZero=0.0, NaN=0.0, pi=0.0, two=0.0, zero=0.0):
        """
        Create a new unmanaged DoubleTest. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(DoubleTest, self).__init__(skillID)
        self.skillName = "doubletest"
        self.minusZZero: float = minusZZero
        self.NaN: float = NaN
        self.pi: float = pi
        self.two: float = two
        self.zero: float = zero

    def getMinusZZero(self):
        return self.minusZZero

    def setMinusZZero(self, value):
        assert isinstance(value, float) or value is None
        self.minusZZero = value

    def getNaN(self):
        return self.NaN

    def setNaN(self, value):
        assert isinstance(value, float) or value is None
        self.NaN = value

    def getPi(self):
        return self.pi

    def setPi(self, value):
        assert isinstance(value, float) or value is None
        self.pi = value

    def getTwo(self):
        return self.two

    def setTwo(self, value):
        assert isinstance(value, float) or value is None
        self.two = value

    def getZZero(self):
        return self.zero

    def setZZero(self, value):
        assert isinstance(value, float) or value is None
        self.zero = value


class FloatTest(SkillObject):
    """
     check some float values.
    """

    def __init__(self, skillID=-1, minusZZero=0.0, NaN=0.0, pi=0.0, two=0.0, zero=0.0):
        """
        Create a new unmanaged FloatTest. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(FloatTest, self).__init__(skillID)
        self.skillName = "floattest"
        self.minusZZero: float = minusZZero
        self.NaN: float = NaN
        self.pi: float = pi
        self.two: float = two
        self.zero: float = zero

    def getMinusZZero(self):
        return self.minusZZero

    def setMinusZZero(self, value):
        assert isinstance(value, float) or value is None
        self.minusZZero = value

    def getNaN(self):
        return self.NaN

    def setNaN(self, value):
        assert isinstance(value, float) or value is None
        self.NaN = value

    def getPi(self):
        return self.pi

    def setPi(self, value):
        assert isinstance(value, float) or value is None
        self.pi = value

    def getTwo(self):
        return self.two

    def setTwo(self, value):
        assert isinstance(value, float) or value is None
        self.two = value

    def getZZero(self):
        return self.zero

    def setZZero(self, value):
        assert isinstance(value, float) or value is None
        self.zero = value


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
        return SkillState.open(path, mode, [DoubleTest, FloatTest])
