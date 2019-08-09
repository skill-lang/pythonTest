

import os
import unittest
from python.src.custom.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_custom_acc_customFields_succ_1(self):
        file = self.tmpFile("customFields_succ_1.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            c = sf.Custom.make()
            # set fields
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Custom.staticSize())
            # create objects from file
            c_2 = sf2.Custom.getByID(c.skillID)
            # assert fields
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

