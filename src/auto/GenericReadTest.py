
import unittest
from tempfile import TemporaryFile
from python.src.auto.api import *
from python.src.common.CommonTest import CommonTest


class GenericReadTest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """
    def read(self, s):
        return SkillFile.open("../../../../" + s, Mode.Read, Mode.ReadOnly)

    def test_writeGeneric(self):
        path = self.tmpFile("write.generic")

        sf = SkillFile.open(path.name)
        self.reflectiveInit(sf)

    def test_writeGenericChecked(self):
        path = self.tmpFile("write.generic.checked")

        # create a name -> type map
        types = dict()
        sf = SkillFile.open(path.name)
        self.reflectiveInit(sf)

        for t in sf.allTypes():
            types[t.name()] = t

        # read file and check skill IDs
        sf2 = SkillFile.open(path.name, Mode.Read)
        for t in sf2.allTypes():
            os = types.get(t.name()).__iter__()
            for o in t:
                self.assertTrue("to few instances in read stat", os.hasNext())
                self.assertEquals(o.getSkillID(), os.next().getSkillID())

    def test_auto_read_accept_age_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/age.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_ageUnrestricted_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/ageUnrestricted.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_coloredNodes_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/coloredNodes.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_crossNodes_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/crossNodes.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_date_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/date.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_emptyBlocks_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/emptyBlocks.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_emptyFile_sf(self):
        sf = self.read("src/test/resources/genbinary/[[all]]/accept/emptyFile.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_noFieldRegressionTest_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/noFieldRegressionTest.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_nodeFirstBlockOnly_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/nodeFirstBlockOnly.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_trivialType_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/trivialType.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_twoNodeBlocks_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/twoNodeBlocks.sf")
        self.assertIsNotNone(sf)

    def test_auto_read_accept_unicode_reference_sf(self):
        sf = self.read("src/test/resources/genbinary/auto/accept/unicode-reference.sf")
        self.assertIsNotNone(sf)

