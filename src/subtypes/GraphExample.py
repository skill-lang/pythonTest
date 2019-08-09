import unittest

from python.src.common.CommonTest import CommonTest
from python.src.subtypes.api import *


class GraphExample(unittest.TestCase, CommonTest):

    def test_EndVortrag(self):
        file = self.tmpFile("graph")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        c = sf.C.make()
        d = sf.D.make()
        c.setA(d)
        d.setA(c)
        c.setC(c)
        d.setD(d)
        sf.close()

        sf2 = SkillFile.open(file.name, Mode.Read, Mode.ReadOnly)
        c2 = sf2.C.getByID(c.getSkillID())
        self.assertEqual(c2.c, c2)
        d2 = sf2.D.getByID(d.getSkillID())
        self.assertEqual(d2.d, d2)
        self.assertEqual(c2.a, d2)
        self.assertEqual(d2.a, c2)
