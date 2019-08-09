

import os
import unittest
from python.src.number.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_number_acc_numbers(self):
        file = self.tmpFile("numbers.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            n = sf.Number.make()
            # set fields
            n.setNumber(1234567)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Number.staticSize())
            # create objects from file
            n_2 = sf2.Number.getByID(n.skillID)
            # assert fields
            self.assertEqual(n_2.getNumber(), 1234567)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

