import os
import unittest
from python.src.constants.api import *


class ReadJava(unittest.TestCase):
    """
    Tests the file reading capabilities.
    """
    def test_None(self):
        file = "../../DatenJava/constants/make.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(1, sf.Constant.staticSize())
        # create objects from file
        consts_2 = sf.Constant.getByID(1)
        # assert fields
        # close file
        sf.close()
