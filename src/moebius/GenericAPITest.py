

import os
import unittest
from python.src.moebius.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_moebius_acc_two(self):
        file = self.tmpFile("two.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            ä = sf.Ä.make()
            ö = sf.Ö.make()
            # set fields
            ä.setÖ(ö)

            ö.setÄ(ä)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Ö.staticSize())
            self.assertEqual(1, sf.Ä.staticSize())
            # create objects from file
            ä_2 = sf2.Ä.getByID(ä.skillID)
            ö_2 = sf2.Ö.getByID(ö.skillID)
            # assert fields
            self.assertEqual(ä_2.getÖ(), ö_2)

            self.assertEqual(ö_2.getÄ(), ä_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

