

import os
import unittest
from python.src.restrictionsCore.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_restrictions_restrictionsCore_fail_duplicate(self):
        file = self.tmpFile("duplicate.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            sys_1 = sf.System.make()
            sys_2 = sf.System.make()
            # set fields
            sys_1.setName("Hexadecimal")
            sys_1.setVersion(1.1)

            sys_2.setName("Octal")
            sys_2.setVersion(1.2)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(2, sf.System.staticSize())
            # create objects from file
            sys_1_2 = sf2.System.getByID(sys_1.skillID)
            sys_2_2 = sf2.System.getByID(sys_2.skillID)
            # assert fields
            self.assertEqual(sys_1_2.getName() is not None and sys_1_2.getName(), "Hexadecimal")
            self.assertEqual(sys_1_2.getVersion(), 1.1)

            self.assertEqual(sys_2_2.getName() is not None and sys_2_2.getName(), "Octal")
            self.assertEqual(sys_2_2.getVersion(), 1.2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_restrictionsCore_acc_make(self):
        file = self.tmpFile("make.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            sys = sf.System.make()
            # set fields
            sys.setName("Hexadecimal")
            sys.setVersion(1.1)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.System.staticSize())
            # create objects from file
            sys_2 = sf2.System.getByID(sys.skillID)
            # assert fields
            self.assertEqual(sys_2.getName() is not None and sys_2.getName(), "Hexadecimal")
            self.assertEqual(sys_2.getVersion(), 1.1)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsCore_fail_restrictionsCore_fail_2(self):
        file = self.tmpFile("restrictionsCore_fail_2.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            sys = sf.System.make()
            # set fields
            sys.setName("null")
            sys.setVersion(1.1)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.System.staticSize())
            # create objects from file
            sys_2 = sf2.System.getByID(sys.skillID)
            # assert fields
            self.assertEqual(sys_2.getName() is not None and sys_2.getName(), "null")
            self.assertEqual(sys_2.getVersion(), 1.1)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

