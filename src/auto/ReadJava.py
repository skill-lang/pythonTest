import os
import unittest
from python.src.auto.api import *


class ReadJava(unittest.TestCase):
    """
    Tests the file reading capabilities.
    """
    def test_Some(self):
        file = "../../DatenJava/auto/some.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(1, sf.D.staticSize())
        self.assertEqual(1, sf.A.staticSize())
        self.assertEqual(1, sf.C.staticSize())
        self.assertEqual(1, sf.B.staticSize())
        # create objects from file
        a_2 = sf.A.getByID(1)
        b_2 = sf.B.getByID(2)
        c_2 = sf.C.getByID(3)
        d_2 = sf.D.getByID(4)
        # assert fields
        # close file
        sf.close()
