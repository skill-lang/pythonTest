

import os
import unittest
from python.src.graph.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_graph_acc_null(self):
        file = self.tmpFile("null.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            nd = sf.Node.make()
            # set fields
            nd.setColor("null")
            nd.setEdges({null})
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Node.staticSize())
            # create objects from file
            nd_2 = sf2.Node.getByID(nd.skillID)
            # assert fields
            self.assertEqual(nd_2.getColor() is not None and nd_2.getColor(), "null")
            self.assertEqual(nd_2.getEdges() is not None and nd_2.getEdges(), set(null))
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_graph_acc_small(self):
        file = self.tmpFile("small.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            nd_2 = sf.Node.make()
            nd_1 = sf.Node.make()
            # set fields
            nd_2.setColor("blue")
            nd_2.setEdges({})

            nd_1.setColor("red")
            nd_1.setEdges({nd_2})
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(2, sf.Node.staticSize())
            # create objects from file
            nd_2_2 = sf2.Node.getByID(nd_2.skillID)
            nd_1_2 = sf2.Node.getByID(nd_1.skillID)
            # assert fields
            self.assertEqual(nd_2_2.getColor() is not None and nd_2_2.getColor(), "blue")
            self.assertEqual(nd_2_2.getEdges() is not None and nd_2_2.getEdges(), set())

            self.assertEqual(nd_1_2.getColor() is not None and nd_1_2.getColor(), "red")
            self.assertEqual(nd_1_2.getEdges() is not None and nd_1_2.getEdges(), set(nd_2))
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_graph_acc_penta(self):
        file = self.tmpFile("penta.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            n1 = sf.Node.make()
            n2 = sf.Node.make()
            n3 = sf.Node.make()
            n4 = sf.Node.make()
            n5 = sf.Node.make()
            # set fields
            n1.setColor("black")
            n1.setEdges({n1, n2, n3, n4, n5})

            n2.setColor("schwarz")
            n2.setEdges({n1, n2, n3, n4, n5})

            n3.setColor("niger")
            n3.setEdges({n1, n2, n3, n4, n5})

            n4.setColor("noir")
            n4.setEdges({n1, n2, n3, n4, n5})

            n5.setColor("negro")
            n5.setEdges({n1, n2, n3, n4, n5})
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(5, sf.Node.staticSize())
            # create objects from file
            n1_2 = sf2.Node.getByID(n1.skillID)
            n2_2 = sf2.Node.getByID(n2.skillID)
            n3_2 = sf2.Node.getByID(n3.skillID)
            n4_2 = sf2.Node.getByID(n4.skillID)
            n5_2 = sf2.Node.getByID(n5.skillID)
            # assert fields
            self.assertEqual(n1_2.getColor() is not None and n1_2.getColor(), "black")
            self.assertEqual(n1_2.getEdges() is not None and n1_2.getEdges(), set(n1, n2, n3, n4, n5))

            self.assertEqual(n2_2.getColor() is not None and n2_2.getColor(), "schwarz")
            self.assertEqual(n2_2.getEdges() is not None and n2_2.getEdges(), set(n1, n2, n3, n4, n5))

            self.assertEqual(n3_2.getColor() is not None and n3_2.getColor(), "niger")
            self.assertEqual(n3_2.getEdges() is not None and n3_2.getEdges(), set(n1, n2, n3, n4, n5))

            self.assertEqual(n4_2.getColor() is not None and n4_2.getColor(), "noir")
            self.assertEqual(n4_2.getEdges() is not None and n4_2.getEdges(), set(n1, n2, n3, n4, n5))

            self.assertEqual(n5_2.getColor() is not None and n5_2.getColor(), "negro")
            self.assertEqual(n5_2.getEdges() is not None and n5_2.getEdges(), set(n1, n2, n3, n4, n5))
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

