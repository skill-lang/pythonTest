

import os
import unittest
from python.src.unknown.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_unknown_acc_partial(self):
        file = self.tmpFile("partial.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            a = sf.A.make()
            c = sf.C.make()
            # set fields
            a.setA(a)

            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.A.staticSize())
            self.assertEqual(1, sf.C.staticSize())
            # create objects from file
            a_2 = sf2.A.getByID(a.skillID)
            c_2 = sf2.C.getByID(c.skillID)
            # assert fields
            self.assertEqual(a_2.getA(), a_2)

            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_unknown_acc_full(self):
        file = self.tmpFile("full.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            a = sf.A.make()
            c = sf.C.make()
            # set fields
            a.setA(a)

            c.setA(a)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.A.staticSize())
            self.assertEqual(1, sf.C.staticSize())
            # create objects from file
            a_2 = sf2.A.getByID(a.skillID)
            c_2 = sf2.C.getByID(c.skillID)
            # assert fields
            self.assertEqual(a_2.getA(), a_2)

            self.assertEqual(c_2.getA(), a_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

