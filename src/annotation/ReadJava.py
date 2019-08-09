import os
import unittest
from python.src.annotation.api import *


class ReadJava(unittest.TestCase):
    """
    Tests the file reading capabilities.
    """
    def test_None(self):
        file = "../../DatenJava/annotation/null.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(1, sf.Test.staticSize())
        # create objects from file
        one = sf.Test.getByID(1)
        # assert fields
        self.assertEqual(one.getF(), None)
        # close file
        sf.close()
