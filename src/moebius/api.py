#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from moebius.internal import SkillState, SkillObject, Mode


class Ä(SkillObject):

    def __init__(self, skillID=-1, ö=None):
        """
        Create a new unmanaged Ä. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Ä, self).__init__(skillID)
        self.skillName = "ä"
        self.ö: Ö = ö

    def getÖ(self):
        return self.ö

    def setÖ(self, value):
        assert isinstance(value, Ö) or value is None
        self.ö = value


class Ö(SkillObject):

    def __init__(self, skillID=-1, ä=None):
        """
        Create a new unmanaged Ö. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Ö, self).__init__(skillID)
        self.skillName = "ö"
        self.ä: Ä = ä

    def getÄ(self):
        return self.ä

    def setÄ(self, value):
        assert isinstance(value, Ä) or value is None
        self.ä = value


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
        return SkillState.open(path, mode, [Ä, Ö])
