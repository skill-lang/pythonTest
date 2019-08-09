

import os
import unittest
from python.src.hintsAll.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_API_core_hintsAll_acc_basic(self):
        file = self.tmpFile("basic.sf")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        try:
            # create objects
            a = sf.Abuser.make()
            nas = sf.NowASingleton.make()
            uid = sf.UID.make()
            bt = sf.BadType.make()
            u = sf.User.make()
            em = sf.ExternMixin.make()
            expr = sf.Expression.make()
            # set fields
            a.setAbuseDescription("I am a absue description")


            uid.setIdentifier(7)

            bt.setReflectivelyInVisible("I am reflectively visible")
            bt.setIgnoredData("Ignore me")

            u.setName("herb")
            u.setReflectivelyVisible("I am not visible")
            u.setAge(43)

            em.setUnknownStuff(None)

            sf.close()

            # read back and assert correctness
            sf2 = SkillFile.open(sf.currentPath(), Mode.Read, Mode.ReadOnly)
            # check count per Type
            self.assertEqual(1, sf.BadType.staticSize())
            self.assertEqual(1, sf.NowASingleton.staticSize())
            self.assertEqual(1, sf.Abuser.staticSize())
            self.assertEqual(1, sf.ExternMixin.staticSize())
            self.assertEqual(1, sf.User.staticSize())
            self.assertEqual(1, sf.UID.staticSize())
            self.assertEqual(1, sf.Expression.staticSize())
            # create objects from file
            a_2 = sf2.Abuser.getByID(a.skillID)
            nas_2 = sf2.NowASingleton.getByID(nas.skillID)
            uid_2 = sf2.UID.getByID(uid.skillID)
            bt_2 = sf2.BadType.getByID(bt.skillID)
            u_2 = sf2.User.getByID(u.skillID)
            em_2 = sf2.ExternMixin.getByID(em.skillID)
            expr_2 = sf2.Expression.getByID(expr.skillID)
            # assert fields
            self.assertEqual(a_2.getAbuseDescription() is not None and a_2.getAbuseDescription(), "I am a absue description")


            self.assertEqual(uid_2.getIdentifier(), 7)

            self.assertEqual(bt_2.getReflectivelyInVisible() is not None and bt_2.getReflectivelyInVisible(), "I am reflectively visible")
            self.assertEqual(bt_2.getIgnoredData() is not None and bt_2.getIgnoredData(), "Ignore me")

            self.assertEqual(u_2.getName() is not None and u_2.getName(), "herb")
            self.assertEqual(u_2.getReflectivelyVisible() is not None and u_2.getReflectivelyVisible(), "I am not visible")
            self.assertEqual(u_2.getAge(), 43)

            self.assertEqual(em_2.getUnknownStuff(), null)

            # close file
            sf2.close()
        finally:
            # delete files
            os.remove(sf.currentPath())

