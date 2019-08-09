

import os
import unittest
from python.src.unicode.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_unicode_acc_example(self):
        file = self.tmpFile("example.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            uc = sf.Unicode.make()
            # set fields
            uc.setOne("1")
            uc.setTwo("ö")
            uc.setThree("☢")
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Unicode.staticSize())
            # create objects from file
            uc_2 = sf2.Unicode.getByID(uc.skillID)
            # assert fields
            self.assertEqual(uc_2.getOne() is not None and uc_2.getOne(), "1")
            self.assertEqual(uc_2.getTwo() is not None and uc_2.getTwo(), "ö")
            self.assertEqual(uc_2.getThree() is not None and uc_2.getThree(), "☢")
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

