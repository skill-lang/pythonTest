

import os
import unittest
from python.src.constants.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_constants_acc_make(self):
        file = self.tmpFile("make.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            consts = sf.Constant.make()
            # set fields
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Constant.staticSize())
            # create objects from file
            consts_2 = sf2.Constant.getByID(consts.skillID)
            # assert fields
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

