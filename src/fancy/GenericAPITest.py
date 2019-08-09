

import os
import unittest
from python.src.fancy.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_fancy_acc_fancy(self):
        file = self.tmpFile("fancy.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            d = sf.D.make()
            g = sf.G.make()
            # set fields
            d.setParent(d)
            d.setValue(d)

            g.setParent(d)
            g.setAMap(self.put(dict(), 'g', ))
            g.setValue(g)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.D.staticSize())
            self.assertEqual(1, sf.G.staticSize())
            # create objects from file
            d_2 = sf2.D.getByID(d.skillID)
            g_2 = sf2.G.getByID(g.skillID)
            # assert fields
            self.assertEqual(d_2.getParent(), d_2)
            self.assertEqual(d_2.getValue(), d_2)

            self.assertEqual(g_2.getParent(), d_2)
            self.assertEqual(g_2.getAMap() is not None and g_2.getAMap(), self.put(dict(), 'g_2', _2))
            self.assertEqual(g_2.getValue(), g_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

