#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from user.internal import SkillState, SkillObject, Mode


class User(SkillObject):
    """
     A user has a name and an age.
    """

    def __init__(self, skillID=-1, age=0, name=None):
        """
        Create a new unmanaged User. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(User, self).__init__(skillID)
        self.skillName = "user"
        self.age: int = age
        self.name: str = name

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
        return SkillState.open(path, mode, [User])
