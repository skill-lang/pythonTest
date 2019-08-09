

import os
import unittest
from python.src.basicTypes.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_basicTypes_acc_Zall(self):
        file = self.tmpFile("all.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            all = sf.BasicTypes.make()
            all_aUserType_obj_int64I_obj = sf.BasicInt64I.make()
            all_anotherUserType_obj = sf.BasicFloats.make()
            all_aUserType_obj = sf.BasicIntegers.make()
            all_aUserType_obj_int32_obj = sf.BasicInt32.make()
            all_anotherUserType_obj_float32_obj = sf.BasicFloat32.make()
            all_aUserType_obj_int64V_obj = sf.BasicInt64V.make()
            all_anotherUserType_obj_float64_obj = sf.BasicFloat64.make()
            all_aUserType_obj_int8_obj = sf.BasicInt8.make()
            all_aUserType_obj_int16_obj = sf.BasicInt16.make()
            all_aBool_obj = sf.BasicBool.make()
            all_aString_obj = sf.BasicString.make()
            # set fields
            all.setAUserType(all_aUserType_obj)
            all.setAString(all_aString_obj)
            all.setAList([3.0, 4.0])
            all.setAMap(self.put(dict(), '5', ))
            all.setAnArray(["all_aUserType_obj"])
            all.setAnAnnotation(all_aBool_obj)
            all.setAnotherUserType(all_anotherUserType_obj)
            all.setASet({2})
            all.setABool(all_aBool_obj)

            all_aUserType_obj_int64I_obj.setBasicInt(0)

            all_anotherUserType_obj.setFloat32(all_anotherUserType_obj_float32_obj)
            all_anotherUserType_obj.setFloat64(all_anotherUserType_obj_float64_obj)

            all_aUserType_obj.setInt32(all_aUserType_obj_int32_obj)
            all_aUserType_obj.setInt8(all_aUserType_obj_int8_obj)
            all_aUserType_obj.setInt64V(all_aUserType_obj_int64V_obj)
            all_aUserType_obj.setInt64I(all_aUserType_obj_int64I_obj)
            all_aUserType_obj.setInt16(all_aUserType_obj_int16_obj)

            all_aUserType_obj_int32_obj.setBasicInt(-1)

            all_anotherUserType_obj_float32_obj.setBasicFloat(1.0)

            all_aUserType_obj_int64V_obj.setBasicInt(1)

            all_anotherUserType_obj_float64_obj.setBasicFloat(2.0)

            all_aUserType_obj_int8_obj.setBasicInt(-3)

            all_aUserType_obj_int16_obj.setBasicInt(-2)

            all_aBool_obj.setBasicBool(true)

            all_aString_obj.setBasicString("Hello World!")
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
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
            all_2 = sf2.BasicTypes.getByID(all.skillID)
            all_aUserType_obj_int64I_obj_2 = sf2.BasicInt64I.getByID(all_aUserType_obj_int64I_obj.skillID)
            all_anotherUserType_obj_2 = sf2.BasicFloats.getByID(all_anotherUserType_obj.skillID)
            all_aUserType_obj_2 = sf2.BasicIntegers.getByID(all_aUserType_obj.skillID)
            all_aUserType_obj_int32_obj_2 = sf2.BasicInt32.getByID(all_aUserType_obj_int32_obj.skillID)
            all_anotherUserType_obj_float32_obj_2 = sf2.BasicFloat32.getByID(all_anotherUserType_obj_float32_obj.skillID)
            all_aUserType_obj_int64V_obj_2 = sf2.BasicInt64V.getByID(all_aUserType_obj_int64V_obj.skillID)
            all_anotherUserType_obj_float64_obj_2 = sf2.BasicFloat64.getByID(all_anotherUserType_obj_float64_obj.skillID)
            all_aUserType_obj_int8_obj_2 = sf2.BasicInt8.getByID(all_aUserType_obj_int8_obj.skillID)
            all_aUserType_obj_int16_obj_2 = sf2.BasicInt16.getByID(all_aUserType_obj_int16_obj.skillID)
            all_aBool_obj_2 = sf2.BasicBool.getByID(all_aBool_obj.skillID)
            all_aString_obj_2 = sf2.BasicString.getByID(all_aString_obj.skillID)
            # assert fields
            self.assertEqual(all_2.getAUserType(), all_aUserType_obj_2)
            self.assertEqual(all_2.getAString(), all_aString_obj_2)
            self.assertEqual(all_2.getAList() is not None and all_2.getAList(), [3.0, 4.0])
            self.assertEqual(all_2.getAMap() is not None and all_2.getAMap(), self.put(dict(), '5_2', _2))
            self.assertEqual(all_2.getAnArray(), ["all_aUserType_obj"]_2)
            self.assertEqual(all_2.getAnAnnotation(), all_aBool_obj_2)
            self.assertEqual(all_2.getAnotherUserType(), all_anotherUserType_obj_2)
            self.assertEqual(all_2.getASet() is not None and all_2.getASet(), set(2))
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

            self.assertEqual(all_aBool_obj_2.getBasicBool(), true)

            self.assertEqual(all_aString_obj_2.getBasicString() is not None and all_aString_obj_2.getBasicString(), "Hello World!")
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

    def test_API_core_basicTypes_acc_roland(self):
        file = self.tmpFile("roland.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            v_0_b = sf.BasicInt64V.make()
            v_1_a = sf.BasicInt64V.make()
            v_0_c = sf.BasicInt64V.make()
            v_1_b = sf.BasicInt64V.make()
            v_2_a = sf.BasicInt64V.make()
            v_0_a = sf.BasicInt64V.make()
            v_3_c = sf.BasicInt64V.make()
            v_4_b = sf.BasicInt64V.make()
            v_5_a = sf.BasicInt64V.make()
            v_4_c = sf.BasicInt64V.make()
            v_5_b = sf.BasicInt64V.make()
            v_6_a = sf.BasicInt64V.make()
            v_1_c = sf.BasicInt64V.make()
            v_2_b = sf.BasicInt64V.make()
            v_3_a = sf.BasicInt64V.make()
            v_2_c = sf.BasicInt64V.make()
            v_3_b = sf.BasicInt64V.make()
            v_4_a = sf.BasicInt64V.make()
            v_7_c = sf.BasicInt64V.make()
            v_8_b = sf.BasicInt64V.make()
            v_9_a = sf.BasicInt64V.make()
            v_8_c = sf.BasicInt64V.make()
            v_9_b = sf.BasicInt64V.make()
            v_5_c = sf.BasicInt64V.make()
            v_6_b = sf.BasicInt64V.make()
            v_7_a = sf.BasicInt64V.make()
            v_6_c = sf.BasicInt64V.make()
            v_7_b = sf.BasicInt64V.make()
            v_8_a = sf.BasicInt64V.make()
            v_9_c = sf.BasicInt64V.make()
            # set fields
            v_0_b.setBasicInt(0)

            v_1_a.setBasicInt(129)

            v_0_c.setBasicInt(-1)

            v_1_b.setBasicInt(128)

            v_2_a.setBasicInt(16385)

            v_0_a.setBasicInt(1)

            v_3_c.setBasicInt(2097151)

            v_4_b.setBasicInt(268435456)

            v_5_a.setBasicInt(34359738369)

            v_4_c.setBasicInt(268435455)

            v_5_b.setBasicInt(34359738368)

            v_6_a.setBasicInt(4398046511105)

            v_1_c.setBasicInt(127)

            v_2_b.setBasicInt(16384)

            v_3_a.setBasicInt(2097153)

            v_2_c.setBasicInt(16383)

            v_3_b.setBasicInt(2097152)

            v_4_a.setBasicInt(268435457)

            v_7_c.setBasicInt(562949953421311)

            v_8_b.setBasicInt(72057594037927936)

            v_9_a.setBasicInt(-9223372036854775807)

            v_8_c.setBasicInt(72057594037927935)

            v_9_b.setBasicInt(-9223372036854775808)

            v_5_c.setBasicInt(34359738367)

            v_6_b.setBasicInt(4398046511104)

            v_7_a.setBasicInt(562949953421313)

            v_6_c.setBasicInt(4398046511103)

            v_7_b.setBasicInt(562949953421312)

            v_8_a.setBasicInt(72057594037927937)

            v_9_c.setBasicInt(9223372036854775807)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(30, sf.BasicInt64V.staticSize())
            # create objects from file
            v_0_b_2 = sf2.BasicInt64V.getByID(v_0_b.skillID)
            v_1_a_2 = sf2.BasicInt64V.getByID(v_1_a.skillID)
            v_0_c_2 = sf2.BasicInt64V.getByID(v_0_c.skillID)
            v_1_b_2 = sf2.BasicInt64V.getByID(v_1_b.skillID)
            v_2_a_2 = sf2.BasicInt64V.getByID(v_2_a.skillID)
            v_0_a_2 = sf2.BasicInt64V.getByID(v_0_a.skillID)
            v_3_c_2 = sf2.BasicInt64V.getByID(v_3_c.skillID)
            v_4_b_2 = sf2.BasicInt64V.getByID(v_4_b.skillID)
            v_5_a_2 = sf2.BasicInt64V.getByID(v_5_a.skillID)
            v_4_c_2 = sf2.BasicInt64V.getByID(v_4_c.skillID)
            v_5_b_2 = sf2.BasicInt64V.getByID(v_5_b.skillID)
            v_6_a_2 = sf2.BasicInt64V.getByID(v_6_a.skillID)
            v_1_c_2 = sf2.BasicInt64V.getByID(v_1_c.skillID)
            v_2_b_2 = sf2.BasicInt64V.getByID(v_2_b.skillID)
            v_3_a_2 = sf2.BasicInt64V.getByID(v_3_a.skillID)
            v_2_c_2 = sf2.BasicInt64V.getByID(v_2_c.skillID)
            v_3_b_2 = sf2.BasicInt64V.getByID(v_3_b.skillID)
            v_4_a_2 = sf2.BasicInt64V.getByID(v_4_a.skillID)
            v_7_c_2 = sf2.BasicInt64V.getByID(v_7_c.skillID)
            v_8_b_2 = sf2.BasicInt64V.getByID(v_8_b.skillID)
            v_9_a_2 = sf2.BasicInt64V.getByID(v_9_a.skillID)
            v_8_c_2 = sf2.BasicInt64V.getByID(v_8_c.skillID)
            v_9_b_2 = sf2.BasicInt64V.getByID(v_9_b.skillID)
            v_5_c_2 = sf2.BasicInt64V.getByID(v_5_c.skillID)
            v_6_b_2 = sf2.BasicInt64V.getByID(v_6_b.skillID)
            v_7_a_2 = sf2.BasicInt64V.getByID(v_7_a.skillID)
            v_6_c_2 = sf2.BasicInt64V.getByID(v_6_c.skillID)
            v_7_b_2 = sf2.BasicInt64V.getByID(v_7_b.skillID)
            v_8_a_2 = sf2.BasicInt64V.getByID(v_8_a.skillID)
            v_9_c_2 = sf2.BasicInt64V.getByID(v_9_c.skillID)
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
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

