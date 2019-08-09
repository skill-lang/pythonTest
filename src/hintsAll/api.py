#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from hintsAll.internal import SkillState, SkillObject, Mode


class Abuser(SkillObject):
    """
     Just for fun
    """

    def __init__(self, skillID=-1, abuseDescription=None):
        """
        Create a new unmanaged Abuser. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Abuser, self).__init__(skillID)
        self.skillName = "abuser"
        self.abuseDescription: str = abuseDescription

    def getAbuseDescription(self):
        return self.abuseDescription

    def setAbuseDescription(self, value):
        assert isinstance(value, str) or value is None
        self.abuseDescription = value


class BadType(SkillObject):

    def __init__(self, skillID=-1, ignoredData=None, reflectivelyInVisible=None):
        """
        Create a new unmanaged BadType. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(BadType, self).__init__(skillID)
        self.skillName = "badtype"
        self.ignoredData: str = ignoredData
        self.reflectivelyInVisible: str = reflectivelyInVisible

    def getIgnoredData(self):
        return self.ignoredData

    def setIgnoredData(self, value):
        assert isinstance(value, str) or value is None
        self.ignoredData = value

    def getReflectivelyInVisible(self):
        return self.reflectivelyInVisible

    def setReflectivelyInVisible(self, value):
        assert isinstance(value, str) or value is None
        self.reflectivelyInVisible = value


class Expression(SkillObject):
    """
     all expressions are pure
    """

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged Expression. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Expression, self).__init__(skillID)
        self.skillName = "expression"
        


class ExternMixin(SkillObject):
    """
     A type mixed into our hirarchy.
     @todo  provide tests for programming languages using actual user defined implementations
    """

    def __init__(self, skillID=-1, unknownStuff=None):
        """
        Create a new unmanaged ExternMixin. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(ExternMixin, self).__init__(skillID)
        self.skillName = "externmixin"
        self.unknownStuff: SkillObject = unknownStuff

    def getUnknownStuff(self):
        return self.unknownStuff

    def setUnknownStuff(self, value):
        assert isinstance(value, SkillObject) or value is None
        self.unknownStuff = value


class NowASingleton(SkillObject):
    """
     what ever it was before, now it is a singleton
     @todo  provide a test binary to check this hint (where it should be abstract; and a fail, where it has a subclass,
     because it can not be a singleton in that case)
     @note  this is readOnly; should not matter, because it has no mutable state
    """

    def __init__(self, skillID=-1, guard=0):
        """
        Create a new unmanaged NowASingleton. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(NowASingleton, self).__init__(skillID)
        self.skillName = "nowasingleton"
        

    def getGuard(self):
        return self.guard

    def setGuard(self, value):
        """ Constant field. You cannot set guard """
        raise Exception("You are not allowed to set guard")
        


class UID(SkillObject):
    """
     Unique Identifiers are unique and appear as if they were longs
    """

    def __init__(self, skillID=-1, identifier=0):
        """
        Create a new unmanaged UID. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(UID, self).__init__(skillID)
        self.skillName = "uid"
        self.identifier: int = identifier

    def getIdentifier(self):
        return self.identifier

    def setIdentifier(self, value):
        assert isinstance(value, int) or value is None
        self.identifier = value


class User(SkillObject):
    """
     A user has a name and an age.
    """

    def __init__(self, skillID=-1, age=0, name=None, reflectivelyVisible=None):
        """
        Create a new unmanaged User. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(User, self).__init__(skillID)
        self.skillName = "user"
        self.age: int = age
        self.name: str = name
        self.reflectivelyVisible: str = reflectivelyVisible

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

    def getReflectivelyVisible(self):
        return self.reflectivelyVisible

    def setReflectivelyVisible(self, value):
        assert isinstance(value, str) or value is None
        self.reflectivelyVisible = value


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
        return SkillState.open(path, mode, [Abuser, BadType, Expression, ExternMixin, NowASingleton, UID, User])
