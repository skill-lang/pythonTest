

import os
import unittest
from python.src.unicode.api import *


class ReadJava(unittest.TestCase):
    """
    Tests the file reading capabilities.
    """

    def test_Example(self):
        file = "../../DatenJava/unicode/example.sf"
        sf2 = SkillFile.open(file, Mode.Read, Mode.ReadOnly)
        self.assertEqual(1, sf2.Unicode.staticSize())
        uc_2 = sf2.Unicode.getByID(1)
        self.assertEqual(uc_2.getOne() is not None and uc_2.getOne(), "1")
        self.assertEqual(uc_2.getTwo() is not None and uc_2.getTwo(), "ö")
        self.assertEqual(uc_2.getThree() is not None and uc_2.getThree(), "☢")
        sf2.close()

