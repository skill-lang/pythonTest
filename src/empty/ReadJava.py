

import os
import unittest
from python.src.empty.api import *
from python.src.common.CommonTest import CommonTest


class GenericAPITest(unittest.TestCase, CommonTest):
    """
    Tests the file reading capabilities.
    """

    def test_empty(self):
        file = "../../DatenJava/empty/empty.sf"
        sf2 = SkillFile.open(file, Mode.Read, Mode.ReadOnly)
        sf2.close()

