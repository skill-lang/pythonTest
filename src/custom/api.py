#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from custom.internal import SkillState, SkillObject, Mode


class Basis(SkillObject):

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged Basis. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Basis, self).__init__(skillID)
        self.skillName = "basis"
        


class Custom(Basis):
    """
     Demonstration of the capabilities of custom fields.
     @note  Despite the appearance in the specification, for any given language, the Type has at most one field.
    """

    def __init__(self, skillID=-1):
        """
        Create a new unmanaged Custom. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Custom, self).__init__(skillID)
        self.skillName = "custom"
        


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
        return SkillState.open(path, mode, [Basis, Custom])
