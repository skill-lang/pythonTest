#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from number.internal import SkillState, SkillObject, Mode


class Number(SkillObject):

    def __init__(self, skillID=-1, number=0):
        """
        Create a new unmanaged Number. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Number, self).__init__(skillID)
        self.skillName = "number"
        self.number: int = number

    def getNumber(self):
        return self.number

    def setNumber(self, value):
        assert isinstance(value, int) or value is None
        self.number = value


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
        return SkillState.open(path, mode, [Number])
