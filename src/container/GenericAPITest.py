

import os
import unittest
from python.src.container.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_container_fail_fail_long_array(self):
        file = self.tmpFile("fail_long_array.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            cont = sf.Container.make()
            # set fields
            cont.setArr([-1,0,1,2])
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Container.staticSize())
            # create objects from file
            cont_2 = sf2.Container.getByID(cont.skillID)
            # assert fields
            self.assertEqual(cont_2.getArr(), [-1,0,1,2]_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_container_acc_make(self):
        file = self.tmpFile("make.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            cont = sf.Container.make()
            # set fields
            cont.setArr([-1,0,1])
            cont.setS({9, 9, 9})
            cont.setF(self.put(dict(), 'String', ))
            cont.setSomeSet({})
            cont.setVarr([-2,-1,0,1])
            cont.setL([0, 1, 2, 3, 4, 5, 6, 7, 8])
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Container.staticSize())
            # create objects from file
            cont_2 = sf2.Container.getByID(cont.skillID)
            # assert fields
            self.assertEqual(cont_2.getArr(), [-1,0,1]_2)
            self.assertEqual(cont_2.getS() is not None and cont_2.getS(), set(9, 9, 9))
            self.assertEqual(cont_2.getF() is not None and cont_2.getF(), self.put(dict(), 'String_2', _2))
            self.assertEqual(cont_2.getSomeSet() is not None and cont_2.getSomeSet(), set())
            self.assertEqual(cont_2.getVarr(), [-2,-1,0,1]_2)
            self.assertEqual(cont_2.getL() is not None and cont_2.getL(), [0, 1, 2, 3, 4, 5, 6, 7, 8])
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_container_fail_fail_short_array(self):
        file = self.tmpFile("fail_short_array.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            cont = sf.Container.make()
            # set fields
            cont.setArr([-1,0])
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Container.staticSize())
            # create objects from file
            cont_2 = sf2.Container.getByID(cont.skillID)
            # assert fields
            self.assertEqual(cont_2.getArr(), [-1,0]_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

