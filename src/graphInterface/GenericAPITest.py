

import os
import unittest
from python.src.graphInterface.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_interfaces_graphInterface_acc_succ_1(self):
        file = self.tmpFile("succ_1.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            ch = sf.ColorHolder.make()
            sn = sf.SubNode.make()
            n = sf.Node.make()
            # set fields
            ch.setAnAbstractNode(n)
            ch.setAnAnnotation(None)

            sn.setNext(None)
            sn.setColor("red")
            sn.setF(None)
            sn.setEdges({n})
            sn.setMap(self.put(dict(), 'n', ))
            sn.setMark("Cirlce")
            sn.setN(n)

            n.setNext(None)
            n.setColor("blue")
            n.setEdges({})
            n.setMap(self.put(dict(), 'n', ))
            n.setMark("Circle")
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.SubNode.staticSize())
            self.assertEqual(1, sf.Node.staticSize())
            self.assertEqual(1, sf.ColorHolder.staticSize())
            # create objects from file
            ch_2 = sf2.ColorHolder.getByID(ch.skillID)
            sn_2 = sf2.SubNode.getByID(sn.skillID)
            n_2 = sf2.Node.getByID(n.skillID)
            # assert fields
            self.assertEqual(ch_2.getAnAbstractNode(), n_2)
            self.assertEqual(ch_2.getAnAnnotation(), null_2)

            self.assertEqual(sn_2.getNext(), null_2)
            self.assertEqual(sn_2.getColor() is not None and sn_2.getColor(), "red")
            self.assertEqual(sn_2.getF(), null_2)
            self.assertEqual(sn_2.getEdges() is not None and sn_2.getEdges(), set(n))
            self.assertEqual(sn_2.getMap() is not None and sn_2.getMap(), self.put(dict(), 'n_2', _2))
            self.assertEqual(sn_2.getMark() is not None and sn_2.getMark(), "Cirlce")
            self.assertEqual(sn_2.getN(), n_2)

            self.assertEqual(n_2.getNext(), null_2)
            self.assertEqual(n_2.getColor() is not None and n_2.getColor(), "blue")
            self.assertEqual(n_2.getEdges() is not None and n_2.getEdges(), set())
            self.assertEqual(n_2.getMap() is not None and n_2.getMap(), self.put(dict(), 'n_2', _2))
            self.assertEqual(n_2.getMark() is not None and n_2.getMark(), "Circle")
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_interfaces_graphInterface_fail_fail_1(self):
        file = self.tmpFile("fail_1.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            ch = sf.ColorHolder.make()
            sn = sf.SubNode.make()
            # set fields

            sn.setNext(ch)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.SubNode.staticSize())
            self.assertEqual(1, sf.ColorHolder.staticSize())
            # create objects from file
            ch_2 = sf2.ColorHolder.getByID(ch.skillID)
            sn_2 = sf2.SubNode.getByID(sn.skillID)
            # assert fields

            self.assertEqual(sn_2.getNext(), ch_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

