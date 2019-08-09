#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from restrictionsCore.internal import SkillState, SkillObject, Mode


class Properties(SkillObject):

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged Properties. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Properties, self).__init__(skillID)
        self.skillName = "properties"
        


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
        return SkillState.open(path, mode, [Properties, System])
