

import os
import unittest
from python.src.user.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_user_acc_bernd(self):
        file = self.tmpFile("bernd.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            usr = sf.User.make()
            # set fields
            usr.setName("Bernd das Brot")
            usr.setAge(44)
            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.User.staticSize())
            # create objects from file
            usr_2 = sf2.User.getByID(usr.skillID)
            # assert fields
            self.assertEqual(usr_2.getName() is not None and usr_2.getName(), "Bernd das Brot")
            self.assertEqual(usr_2.getAge(), 44)
            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

