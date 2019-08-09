

import os
import unittest
from python.src.age.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_restrictions_age_fail_restr(self):
        file = self.tmpFile("restr.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            one = sf.Age.make()
            # set fields
            one.setAge(-1)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Age.staticSize())
            # create objects from file
            one_2 = sf2.Age.getByID(one.skillID)
            # assert fields
            self.assertEqual(one_2.getAge(), -1)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_age_acc_one(self):
        file = self.tmpFile("one.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            one = sf.Age.make()
            # set fields
            one.setAge(30)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Age.staticSize())
            # create objects from file
            one_2 = sf2.Age.getByID(one.skillID)
            # assert fields
            self.assertEqual(one_2.getAge(), 30)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_age_acc_two(self):
        file = self.tmpFile("two.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            one = sf.Age.make()
            two = sf.Age.make()
            # set fields
            one.setAge(30)

            two.setAge(2)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(2, sf.Age.staticSize())
            # create objects from file
            one_2 = sf2.Age.getByID(one.skillID)
            two_2 = sf2.Age.getByID(two.skillID)
            # assert fields
            self.assertEqual(one_2.getAge(), 30)

            self.assertEqual(two_2.getAge(), 2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

