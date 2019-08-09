#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from age.internal import SkillState, SkillObject, Mode


class Age(SkillObject):
    """
     The age of a person.
     @author  Timm Felden
    """

    def __init__(self, skillID=-1, age=0):
        """
        Create a new unmanaged Age. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Age, self).__init__(skillID)
        self.skillName = "age"
        self.age: int = age

    def getAge(self):
        return self.age

    def setAge(self, value):
        assert isinstance(value, int) or value is None
        self.age = value


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
        return SkillState.open(path, mode, [Age])
