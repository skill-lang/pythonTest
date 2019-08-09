
import unittest
from tempfile import TemporaryFile
from python.src.restrictionsCore.api import *
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

    def test_restrictionsCore_read_accept_age_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/age.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_age16_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/age16.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_ageUnrestricted_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/ageUnrestricted.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_aircraft_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/aircraft.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_annotationNull_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/annotationNull.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_annotationString_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/annotationString.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_annotationTest_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/annotationTest.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_coloredNodes_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/coloredNodes.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_container_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/container.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_crossNodes_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/crossNodes.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_date_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/date.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_emptyBlocks_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/emptyBlocks.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_emptyFile_sf(self):
        sf = self.read("src/test/resources/genbinary/[[all]]/accept/emptyFile.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_fourColoredNodes_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/fourColoredNodes.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_localBasePoolOffset_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/localBasePoolOffset.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_noFieldRegressionTest_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/noFieldRegressionTest.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_nodeFirstBlockOnly_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/nodeFirstBlockOnly.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_restrictionsAll_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/restrictionsAll.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_trivialType_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/trivialType.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_twoNodeBlocks_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/twoNodeBlocks.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_twoTypes_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/twoTypes.sf")
        self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_unicode_reference_sf(self):
        sf = self.read("src/test/resources/genbinary/restrictionsCore/accept/unicode-reference.sf")
        self.assertIsNotNone(sf)

