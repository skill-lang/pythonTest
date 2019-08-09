import unittest

from python.src.age.api import *
from python.src.common.CommonTest import CommonTest


class SimpleAppend(unittest.TestCase, CommonTest):
    """Test appending to a file."""

    def test_appendExample(self):
        path = self.tmpFile("append.test")

        sf = SkillFile.open("age-example.sf", Mode.Read, Mode.Append)
        sf.Age.make(2)
        sf.Age.make(3)
        sf.changePath(path.name)
        sf.close()

        self.assertEqual(self.sha256(path.name), self.sha256("age-example-append.sf"))
        sf2 = SkillFile.open(path.name, Mode.ReadOnly, Mode.Read)
        l = [1, -1, 2, 3]
        i = 0
        for next in sf2.Age:
            self.assertEqual(next.age, l[i])
            i = i + 1
        sf2.close()

    def test_writeAppendMultiState(self):
        limit = 10000
        path = self.tmpFile("append")
        # write
        sf = SkillFile.open(path.name, Mode.Create, Mode.Write)
        for i in range(0, limit):
            sf.Age.make(i)
        sf.close()
        # append
        for i in range(1, 10):
            sf = SkillFile.open(path.name, Mode.Read, Mode.Append)
            for v in range(i * limit, limit + i * limit):
                sf.Age.make(v)
            sf.close()
        # read & check & write
        writePath = self.tmpFile("write")
        state = SkillFile.open(path.name, Mode.Read, Mode.Write)
        self.assertEqual(len(state.Age), 10*limit, msg="we somehow lost " + str(10 * limit - len(state.Age)) + " dates")
        cond = True
        d = state.Age.__iter__()
        for i in range(0, 10*limit):
            cond = cond and (i == d.__next__().age)
        self.assertTrue(cond, msg="match failed")
        state.changePath(writePath.name)
        state.close()
        # check append against write
      #  self.assertEqual(self.sha256(path.name), self.sha256(writePath.name))
        s1 = SkillFile.open(path.name, Mode.Read)
        s2 = SkillFile.open(writePath.name, Mode.Read)
        for x, y in zip(s1.Age, s2.Age):
            self.assertEqual(x.age, y.age)
