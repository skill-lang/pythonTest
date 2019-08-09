#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from escaping.internal import SkillState, SkillObject, Mode


class Boolean(SkillObject):
    """
     Representation of another type.
     @note  Caused by a Bug in the C generator.
    """

    def __init__(self, skillID=-1, Zbool=None, boolean=False):
        """
        Create a new unmanaged Boolean. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Boolean, self).__init__(skillID)
        self.skillName = "boolean"
        self.Zbool: Boolean = Zbool
        self.boolean: bool = boolean

    def getBool(self):
        return self.Zbool

    def setBool(self, value):
        assert isinstance(value, Boolean) or value is None
        self.Zbool = value

    def getBoolean(self):
        return self.boolean

    def setBoolean(self, value):
        assert isinstance(value, bool) or value is None
        self.boolean = value


class If(SkillObject):
    """
     Another stupid typename
    """

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged If. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(If, self).__init__(skillID)
        self.skillName = "if"
        


class Int(SkillObject):
    """
     Stupid typename
    """

    def __init__(self, skillID=-1, Zfor=None, Zif=None):
        """
        Create a new unmanaged Int. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Int, self).__init__(skillID)
        self.skillName = "int"
        self.Zfor: If = Zfor
        self.Zif: Int = Zif

    def getFor(self):
        return self.Zfor

    def setFor(self, value):
        assert isinstance(value, If) or value is None
        self.Zfor = value

    def getIf(self):
        return self.Zif

    def setIf(self, value):
        assert isinstance(value, Int) or value is None
        self.Zif = value


class Z2200(SkillObject):
    """
     non-printable unicode characters
    """

    def __init__(self, skillID=-1, euro=None, Z2622=None):
        """
        Create a new unmanaged ∀. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Z2200, self).__init__(skillID)
        self.skillName = "∀"
        self.euro: Z2200 = euro
        self.Z2622: str = Z2622

    def geteuro(self):
        return self.euro

    def seteuro(self, value):
        assert isinstance(value, Z2200) or value is None
        self.euro = value

    def getZ2622(self):
        return self.Z2622

    def setZ2622(self, value):
        assert isinstance(value, str) or value is None
        self.Z2622 = value


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
        return SkillState.open(path, mode, [Boolean, If, Int, Z2200])
