#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from unicode.internal import SkillState, SkillObject, Mode


class Unicode(SkillObject):
    """
     this test is used to check unicode handling inside of strings; only one instance but no
     @singleton  to keep things simple; all fields contain one character.
    """

    def __init__(self, skillID=-1, one=None, three=None, two=None):
        """
        Create a new unmanaged Unicode. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Unicode, self).__init__(skillID)
        self.skillName = "unicode"
        self.one: str = one
        self.three: str = three
        self.two: str = two

    def getOne(self):
        return self.one

    def setOne(self, value):
        assert isinstance(value, str) or value is None
        self.one = value

    def getThree(self):
        return self.three

    def setThree(self, value):
        assert isinstance(value, str) or value is None
        self.three = value

    def getTwo(self):
        return self.two

    def setTwo(self, value):
        assert isinstance(value, str) or value is None
        self.two = value


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
        return SkillState.open(path, mode, [Unicode])
