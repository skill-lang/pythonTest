#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from basicTypes.internal import SkillState, SkillObject, Mode


class BasicBool(SkillObject):
    """
     Contains a basic bool
    """

    def __init__(self, skillID=-1, basicBool=False):
        """
        Create a new unmanaged BasicBool. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicBool, self).__init__(skillID)
        self.skillName = "basicbool"
        self.basicBool: bool = basicBool

    def getBasicBool(self):
        return self.basicBool

    def setBasicBool(self, value):
        assert isinstance(value, bool) or value is None
        self.basicBool = value


class BasicFloat32(SkillObject):
    """
     Contains a basic Float32
    """

    def __init__(self, skillID=-1, basicFloat=0.0):
        """
        Create a new unmanaged BasicFloat32. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicFloat32, self).__init__(skillID)
        self.skillName = "basicfloat32"
        self.basicFloat: float = basicFloat

    def getBasicFloat(self):
        return self.basicFloat

    def setBasicFloat(self, value):
        assert isinstance(value, float) or value is None
        self.basicFloat = value


class BasicFloat64(SkillObject):
    """
     Contains a basic Float64
    """

    def __init__(self, skillID=-1, basicFloat=0.0):
        """
        Create a new unmanaged BasicFloat64. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicFloat64, self).__init__(skillID)
        self.skillName = "basicfloat64"
        self.basicFloat: float = basicFloat

    def getBasicFloat(self):
        return self.basicFloat

    def setBasicFloat(self, value):
        assert isinstance(value, float) or value is None
        self.basicFloat = value


class BasicFloats(SkillObject):
    """
     Contains all basic float types
    """

    def __init__(self, skillID=-1, float32=None, float64=None):
        """
        Create a new unmanaged BasicFloats. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicFloats, self).__init__(skillID)
        self.skillName = "basicfloats"
        self.float32: BasicFloat32 = float32
        self.float64: BasicFloat64 = float64

    def getFloat32(self):
        return self.float32

    def setFloat32(self, value):
        assert isinstance(value, BasicFloat32) or value is None
        self.float32 = value

    def getFloat64(self):
        return self.float64

    def setFloat64(self, value):
        assert isinstance(value, BasicFloat64) or value is None
        self.float64 = value


class BasicInt16(SkillObject):
    """
     Contains a basic Int16
    """

    def __init__(self, skillID=-1, basicInt=0):
        """
        Create a new unmanaged BasicInt16. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicInt16, self).__init__(skillID)
        self.skillName = "basicint16"
        self.basicInt: int = basicInt

    def getBasicInt(self):
        return self.basicInt

    def setBasicInt(self, value):
        assert isinstance(value, int) or value is None
        self.basicInt = value


class BasicInt32(SkillObject):
    """
     Contains a basic Int32
    """

    def __init__(self, skillID=-1, basicInt=0):
        """
        Create a new unmanaged BasicInt32. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicInt32, self).__init__(skillID)
        self.skillName = "basicint32"
        self.basicInt: int = basicInt

    def getBasicInt(self):
        return self.basicInt

    def setBasicInt(self, value):
        assert isinstance(value, int) or value is None
        self.basicInt = value


class BasicInt64I(SkillObject):
    """
     Contains a basic Int64 with i64
    """

    def __init__(self, skillID=-1, basicInt=0):
        """
        Create a new unmanaged BasicInt64I. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicInt64I, self).__init__(skillID)
        self.skillName = "basicint64i"
        self.basicInt: int = basicInt

    def getBasicInt(self):
        return self.basicInt

    def setBasicInt(self, value):
        assert isinstance(value, int) or value is None
        self.basicInt = value


class BasicInt64V(SkillObject):
    """
     Contains a basic Int64 with v64
    """

    def __init__(self, skillID=-1, basicInt=0):
        """
        Create a new unmanaged BasicInt64V. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicInt64V, self).__init__(skillID)
        self.skillName = "basicint64v"
        self.basicInt: int = basicInt

    def getBasicInt(self):
        return self.basicInt

    def setBasicInt(self, value):
        assert isinstance(value, int) or value is None
        self.basicInt = value


class BasicInt8(SkillObject):
    """
     Contains a basic Int8
    """

    def __init__(self, skillID=-1, basicInt=0):
        """
        Create a new unmanaged BasicInt8. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicInt8, self).__init__(skillID)
        self.skillName = "basicint8"
        self.basicInt: int = basicInt

    def getBasicInt(self):
        return self.basicInt

    def setBasicInt(self, value):
        assert isinstance(value, int) or value is None
        self.basicInt = value


class BasicIntegers(SkillObject):
    """
     Contains all basic int types
    """

    def __init__(self, skillID=-1, int16=None, int32=None, int64I=None, int64V=None, int8=None):
        """
        Create a new unmanaged BasicIntegers. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicIntegers, self).__init__(skillID)
        self.skillName = "basicintegers"
        self.int16: BasicInt16 = int16
        self.int32: BasicInt32 = int32
        self.int64I: BasicInt64I = int64I
        self.int64V: BasicInt64V = int64V
        self.int8: BasicInt8 = int8

    def getInt16(self):
        return self.int16

    def setInt16(self, value):
        assert isinstance(value, BasicInt16) or value is None
        self.int16 = value

    def getInt32(self):
        return self.int32

    def setInt32(self, value):
        assert isinstance(value, BasicInt32) or value is None
        self.int32 = value

    def getInt64I(self):
        return self.int64I

    def setInt64I(self, value):
        assert isinstance(value, BasicInt64I) or value is None
        self.int64I = value

    def getInt64V(self):
        return self.int64V

    def setInt64V(self, value):
        assert isinstance(value, BasicInt64V) or value is None
        self.int64V = value

    def getInt8(self):
        return self.int8

    def setInt8(self, value):
        assert isinstance(value, BasicInt8) or value is None
        self.int8 = value


class BasicString(SkillObject):
    """
     Contains a basic String
    """

    def __init__(self, skillID=-1, basicString=None):
        """
        Create a new unmanaged BasicString. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicString, self).__init__(skillID)
        self.skillName = "basicstring"
        self.basicString: str = basicString

    def getBasicString(self):
        return self.basicString

    def setBasicString(self, value):
        assert isinstance(value, str) or value is None
        self.basicString = value


class BasicTypes(SkillObject):
    """
     Includes all basic types
    """

    def __init__(self, skillID=-1, aBool=None, aList=None, aMap=None, anAnnotation=None, anArray=None, anotherUserType=None, aSet=None, aString=None, aUserType=None):
        """
        Create a new unmanaged BasicTypes. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BasicTypes, self).__init__(skillID)
        self.skillName = "basictypes"
        self.aBool: BasicBool = aBool
        self.aList: list = aList
        self.aMap: dict = aMap
        self.anAnnotation: SkillObject = anAnnotation
        self.anArray: list = anArray
        self.anotherUserType: BasicFloats = anotherUserType
        self.aSet: set = aSet
        self.aString: BasicString = aString
        self.aUserType: BasicIntegers = aUserType

    def getABool(self):
        return self.aBool

    def setABool(self, value):
        assert isinstance(value, BasicBool) or value is None
        self.aBool = value

    def getAList(self):
        return self.aList

    def setAList(self, value):
        assert isinstance(value, list) or value is None
        self.aList = value

    def getAMap(self):
        return self.aMap

    def setAMap(self, value):
        assert isinstance(value, dict) or value is None
        self.aMap = value

    def getAnAnnotation(self):
        return self.anAnnotation

    def setAnAnnotation(self, value):
        assert isinstance(value, SkillObject) or value is None
        self.anAnnotation = value

    def getAnArray(self):
        return self.anArray

    def setAnArray(self, value):
        assert isinstance(value, list) or value is None
        self.anArray = value

    def getAnotherUserType(self):
        return self.anotherUserType

    def setAnotherUserType(self, value):
        assert isinstance(value, BasicFloats) or value is None
        self.anotherUserType = value

    def getASet(self):
        return self.aSet

    def setASet(self, value):
        assert isinstance(value, set) or value is None
        self.aSet = value

    def getAString(self):
        return self.aString

    def setAString(self, value):
        assert isinstance(value, BasicString) or value is None
        self.aString = value

    def getAUserType(self):
        return self.aUserType

    def setAUserType(self, value):
        assert isinstance(value, BasicIntegers) or value is None
        self.aUserType = value


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
        return SkillState.open(path, mode, [BasicBool, BasicFloat32, BasicFloat64, BasicFloats, BasicInt16, BasicInt32, BasicInt64I, BasicInt64V, BasicInt8, BasicIntegers, BasicString, BasicTypes])
