

import os
import unittest
from python.src.floats.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_floats_acc_values(self):
        file = self.tmpFile("values.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            flts = sf.FloatTest.make()
            dbls = sf.DoubleTest.make()
            # set fields
            flts.setZZero(0.0)
            flts.setPi(3.141592653589793)
            flts.setMinusZZero(-0.0)
            flts.setNaN(13.0)
            flts.setTwo(2.0)

            dbls.setZZero(0.0)
            dbls.setPi(3.141592653589793)
            dbls.setMinusZZero(-0.0)
            dbls.setNaN(13.0)
            dbls.setTwo(2.0)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.DoubleTest.staticSize())
            self.assertEqual(1, sf.FloatTest.staticSize())
            # create objects from file
            flts_2 = sf2.FloatTest.getByID(flts.skillID)
            dbls_2 = sf2.DoubleTest.getByID(dbls.skillID)
            # assert fields
            self.assertEqual(flts_2.getZZero(), 0)
            self.assertEqual(flts_2.getPi(), 3.141592653589793)
            self.assertEqual(flts_2.getMinusZZero(), -0.0)
            self.assertEqual(flts_2.getNaN(), 13)
            self.assertEqual(flts_2.getTwo(), 2)

            self.assertEqual(dbls_2.getZZero(), 0)
            self.assertEqual(dbls_2.getPi(), 3.141592653589793)
            self.assertEqual(dbls_2.getMinusZZero(), -0.0)
            self.assertEqual(dbls_2.getNaN(), 13)
            self.assertEqual(dbls_2.getTwo(), 2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

