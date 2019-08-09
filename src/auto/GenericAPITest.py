

import os
import unittest
from python.src.auto.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_auto_acc_some(self):
        file = self.tmpFile("some.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            a = sf.A.make()
            b = sf.B.make()
            c = sf.C.make()
            d = sf.D.make()
            # set fields
            a.setA(a)

            b.setB(b)

            c.setC(c)

            d.setD(None)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.D.staticSize())
            self.assertEqual(1, sf.A.staticSize())
            self.assertEqual(1, sf.C.staticSize())
            self.assertEqual(1, sf.B.staticSize())
            # create objects from file
            a_2 = sf2.A.getByID(a.skillID)
            b_2 = sf2.B.getByID(b.skillID)
            c_2 = sf2.C.getByID(c.skillID)
            d_2 = sf2.D.getByID(d.skillID)
            # assert fields



            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

