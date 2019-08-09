#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from annotation.internal import SkillState, SkillObject, Mode


class Date(SkillObject):
    """
     A simple date test with known Translation
    """

    def __init__(self, skillID=-1, date=0):
        """
        Create a new unmanaged Date. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Date, self).__init__(skillID)
        self.skillName = "date"
        self.date: int = date

    def getDate(self):
        return self.date

    def setDate(self, value):
        assert isinstance(value, int) or value is None
        self.date = value


class Test(SkillObject):
    """
     Test the implementation of annotations.
    """

    def __init__(self, skillID=-1, f=None):
        """
        Create a new unmanaged Test. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Test, self).__init__(skillID)
        self.skillName = "test"
        self.f: SkillObject = f

    def getF(self):
        return self.f

    def setF(self, value):
        assert isinstance(value, SkillObject) or value is None
        self.f = value


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
        return SkillState.open(path, mode, [Date, Test])
