

import os
import unittest
from python.src.map3.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_map3_acc_simple(self):
        file = self.tmpFile("simple.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            T = sf.T.make()
            # set fields
            T.setRef(self.put(dict(), 'hallo', ))
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.T.staticSize())
            # create objects from file
            T_2 = sf2.T.getByID(T.skillID)
            # assert fields
            self.assertEqual(T_2.getRef() is not None and T_2.getRef(), self.put(dict(), 'hallo_2', _2))
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

