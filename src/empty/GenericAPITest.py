

import os
import unittest
from python.src.empty.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_empty_acc_empty(self):
        file = self.tmpFile("empty.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            # set fields
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            # create objects from file
            # assert fields
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

