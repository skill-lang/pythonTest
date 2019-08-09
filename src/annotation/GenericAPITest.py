

import os
import unittest
from python.src.annotation.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_annotation_acc_null(self):
        file = self.tmpFile("null.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            tst = sf.Test.make()
            # set fields
            tst.setF(None)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Test.staticSize())
            # create objects from file
            tst_2 = sf2.Test.getByID(tst.skillID)
            # assert fields
            self.assertEqual(tst_2.getF(), null)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

