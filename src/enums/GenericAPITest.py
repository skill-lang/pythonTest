

import os
import unittest
from python.src.enums.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_restrictions_enums_fail_instances(self):
        file = self.tmpFile("instances.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            enm_last = sf.TestEnum.make()
            enm_second = sf.TestEnum.make()
            enm_third = sf.TestEnum.make()
            enm_default = sf.TestEnum.make()
            # set fields
            enm_last.setNext(enm_default)
            enm_last.setName("last")

            enm_second.setNext(enm_third)
            enm_second.setName("second")

            enm_third.setNext(enm_last)
            enm_third.setName("third")

            enm_default.setNext(enm_second)
            enm_default.setName("default")
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(4, sf.TestEnum.staticSize())
            # create objects from file
            enm_last_2 = sf2.TestEnum.getByID(enm_last.skillID)
            enm_second_2 = sf2.TestEnum.getByID(enm_second.skillID)
            enm_third_2 = sf2.TestEnum.getByID(enm_third.skillID)
            enm_default_2 = sf2.TestEnum.getByID(enm_default.skillID)
            # assert fields
            self.assertEqual(enm_last_2.getNext(), enm_default_2)

            self.assertEqual(enm_second_2.getNext(), enm_third_2)

            self.assertEqual(enm_third_2.getNext(), enm_last_2)

            self.assertEqual(enm_default_2.getNext(), enm_second_2)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

