import os
import unittest
from python.src.subtypes.api import *


class ReadJava(unittest.TestCase):
    """
    Tests the file reading capabilities.
    """
    def test_Poly(self):
        file = "../../DatenJava/subtypes/poly.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(1, sf.D.staticSize())
        self.assertEqual(1, sf.A.staticSize())
        self.assertEqual(1, sf.C.staticSize())
        self.assertEqual(1, sf.B.staticSize())
        # create objects from file
        a_2 = sf.A.getByID(1)
        b_2 = sf.B.getByID(2)
        c_2 = sf.C.getByID(4)
        d_2 = sf.D.getByID(3)
        # assert fields
        self.assertEqual(a_2.getA(), d_2)

        self.assertEqual(b_2.getA(), d_2)
        self.assertEqual(b_2.getB(), d_2)

        self.assertEqual(c_2.getA(), d_2)
        self.assertEqual(c_2.getC(), c_2)

        self.assertEqual(d_2.getA(), d_2)
        self.assertEqual(d_2.getB(), d_2)
        self.assertEqual(d_2.getD(), d_2)
        # close file
        sf.close()

    def test_simple(self):
        file = "../../DatenJava/subtypes/simple.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(1, sf.D.staticSize())
        self.assertEqual(1, sf.A.staticSize())
        self.assertEqual(1, sf.C.staticSize())
        self.assertEqual(1, sf.B.staticSize())
        # create objects from file
        a_2 = sf.A.getByID(1)
        b_2 = sf.B.getByID(2)
        c_2 = sf.C.getByID(4)
        d_2 = sf.D.getByID(3)
        # assert fields
        self.assertEqual(a_2.getA(), a_2)

        self.assertEqual(b_2.getA(), a_2)
        self.assertEqual(b_2.getB(), b_2)

        self.assertEqual(c_2.getA(), a_2)
        self.assertEqual(c_2.getC(), c_2)

        self.assertEqual(d_2.getA(), a_2)
        self.assertEqual(d_2.getB(), b_2)
        self.assertEqual(d_2.getD(), d_2)
        # close file
        sf.close()
