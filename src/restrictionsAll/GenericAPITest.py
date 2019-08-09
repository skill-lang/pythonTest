

import os
import unittest
from python.src.restrictionsAll.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_restrictions_restrictionsAll_fail_range4(self):
        file = self.tmpFile("range4.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(0)
            rbc.setNegative2(1)
            rbc.setDegrees2(360.0)
            rbc.setPositive2(0)
            rbc.setPositive(0)
            rbc.setDegrees(0.0)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 1)
            self.assertEqual(rbc_2.getDegrees2(), 360)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), 0)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_restrictionsAll_acc_example(self):
        file = self.tmpFile("example.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            op = sf.Operator.make()
            rbc = sf.RangeBoarderCases.make()
            dbc = sf.DefaultBoarderCases.make()
            none_obj = sf.ZNone.make()
            sys_obj = sf.System.make()
            trm = sf.Term.make()
            rp = sf.RegularProperty.make()
            cmnt = sf.Comment.make()
            # set fields
            op.setName("Minus")

            rbc.setNegative(0)
            rbc.setNegative2(0)
            rbc.setDegrees2(360.0)
            rbc.setPositive2(0)
            rbc.setPositive(0)
            rbc.setDegrees(0.0)

            dbc.setSystem(sys_obj)
            dbc.setNopDefault(0)
            dbc.setZNone(none_obj)
            dbc.setFloat(-1.0)
            dbc.setMessage("Hello World!")


            sys_obj.setName("Hexadecimal")
            sys_obj.setVersion(1.1)

            trm.setArguments(["trm",null])
            trm.setOperator(op)


            cmnt.setProperty(sys_obj)
            cmnt.setText("A comment")
            cmnt.setTarget(op)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.DefaultBoarderCases.staticSize())
            self.assertEqual(1, sf.Operator.staticSize())
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            self.assertEqual(1, sf.ZNone.staticSize())
            self.assertEqual(1, sf.Comment.staticSize())
            self.assertEqual(1, sf.RegularProperty.staticSize())
            self.assertEqual(1, sf.Term.staticSize())
            self.assertEqual(1, sf.System.staticSize())
            # create objects from file
            op_2 = sf2.Operator.getByID(op.skillID)
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            dbc_2 = sf2.DefaultBoarderCases.getByID(dbc.skillID)
            none_obj_2 = sf2.ZNone.getByID(none_obj.skillID)
            sys_obj_2 = sf2.System.getByID(sys_obj.skillID)
            trm_2 = sf2.Term.getByID(trm.skillID)
            rp_2 = sf2.RegularProperty.getByID(rp.skillID)
            cmnt_2 = sf2.Comment.getByID(cmnt.skillID)
            # assert fields
            self.assertEqual(op_2.getName() is not None and op_2.getName(), "Minus")

            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 360)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), 0)

            self.assertEqual(dbc_2.getNopDefault(), 0)
            self.assertEqual(dbc_2.getZNone(), none_obj_2)
            self.assertEqual(dbc_2.getFloat(), -1)
            self.assertEqual(dbc_2.getMessage() is not None and dbc_2.getMessage(), "Hello World!")


            self.assertEqual(sys_obj_2.getName() is not None and sys_obj_2.getName(), "Hexadecimal")
            self.assertEqual(sys_obj_2.getVersion(), 1.1)

            self.assertEqual(trm_2.getArguments(), ["trm",null]_2)
            self.assertEqual(trm_2.getOperator(), op_2)


            self.assertEqual(cmnt_2.getProperty(), sys_obj_2)
            self.assertEqual(cmnt_2.getText() is not None and cmnt_2.getText(), "A comment")
            self.assertEqual(cmnt_2.getTarget(), op_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_nonnull(self):
        file = self.tmpFile("nonnull.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            op = sf.Term.make()
            # set fields
            op.setOperator(None)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Term.staticSize())
            # create objects from file
            op_2 = sf2.Term.getByID(op.skillID)
            # assert fields
            self.assertEqual(op_2.getOperator(), null_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_unique(self):
        file = self.tmpFile("unique.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            op_2 = sf.Operator.make()
            op_1 = sf.Operator.make()
            # set fields
            op_2.setName("Minus")

            op_1.setName("Minus")
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(2, sf.Operator.staticSize())
            # create objects from file
            op_2_2 = sf2.Operator.getByID(op_2.skillID)
            op_1_2 = sf2.Operator.getByID(op_1.skillID)
            # assert fields
            self.assertEqual(op_2_2.getName() is not None and op_2_2.getName(), "Minus")

            self.assertEqual(op_1_2.getName() is not None and op_1_2.getName(), "Minus")
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_restrictionsAll_acc_twoSingletons(self):
        file = self.tmpFile("twoSingletons.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            none_1 = sf.ZNone.make()
            none_2 = sf.ZNone.make()
            # set fields

            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(2, sf.ZNone.staticSize())
            # create objects from file
            none_1_2 = sf2.ZNone.getByID(none_1.skillID)
            none_2_2 = sf2.ZNone.getByID(none_2.skillID)
            # assert fields

            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_acc_range7(self):
        file = self.tmpFile("range7.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(0)
            rbc.setNegative2(0)
            rbc.setDegrees2(360.0)
            rbc.setPositive2(0)
            rbc.setPositive(0)
            rbc.setDegrees(0.001)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 360)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), 0.001)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_oneOf(self):
        file = self.tmpFile("oneOf.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rp = sf.RegularProperty.make()
            cmnt = sf.Comment.make()
            # set fields

            cmnt.setProperty(rp)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Comment.staticSize())
            self.assertEqual(1, sf.RegularProperty.staticSize())
            # create objects from file
            rp_2 = sf2.RegularProperty.getByID(rp.skillID)
            cmnt_2 = sf2.Comment.getByID(cmnt.skillID)
            # assert fields

            self.assertEqual(cmnt_2.getProperty(), rp_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_range8(self):
        file = self.tmpFile("range8.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(0)
            rbc.setNegative2(0)
            rbc.setDegrees2(360.1)
            rbc.setPositive2(0)
            rbc.setPositive(0)
            rbc.setDegrees(0.001)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 360.1)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), 0.001)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_range5(self):
        file = self.tmpFile("range5.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(0)
            rbc.setNegative2(0)
            rbc.setDegrees2(360.0)
            rbc.setPositive2(0)
            rbc.setPositive(0)
            rbc.setDegrees(360.0)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 360)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), 360)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_range6(self):
        file = self.tmpFile("range6.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(0)
            rbc.setNegative2(0)
            rbc.setDegrees2(360.0)
            rbc.setPositive2(0)
            rbc.setPositive(0)
            rbc.setDegrees(-0.001)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 360)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), -0.001)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_oneOf2(self):
        file = self.tmpFile("oneOf2.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rp = sf.RegularProperty.make()
            cmnt = sf.Comment.make()
            # set fields

            cmnt.setTarget(rp)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Comment.staticSize())
            self.assertEqual(1, sf.RegularProperty.staticSize())
            # create objects from file
            rp_2 = sf2.RegularProperty.getByID(rp.skillID)
            cmnt_2 = sf2.Comment.getByID(cmnt.skillID)
            # assert fields

            self.assertEqual(cmnt_2.getTarget(), rp_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_range2(self):
        file = self.tmpFile("range2.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(0)
            rbc.setNegative2(0)
            rbc.setDegrees2(360.0)
            rbc.setPositive2(-1)
            rbc.setPositive(0)
            rbc.setDegrees(0.0)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 360)
            self.assertEqual(rbc_2.getPositive2(), -1)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), 0)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_acc_range7b(self):
        file = self.tmpFile("range7b.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(0)
            rbc.setNegative2(0)
            rbc.setDegrees2(0.001)
            rbc.setPositive2(0)
            rbc.setPositive(0)
            rbc.setDegrees(0.001)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 0.001)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), 0.001)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_nonnull2(self):
        file = self.tmpFile("nonnull2.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            cmnt = sf.Comment.make()
            # set fields
            cmnt.setText("null")
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.Comment.staticSize())
            # create objects from file
            cmnt_2 = sf2.Comment.getByID(cmnt.skillID)
            # assert fields
            self.assertEqual(cmnt_2.getText() is not None and cmnt_2.getText(), "null")
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_range3(self):
        file = self.tmpFile("range3.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(1)
            rbc.setNegative2(0)
            rbc.setDegrees2(360.0)
            rbc.setPositive2(0)
            rbc.setPositive(0)
            rbc.setDegrees(0.0)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 1)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 360)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), 0)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_range1(self):
        file = self.tmpFile("range1.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(0)
            rbc.setNegative2(0)
            rbc.setDegrees2(360.0)
            rbc.setPositive2(0)
            rbc.setPositive(-1)
            rbc.setDegrees(0.0)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 360)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), -1)
            self.assertEqual(rbc_2.getDegrees(), 0)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_restrictions_restrictionsAll_fail_range9(self):
        file = self.tmpFile("range9.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            rbc = sf.RangeBoarderCases.make()
            # set fields
            rbc.setNegative(0)
            rbc.setNegative2(0)
            rbc.setDegrees2(0.0)
            rbc.setPositive2(0)
            rbc.setPositive(0)
            rbc.setDegrees(0.001)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.RangeBoarderCases.staticSize())
            # create objects from file
            rbc_2 = sf2.RangeBoarderCases.getByID(rbc.skillID)
            # assert fields
            self.assertEqual(rbc_2.getNegative(), 0)
            self.assertEqual(rbc_2.getNegative2(), 0)
            self.assertEqual(rbc_2.getDegrees2(), 0)
            self.assertEqual(rbc_2.getPositive2(), 0)
            self.assertEqual(rbc_2.getPositive(), 0)
            self.assertEqual(rbc_2.getDegrees(), 0.001)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

