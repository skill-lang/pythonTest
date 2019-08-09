#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from enums.internal import SkillState, SkillObject, Mode


class TestEnum(SkillObject):
    """
     Test of mapping of enums.
     @author  Timm Felden
    """

    def __init__(self, skillID=-1, name=None, Znext=None):
        """
        Create a new unmanaged TestEnum. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(TestEnum, self).__init__(skillID)
        self.skillName = "testenum"
        self.name: str = name
        self.Znext: TestEnum = Znext

    def getName(self):
        return self.name

    def setName(self, value):
        assert isinstance(value, str) or value is None
        self.name = value

    def getNext(self):
        return self.Znext

    def setNext(self, value):
        assert isinstance(value, TestEnum) or value is None
        self.Znext = value


class Testenum_last(TestEnum):

    def __init__(self, skillID=-1, name=None, Znext=None):
        """
        Create a new unmanaged Testenum:last. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Testenum_last, self).__init__(skillID)
        self.skillName = "testenum:last"
        self.name: str = name
        self.Znext: TestEnum = Znext


class Testenum_third(TestEnum):

    def __init__(self, skillID=-1, name=None, Znext=None):
        """
        Create a new unmanaged Testenum:third. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Testenum_third, self).__init__(skillID)
        self.skillName = "testenum:third"
        self.name: str = name
        self.Znext: TestEnum = Znext


class Testenum_second(TestEnum):

    def __init__(self, skillID=-1, name=None, Znext=None):
        """
        Create a new unmanaged Testenum:second. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Testenum_second, self).__init__(skillID)
        self.skillName = "testenum:second"
        self.name: str = name
        self.Znext: TestEnum = Znext


class Testenum_default(TestEnum):

    def __init__(self, skillID=-1, name=None, Znext=None):
        """
        Create a new unmanaged Testenum:default. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Testenum_default, self).__init__(skillID)
        self.skillName = "testenum:default"
        self.name: str = name
        self.Znext: TestEnum = Znext


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
        return SkillState.open(path, mode, [TestEnum, Testenum_last, Testenum_third, Testenum_second, Testenum_default])
