

import os
import unittest
from python.src.subtypes.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_subtypes_acc_simple(self):
        file = self.tmpFile("simple.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            a = sf.A.make()
            b = sf.B.make()
            c = sf.C.make()
            d = sf.D.make()
            # set fields
            a.setA(a)

            b.setA(a)
            b.setB(b)

            c.setA(a)
            c.setC(c)

            d.setA(a)
            d.setB(b)
            d.setD(d)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.D.staticSize())
            self.assertEqual(1, sf.A.staticSize())
            self.assertEqual(1, sf.C.staticSize())
            self.assertEqual(1, sf.B.staticSize())
            # create objects from file
            a_2 = sf2.A.getByID(a.skillID)
            b_2 = sf2.B.getByID(b.skillID)
            c_2 = sf2.C.getByID(c.skillID)
            d_2 = sf2.D.getByID(d.skillID)
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
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_subtypes_acc_poly(self):
        file = self.tmpFile("poly.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            a = sf.A.make()
            b = sf.B.make()
            c = sf.C.make()
            d = sf.D.make()
            # set fields
            a.setA(d)

            b.setA(d)
            b.setB(d)

            c.setA(d)
            c.setC(c)

            d.setA(d)
            d.setB(d)
            d.setD(d)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.D.staticSize())
            self.assertEqual(1, sf.A.staticSize())
            self.assertEqual(1, sf.C.staticSize())
            self.assertEqual(1, sf.B.staticSize())
            # create objects from file
            a_2 = sf2.A.getByID(a.skillID)
            b_2 = sf2.B.getByID(b.skillID)
            c_2 = sf2.C.getByID(c.skillID)
            d_2 = sf2.D.getByID(d.skillID)
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
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_subtypes_fail_poly_fail_1(self):
        file = self.tmpFile("poly_fail_1.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            a = sf.A.make()
            b = sf.B.make()
            c = sf.C.make()
            d = sf.D.make()
            # set fields
            a.setA(a)

            b.setA(a)
            b.setB(c)

            c.setA(a)
            c.setC(c)

            d.setA(a)
            d.setB(b)
            d.setD(d)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.D.staticSize())
            self.assertEqual(1, sf.A.staticSize())
            self.assertEqual(1, sf.C.staticSize())
            self.assertEqual(1, sf.B.staticSize())
            # create objects from file
            a_2 = sf2.A.getByID(a.skillID)
            b_2 = sf2.B.getByID(b.skillID)
            c_2 = sf2.C.getByID(c.skillID)
            d_2 = sf2.D.getByID(d.skillID)
            # assert fields
            self.assertEqual(a_2.getA(), a_2)

            self.assertEqual(b_2.getA(), a_2)
            self.assertEqual(b_2.getB(), c_2)

            self.assertEqual(c_2.getA(), a_2)
            self.assertEqual(c_2.getC(), c_2)

            self.assertEqual(d_2.getA(), a_2)
            self.assertEqual(d_2.getB(), b_2)
            self.assertEqual(d_2.getD(), d_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_subtypes_fail_poly_fail_2(self):
        file = self.tmpFile("poly_fail_2.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            a = sf.A.make()
            c = sf.C.make()
            # set fields
            a.setA(a)

            c.setA(a)
            c.setC(a)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.A.staticSize())
            self.assertEqual(1, sf.C.staticSize())
            # create objects from file
            a_2 = sf2.A.getByID(a.skillID)
            c_2 = sf2.C.getByID(c.skillID)
            # assert fields
            self.assertEqual(a_2.getA(), a_2)

            self.assertEqual(c_2.getA(), a_2)
            self.assertEqual(c_2.getC(), a_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_subtypes_fail_polyFail(self):
        file = self.tmpFile("polyFail.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            a = sf.A.make()
            b = sf.B.make()
            c = sf.C.make()
            d = sf.D.make()
            # set fields
            a.setA(a)

            b.setA(a)
            b.setB(a)

            c.setA(a)
            c.setC(a)

            d.setA(a)
            d.setB(a)
            d.setD(a)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.D.staticSize())
            self.assertEqual(1, sf.A.staticSize())
            self.assertEqual(1, sf.C.staticSize())
            self.assertEqual(1, sf.B.staticSize())
            # create objects from file
            a_2 = sf2.A.getByID(a.skillID)
            b_2 = sf2.B.getByID(b.skillID)
            c_2 = sf2.C.getByID(c.skillID)
            d_2 = sf2.D.getByID(d.skillID)
            # assert fields
            self.assertEqual(a_2.getA(), a_2)

            self.assertEqual(b_2.getA(), a_2)
            self.assertEqual(b_2.getB(), a_2)

            self.assertEqual(c_2.getA(), a_2)
            self.assertEqual(c_2.getC(), a_2)

            self.assertEqual(d_2.getA(), a_2)
            self.assertEqual(d_2.getB(), a_2)
            self.assertEqual(d_2.getD(), a_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

