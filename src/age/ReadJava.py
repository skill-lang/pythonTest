

import os
import unittest
from python.src.age.api import *


class ReadJava(unittest.TestCase):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_age_acc_one(self):
        file = "../../DatenJava/age/one.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(1, sf.Age.staticSize())
        # create objects from file
        one = sf.Age.getByID(1)
        # assert fields
        self.assertEqual(one.getAge(), 30)
        # close file
        sf.close()

    def test_API_core_age_acc_two(self):
        file = "../../DatenJava/age/two.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(2, sf.Age.staticSize())
        # create objects from file
        one = sf.Age.getByID(1)
        two = sf.Age.getByID(2)
        # assert fields
        self.assertEqual(one.getAge(), 30)
        self.assertEqual(two.getAge(), 2)
        # close file
        sf.close()

