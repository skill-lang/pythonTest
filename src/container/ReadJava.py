import os
import unittest

from python.src.common.CommonTest import CommonTest
from python.src.container.api import *


class ReadJava(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """
    def test_Make(self):
        file = "../../DatenJava/container/make.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(1, sf.Container.staticSize())
        # create objects from file
        cont_2 = sf.Container.getByID(1)
        # assert fields
        self.assertEqual(cont_2.getArr(), [-1, 0, 1])
        self.assertEqual(cont_2.getS() is not None and cont_2.getS(), {9, 9, 9})
        self.assertEqual(cont_2.getF() is not None and cont_2.getF(),
                         self.put(dict(), 'String', self.put(self.put(dict(), 2, 1), 3, 1)))
        self.assertEqual(cont_2.getSomeSet() is not None and cont_2.getSomeSet(), set())
        self.assertEqual(cont_2.getVarr(), [-2, -1, 0, 1])
        self.assertEqual(cont_2.getL() is not None and cont_2.getL(), [0, 1, 2, 3, 4, 5, 6, 7, 8])
        # close file
        sf.close()
