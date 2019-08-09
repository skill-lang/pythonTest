
from unittest import Testcase
from tempfle import TemporaryFile
from src.test.de.ust.skill.generator.common.CommonTest import CommonTest
from restrictionsCore.api.SkillFile import SkillFile

from src.api.SkillException import SkillException
from src.api.SkillFile import SkillFile.Mode
from src.internal.ForceLazyFields import ForceLazyFields
from src.internal.SkillObject import SkillObject


class GenericReadTest(CommonTest, Testcase):
    """
    Tests the file reading capabilities.
    """
    def test_read(self, s):
        return SkillFile.open("../../" + s, Mode.Read, Mode.ReadOnly)

    def test_writeGeneric(self):
        path = tmpFile("write.generic")
        try:
            sf = SkillFile.open(path))
            self.reflectiveInit(sf)

    def test_writeGenericChecked(self):
        path = tmpFile("write.generic.checked")

        // create a name -> type map
        types = dict()
        try:
            sf = SkillFile.open(path))
            self.reflectiveInit(sf);

            for t in sf.allTypes():
                types.put(t.name(), t)

        // read file and check skill IDs
        sf2 = SkillFile.open(path, Mode.Read);
        for t in sf2.allTypes():
            os = types.get(t.name()).iterator()
            for o in t:
                assertTrue("to few instances in read stat", os.hasNext())
                assertEquals(o.getSkillID(), os.next().getSkillID())

    def test_restrictionsCore_read_accept_age_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/age.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_age16_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/age16.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_ageUnrestricted_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/ageUnrestricted.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_aircraft_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/aircraft.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_annotationNull_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/annotationNull.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_annotationString_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/annotationString.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_annotationTest_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/annotationTest.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_coloredNodes_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/coloredNodes.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_container_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/container.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_crossNodes_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/crossNodes.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_date_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/date.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_emptyBlocks_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/emptyBlocks.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_emptyFile_sf(self):
        try:
            sf = read("src/test/resources/genbinary/[[all]]/accept/emptyFile.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_fourColoredNodes_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/fourColoredNodes.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_localBasePoolOffset_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/localBasePoolOffset.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_noFieldRegressionTest_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/noFieldRegressionTest.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_nodeFirstBlockOnly_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/nodeFirstBlockOnly.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_restrictionsAll_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/restrictionsAll.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_trivialType_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/trivialType.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_twoNodeBlocks_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/twoNodeBlocks.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_twoTypes_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/twoTypes.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_accept_unicode_reference_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/accept/unicode-reference.sf")
            self.assertIsNotNone(sf)

    def test_restrictionsCore_read_reject_duplicateDefinition_sf(self):
        try:
            sf = read("src/test/resources/genbinary/[[all]]/fail/duplicateDefinition.sf")
            ForceLazyFields.forceFullCheck(sf);
            Assert.fail("Expected ParseException to be thrown");
        except SkillException:
            # success

    def test_restrictionsCore_read_reject_duplicateDefinitionMixed_sf(self):
        try:
            sf = read("src/test/resources/genbinary/[[all]]/fail/duplicateDefinitionMixed.sf")
            ForceLazyFields.forceFullCheck(sf);
            Assert.fail("Expected ParseException to be thrown");
        except SkillException:
            # success

    def test_restrictionsCore_read_reject_duplicateDefinitionSecondBlock_sf(self):
        try:
            sf = read("src/test/resources/genbinary/[[all]]/fail/duplicateDefinitionSecondBlock.sf")
            ForceLazyFields.forceFullCheck(sf);
            Assert.fail("Expected ParseException to be thrown");
        except SkillException:
            # success

    def test_restrictionsCore_read_reject_illegalStringPoolOffsets_sf(self):
        try:
            sf = read("src/test/resources/genbinary/[[all]]/fail/illegalStringPoolOffsets.sf")
            ForceLazyFields.forceFullCheck(sf);
            Assert.fail("Expected ParseException to be thrown");
        except SkillException:
            # success

    def test_restrictionsCore_read_reject_illegalTypeID_sf(self):
        try:
            sf = read("src/test/resources/genbinary/[[all]]/fail/illegalTypeID.sf")
            ForceLazyFields.forceFullCheck(sf);
            Assert.fail("Expected ParseException to be thrown");
        except SkillException:
            # success

    def test_restrictionsCore_read_reject_missingUserType_sf(self):
        try:
            sf = read("src/test/resources/genbinary/[[all]]/fail/missingUserType.sf")
            ForceLazyFields.forceFullCheck(sf);
            Assert.fail("Expected ParseException to be thrown");
        except SkillException:
            # success

    def test_restrictionsCore_read_reject_nullAsFieldName_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/fail/nullAsFieldName.sf")
            ForceLazyFields.forceFullCheck(sf);
            Assert.fail("Expected ParseException to be thrown");
        except SkillException:
            # success

    def test_restrictionsCore_read_reject_nullInNonNullNode_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/fail/nullInNonNullNode.sf")
            ForceLazyFields.forceFullCheck(sf);
            Assert.fail("Expected ParseException to be thrown");
        except SkillException:
            # success

    def test_restrictionsCore_read_reject_partial_sf(self):
        try:
            sf = read("src/test/resources/genbinary/restrictionsCore/fail/partial.sf")
            ForceLazyFields.forceFullCheck(sf);
            Assert.fail("Expected ParseException to be thrown");
        except SkillException:
            # success

