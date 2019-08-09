import unittest

from python.src.age.api import *
from python.src.common.CommonTest import CommonTest


class SimpleDelete(unittest.TestCase, CommonTest):

    def test_writeDelete(self):
        count = 100
        file = self.tmpFile("writeDelete")
        sf = SkillFile.open(file.name, Mode.Create, Mode.Write)
        for i in range(0, count):
            sf.Age.make()
        sf.close()

        sf2 = SkillFile.open(file.name, Mode.Write, Mode.Read)
        self.assertEqual(count, len(sf2.Age))
        for a in sf2.Age:
            sf2.delete(a)
        sf2.close()

        sf2 = SkillFile.open(file.name, Mode.ReadOnly, Mode.Read)
        self.assertEqual(0, len(sf2.Age))
        sf2.close()
