#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from constants.internal import SkillState, SkillObject, Mode


class Constant(SkillObject):
    """
     Check for constant integerers.
     @author  Dennis Przytarski
    """

    def __init__(self, skillID=-1, a=0, b=0, c=0, d=0, e=0):
        """
        Create a new unmanaged Constant. Allocation of objects without using the
        access factory method is discouraged.
        :param: Used for internal construction only!
        """
        super(Constant, self).__init__(skillID)
        self.skillName = "constant"
        

    def getA(self):
        return self.a

    def setA(self, value):
        """ Constant field. You cannot set a """
        raise Exception("You are not allowed to set a")
        

    def getB(self):
        return self.b

    def setB(self, value):
        """ Constant field. You cannot set b """
        raise Exception("You are not allowed to set b")
        

    def getC(self):
        return self.c

    def setC(self, value):
        """ Constant field. You cannot set c """
        raise Exception("You are not allowed to set c")
        

    def getD(self):
        return self.d

    def setD(self, value):
        """ Constant field. You cannot set d """
        raise Exception("You are not allowed to set d")
        

    def getE(self):
        return self.e

    def setE(self, value):
        """ Constant field. You cannot set e """
        raise Exception("You are not allowed to set e")
        


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
        return SkillState.open(path, mode, [Constant])
