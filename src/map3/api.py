#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from map3.internal import SkillState, SkillObject, Mode


class L(SkillObject):

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged L. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(L, self).__init__(skillID)
        self.skillName = "l"
        


class T(SkillObject):

    def __init__(self, skillID=-1, ref=None):
        """
        Create a new unmanaged T. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(T, self).__init__(skillID)
        self.skillName = "t"
        self.ref: dict = ref

    def getRef(self):
        return self.ref

    def setRef(self, value):
        assert isinstance(value, dict) or value is None
        self.ref = value


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
        return SkillState.open(path, mode, [L, T])
