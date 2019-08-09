
import unittest
from tempfile import TemporaryFile
from python.src.fancy.api import *
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

    def test_fancy_read_accept_age_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/age.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_age16_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/age16.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_ageUnrestricted_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/ageUnrestricted.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_aircraft_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/aircraft.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_annotationNull_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/annotationNull.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_annotationString_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/annotationString.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_annotationTest_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/annotationTest.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_coloredNodes_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/coloredNodes.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_container_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/container.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_crossNodes_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/crossNodes.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_date_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/date.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_emptyFile_sf(self):
        sf = self.read("src/test/resources/genbinary/[[all]]/accept/emptyFile.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_fourColoredNodes_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/fourColoredNodes.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_restrictionsAll_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/restrictionsAll.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_trivialType_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/trivialType.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_twoNodeBlocks_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/twoNodeBlocks.sf")
        self.assertIsNotNone(sf)

    def test_fancy_read_accept_unicode_reference_sf(self):
        sf = self.read("src/test/resources/genbinary/fancy/accept/unicode-reference.sf")
        self.assertIsNotNone(sf)

