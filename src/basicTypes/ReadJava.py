import os
import unittest
from python.src.basicTypes.api import *
from python.src.common.CommonTest import CommonTest


class ReadJava(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """
    def test_All(self):
        file = "../../DatenJava/basicTypes/all.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(1, sf.BasicInt32.staticSize())
        self.assertEqual(1, sf.BasicIntegers.staticSize())
        self.assertEqual(1, sf.BasicFloat64.staticSize())
        self.assertEqual(1, sf.BasicFloats.staticSize())
        self.assertEqual(1, sf.BasicBool.staticSize())
        self.assertEqual(1, sf.BasicInt64V.staticSize())
        self.assertEqual(1, sf.BasicInt16.staticSize())
        self.assertEqual(1, sf.BasicString.staticSize())
        self.assertEqual(1, sf.BasicInt64I.staticSize())
        self.assertEqual(1, sf.BasicTypes.staticSize())
        self.assertEqual(1, sf.BasicInt8.staticSize())
        self.assertEqual(1, sf.BasicFloat32.staticSize())
        # create objects from file
        all_2 = sf.BasicTypes.getByID(1)
        all_aUserType_obj_int64I_obj_2 = sf.BasicInt64I.getByID(1)
        all_anotherUserType_obj_2 = sf.BasicFloats.getByID(1)
        all_aUserType_obj_2 = sf.BasicIntegers.getByID(1)
        all_aUserType_obj_int32_obj_2 = sf.BasicInt32.getByID(1)
        all_anotherUserType_obj_float32_obj_2 = sf.BasicFloat32.getByID(1)
        all_aUserType_obj_int64V_obj_2 = sf.BasicInt64V.getByID(1)
        all_anotherUserType_obj_float64_obj_2 = sf.BasicFloat64.getByID(1)
        all_aUserType_obj_int8_obj_2 = sf.BasicInt8.getByID(1)
        all_aUserType_obj_int16_obj_2 = sf.BasicInt16.getByID(1)
        all_aBool_obj_2 = sf.BasicBool.getByID(1)
        all_aString_obj_2 = sf.BasicString.getByID(1)
        # assert fields
        self.assertEqual(all_2.getAUserType(), all_aUserType_obj_2)
        self.assertEqual(all_2.getAString(), all_aString_obj_2)
        self.assertEqual(all_2.getAList() is not None and all_2.getAList(), [3.0, 4.0])
        self.assertEqual(all_2.getAMap() is not None and all_2.getAMap(), self.put(dict(), 5, 6))

        #    self.assertEqual(all_2.getAnArray(), [all_aUserType_obj])
        self.assertEqual(all_2.getAnAnnotation(), all_aBool_obj_2)
        self.assertEqual(all_2.getAnotherUserType(), all_anotherUserType_obj_2)
        self.assertEqual(all_2.getASet() is not None and all_2.getASet(), {2})
        self.assertEqual(all_2.getABool(), all_aBool_obj_2)

        self.assertEqual(all_aUserType_obj_int64I_obj_2.getBasicInt(), 0)

        self.assertEqual(all_anotherUserType_obj_2.getFloat32(), all_anotherUserType_obj_float32_obj_2)
        self.assertEqual(all_anotherUserType_obj_2.getFloat64(), all_anotherUserType_obj_float64_obj_2)

        self.assertEqual(all_aUserType_obj_2.getInt32(), all_aUserType_obj_int32_obj_2)
        self.assertEqual(all_aUserType_obj_2.getInt8(), all_aUserType_obj_int8_obj_2)
        self.assertEqual(all_aUserType_obj_2.getInt64V(), all_aUserType_obj_int64V_obj_2)
        self.assertEqual(all_aUserType_obj_2.getInt64I(), all_aUserType_obj_int64I_obj_2)
        self.assertEqual(all_aUserType_obj_2.getInt16(), all_aUserType_obj_int16_obj_2)

        self.assertEqual(all_aUserType_obj_int32_obj_2.getBasicInt(), -1)

        self.assertEqual(all_anotherUserType_obj_float32_obj_2.getBasicFloat(), 1)

        self.assertEqual(all_aUserType_obj_int64V_obj_2.getBasicInt(), 1)

        self.assertEqual(all_anotherUserType_obj_float64_obj_2.getBasicFloat(), 2)

        self.assertEqual(all_aUserType_obj_int8_obj_2.getBasicInt(), -3)

        self.assertEqual(all_aUserType_obj_int16_obj_2.getBasicInt(), -2)

        self.assertEqual(all_aBool_obj_2.getBasicBool(), True)

        self.assertEqual(all_aString_obj_2.getBasicString() is not None and all_aString_obj_2.getBasicString(),
                         "Hello World!")
        # close file
        sf.close()

    def test_Roland(self):
        file = "../../DatenJava/basicTypes/roland.sf"
        sf = SkillFile.open(file, Mode.ReadOnly)
        # check count per Type
        self.assertEqual(30, sf.BasicInt64V.staticSize())
        # create objects from file
        v_0_b_2 = sf.BasicInt64V.getByID(1)
        v_1_a_2 = sf.BasicInt64V.getByID(2)
        v_0_c_2 = sf.BasicInt64V.getByID(3)
        v_1_b_2 = sf.BasicInt64V.getByID(4)
        v_2_a_2 = sf.BasicInt64V.getByID(5)
        v_0_a_2 = sf.BasicInt64V.getByID(6)
        v_3_c_2 = sf.BasicInt64V.getByID(7)
        v_4_b_2 = sf.BasicInt64V.getByID(8)
        v_5_a_2 = sf.BasicInt64V.getByID(9)
        v_4_c_2 = sf.BasicInt64V.getByID(10)
        v_5_b_2 = sf.BasicInt64V.getByID(11)
        v_6_a_2 = sf.BasicInt64V.getByID(12)
        v_1_c_2 = sf.BasicInt64V.getByID(13)
        v_2_b_2 = sf.BasicInt64V.getByID(14)
        v_3_a_2 = sf.BasicInt64V.getByID(15)
        v_2_c_2 = sf.BasicInt64V.getByID(16)
        v_3_b_2 = sf.BasicInt64V.getByID(17)
        v_4_a_2 = sf.BasicInt64V.getByID(18)
        v_7_c_2 = sf.BasicInt64V.getByID(19)
        v_8_b_2 = sf.BasicInt64V.getByID(20)
        v_9_a_2 = sf.BasicInt64V.getByID(21)
        v_8_c_2 = sf.BasicInt64V.getByID(22)
        v_9_b_2 = sf.BasicInt64V.getByID(23)
        v_5_c_2 = sf.BasicInt64V.getByID(24)
        v_6_b_2 = sf.BasicInt64V.getByID(25)
        v_7_a_2 = sf.BasicInt64V.getByID(26)
        v_6_c_2 = sf.BasicInt64V.getByID(27)
        v_7_b_2 = sf.BasicInt64V.getByID(28)
        v_8_a_2 = sf.BasicInt64V.getByID(29)
        v_9_c_2 = sf.BasicInt64V.getByID(30)
        # assert fields
        self.assertEqual(v_0_b_2.getBasicInt(), 0)

        self.assertEqual(v_1_a_2.getBasicInt(), 129)

        self.assertEqual(v_0_c_2.getBasicInt(), -1)

        self.assertEqual(v_1_b_2.getBasicInt(), 128)

        self.assertEqual(v_2_a_2.getBasicInt(), 16385)

        self.assertEqual(v_0_a_2.getBasicInt(), 1)

        self.assertEqual(v_3_c_2.getBasicInt(), 2097151)

        self.assertEqual(v_4_b_2.getBasicInt(), 268435456)

        self.assertEqual(v_5_a_2.getBasicInt(), 34359738369)

        self.assertEqual(v_4_c_2.getBasicInt(), 268435455)

        self.assertEqual(v_5_b_2.getBasicInt(), 34359738368)

        self.assertEqual(v_6_a_2.getBasicInt(), 4398046511105)

        self.assertEqual(v_1_c_2.getBasicInt(), 127)

        self.assertEqual(v_2_b_2.getBasicInt(), 16384)

        self.assertEqual(v_3_a_2.getBasicInt(), 2097153)

        self.assertEqual(v_2_c_2.getBasicInt(), 16383)

        self.assertEqual(v_3_b_2.getBasicInt(), 2097152)

        self.assertEqual(v_4_a_2.getBasicInt(), 268435457)

        self.assertEqual(v_7_c_2.getBasicInt(), 562949953421311)

        self.assertEqual(v_8_b_2.getBasicInt(), 72057594037927936)

        self.assertEqual(v_9_a_2.getBasicInt(), -9223372036854775807)

        self.assertEqual(v_8_c_2.getBasicInt(), 72057594037927935)

        self.assertEqual(v_9_b_2.getBasicInt(), -9223372036854775808)

        self.assertEqual(v_5_c_2.getBasicInt(), 34359738367)

        self.assertEqual(v_6_b_2.getBasicInt(), 4398046511104)

        self.assertEqual(v_7_a_2.getBasicInt(), 562949953421313)

        self.assertEqual(v_6_c_2.getBasicInt(), 4398046511103)

        self.assertEqual(v_7_b_2.getBasicInt(), 562949953421312)

        self.assertEqual(v_8_a_2.getBasicInt(), 72057594037927937)

        self.assertEqual(v_9_c_2.getBasicInt(), 9223372036854775807)
        # close file
        sf.close()
