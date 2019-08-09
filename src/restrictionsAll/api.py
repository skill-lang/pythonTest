#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from restrictionsAll.internal import SkillState, SkillObject, Mode


class Comment(SkillObject):

    def __init__(self, skillID=-1, Zproperty=None, target=None, text=None):
        """
        Create a new unmanaged Comment. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Comment, self).__init__(skillID)
        self.skillName = "comment"
        self.Zproperty: Properties = Zproperty
        self.target: SkillObject = target
        self.text: str = text

    def getProperty(self):
        return self.Zproperty

    def setProperty(self, value):
        assert isinstance(value, Properties) or value is None
        self.Zproperty = value

    def getTarget(self):
        return self.target

    def setTarget(self, value):
        assert isinstance(value, SkillObject) or value is None
        self.target = value

    def getText(self):
        return self.text

    def setText(self, value):
        assert isinstance(value, str) or value is None
        self.text = value


class DefaultBoarderCases(SkillObject):

    def __init__(self, skillID=-1, Zfloat=0.0, message=None, none=None, nopDefault=0, system=None):
        """
        Create a new unmanaged DefaultBoarderCases. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(DefaultBoarderCases, self).__init__(skillID)
        self.skillName = "defaultboardercases"
        self.Zfloat: float = Zfloat
        self.message: str = message
        self.none: Properties = none
        self.nopDefault: int = nopDefault
        self.system: SkillObject = system

    def getFloat(self):
        return self.Zfloat

    def setFloat(self, value):
        assert isinstance(value, float) or value is None
        self.Zfloat = value

    def getMessage(self):
        return self.message

    def setMessage(self, value):
        assert isinstance(value, str) or value is None
        self.message = value

    def getZNone(self):
        return self.none

    def setZNone(self, value):
        assert isinstance(value, Properties) or value is None
        self.none = value

    def getNopDefault(self):
        return self.nopDefault

    def setNopDefault(self, value):
        assert isinstance(value, int) or value is None
        self.nopDefault = value

    def getSystem(self):
        return self.system

    def setSystem(self, value):
        assert isinstance(value, SkillObject) or value is None
        self.system = value


class Operator(SkillObject):

    def __init__(self, skillID=-1, name=None):
        """
        Create a new unmanaged Operator. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Operator, self).__init__(skillID)
        self.skillName = "operator"
        self.name: str = name

    def getName(self):
        return self.name

    def setName(self, value):
        assert isinstance(value, str) or value is None
        self.name = value


class Properties(SkillObject):

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged Properties. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Properties, self).__init__(skillID)
        self.skillName = "properties"
        


class ZNone(Properties):

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged None. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(ZNone, self).__init__(skillID)
        self.skillName = "none"
        


class RegularProperty(Properties):
    """
     some regular property
    """

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged RegularProperty. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(RegularProperty, self).__init__(skillID)
        self.skillName = "regularproperty"
        


class System(Properties):
    """
     some properties of the target system
    """

    def __init__(self, skillID=-1, name=None, version=0.0):
        """
        Create a new unmanaged System. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(System, self).__init__(skillID)
        self.skillName = "system"
        self.name: str = name
        self.version: float = version

    def getName(self):
        return self.name

    def setName(self, value):
        assert isinstance(value, str) or value is None
        self.name = value

    def getVersion(self):
        return self.version

    def setVersion(self, value):
        assert isinstance(value, float) or value is None
        self.version = value


class RangeBoarderCases(SkillObject):

    def __init__(self, skillID=-1, degrees=0.0, degrees2=0.0, negative=0, negative2=0, positive=0, positive2=0):
        """
        Create a new unmanaged RangeBoarderCases. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(RangeBoarderCases, self).__init__(skillID)
        self.skillName = "rangeboardercases"
        self.degrees: float = degrees
        self.degrees2: float = degrees2
        self.negative: int = negative
        self.negative2: int = negative2
        self.positive: int = positive
        self.positive2: int = positive2

    def getDegrees(self):
        return self.degrees

    def setDegrees(self, value):
        assert isinstance(value, float) or value is None
        self.degrees = value

    def getDegrees2(self):
        return self.degrees2

    def setDegrees2(self, value):
        assert isinstance(value, float) or value is None
        self.degrees2 = value

    def getNegative(self):
        return self.negative

    def setNegative(self, value):
        assert isinstance(value, int) or value is None
        self.negative = value

    def getNegative2(self):
        return self.negative2

    def setNegative2(self, value):
        assert isinstance(value, int) or value is None
        self.negative2 = value

    def getPositive(self):
        return self.positive

    def setPositive(self, value):
        assert isinstance(value, int) or value is None
        self.positive = value

    def getPositive2(self):
        return self.positive2

    def setPositive2(self, value):
        assert isinstance(value, int) or value is None
        self.positive2 = value


class Term(SkillObject):

    def __init__(self, skillID=-1, arguments=None, operator=None):
        """
        Create a new unmanaged Term. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Term, self).__init__(skillID)
        self.skillName = "term"
        self.arguments: list = arguments
        self.operator: Operator = operator

    def getArguments(self):
        return self.arguments

    def setArguments(self, value):
        assert isinstance(value, list) or value is None
        self.arguments = value

    def getOperator(self):
        return self.operator

    def setOperator(self, value):
        assert isinstance(value, Operator) or value is None
        self.operator = value


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
        return SkillState.open(path, mode, [Comment, DefaultBoarderCases, Operator, Properties, ZNone, RegularProperty, System, RangeBoarderCases, Term])
