

import os
import unittest
from python.src.escaping.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_escaped_escaping_acc_instances(self):
        file = self.tmpFile("instances.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            esc_1 = sf.Int.make()
            esc_3 = sf.Boolean.make()
            esc_2 = sf.If.make()
            esc_4 = sf.Z2200.make()
            # set fields
            esc_1.setFor(esc_2)
            esc_1.setIf(esc_1)

            esc_3.setBoolean(true)
            esc_3.setBool(esc_3)


            esc_4.setZ2622("Hello, World!")
            esc_4.seteuro(esc_4)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Int.staticSize())
            self.assertEqual(1, sf.If.staticSize())
            self.assertEqual(1, sf.Boolean.staticSize())
            self.assertEqual(1, sf.Z2200.staticSize())
            # create objects from file
            esc_1_2 = sf2.Int.getByID(esc_1.skillID)
            esc_3_2 = sf2.Boolean.getByID(esc_3.skillID)
            esc_2_2 = sf2.If.getByID(esc_2.skillID)
            esc_4_2 = sf2.Z2200.getByID(esc_4.skillID)
            # assert fields
            self.assertEqual(esc_1_2.getFor(), esc_2_2)
            self.assertEqual(esc_1_2.getIf(), esc_1_2)

            self.assertEqual(esc_3_2.getBoolean(), true)
            self.assertEqual(esc_3_2.getBool(), esc_3_2)


            self.assertEqual(esc_4_2.getZ2622() is not None and esc_4_2.getZ2622(), "Hello, World!")
            self.assertEqual(esc_4_2.geteuro(), esc_4_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_escaped_escaping_acc_escaping_succ_1(self):
        file = self.tmpFile("escaping_succ_1.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            esc_1 = sf.Int.make()
            esc_3 = sf.Boolean.make()
            esc_2 = sf.If.make()
            esc_4 = sf.Z2200.make()
            # set fields
            esc_1.setFor(esc_2)
            esc_1.setIf(esc_1)

            esc_3.setBoolean(true)
            esc_3.setBool(esc_3)


            esc_4.setZ2622("Hello, World!")
            esc_4.seteuro(esc_4)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Int.staticSize())
            self.assertEqual(1, sf.If.staticSize())
            self.assertEqual(1, sf.Boolean.staticSize())
            self.assertEqual(1, sf.Z2200.staticSize())
            # create objects from file
            esc_1_2 = sf2.Int.getByID(esc_1.skillID)
            esc_3_2 = sf2.Boolean.getByID(esc_3.skillID)
            esc_2_2 = sf2.If.getByID(esc_2.skillID)
            esc_4_2 = sf2.Z2200.getByID(esc_4.skillID)
            # assert fields
            self.assertEqual(esc_1_2.getFor(), esc_2_2)
            self.assertEqual(esc_1_2.getIf(), esc_1_2)

            self.assertEqual(esc_3_2.getBoolean(), true)
            self.assertEqual(esc_3_2.getBool(), esc_3_2)


            self.assertEqual(esc_4_2.getZ2622() is not None and esc_4_2.getZ2622(), "Hello, World!")
            self.assertEqual(esc_4_2.geteuro(), esc_4_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_escaped_escaping_fail_Boolean(self):
        file = self.tmpFile("Boolean.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            esc_3 = sf.Boolean.make()
            # set fields
            esc_3.setBoolean(esc_3)
            esc_3.setBool(esc_3)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Boolean.staticSize())
            # create objects from file
            esc_3_2 = sf2.Boolean.getByID(esc_3.skillID)
            # assert fields
            self.assertEqual(esc_3_2.getBoolean(), esc_3_2)
            self.assertEqual(esc_3_2.getBool(), esc_3_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_escaped_escaping_fail_Zbool(self):
        file = self.tmpFile("bool.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            esc_3 = sf.Boolean.make()
            # set fields
            esc_3.setBoolean(true)
            esc_3.setBool(true)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Boolean.staticSize())
            # create objects from file
            esc_3_2 = sf2.Boolean.getByID(esc_3.skillID)
            # assert fields
            self.assertEqual(esc_3_2.getBoolean(), true)
            self.assertEqual(esc_3_2.getBool(), true_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

