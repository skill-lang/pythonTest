import hashlib
import os
import tempfile
import random
import math
from logging import getLogger
from common.internal.Exceptions import SkillException
from common.internal.StoragePool import StoragePool
from common.internal.fieldTypes.ConstantTypes import ConstantInteger
from common.internal.AutoField import AutoField


class CommonTest:

    reflectiveInitSize = 9

    def __init__(self): super(CommonTest, self).__init__()

    @staticmethod
    def createFile(packagePath, name):
        """
        Create a new file, close it and return the closed file.
        :param packagePath: name of the package
        :param name: name of the file
        :return: closed file
        """
        direc = "common/test/resources/serializedTestfiles/" + packagePath
        if not os.path.exists(direc):
            os.makedirs(direc)
        file = "common/test/resources/serializedTestfiles/" + packagePath + name + ".sf"
        if os.path.exists(file):
            os.remove(file)
        return open(file, 'x').close()

    @staticmethod
    def tmpFile(string):
        """
        Create a temporary closed file which doesn't delete itself when closed.
        :param string: prefix of the file name
        :return: closed temporary file
        """
        r = tempfile.NamedTemporaryFile('w+b', -1, None, None, '.sf', string, None, False)
        r.close()
        return r

    @staticmethod
    def sha256(name):
        """
        Create a sha256 hash from a file
        :param name: name of the file
        :return: sha 256 hash
        """
        hasher = hashlib.sha256()
        with open(name, 'rb') as file:
            buffer = file.read()
            hasher.update(buffer)
        return hasher.hexdigest()

    def reflectiveInit(self, sf):
        for t in sf.allTypes():
            try:
                for i in range(self.reflectiveInitSize, 0, -1):
                    t.make()
            except SkillException:
                pass  # the type cannot have more instances

        for t in sf.allTypes():  # t: StoragePool
            for obj in t:  # obj: SkillObject
                for f in t.fields():
                    if not isinstance(f, AutoField) and not isinstance(f.fieldType(), ConstantInteger):
                        self.set(sf, obj, f)

    def set(self, sf, obj, f):
        v = self.value(sf, f.fieldType())
        setattr(obj, f.name(), v)

    def value(self, sf, fType):
        if isinstance(fType, StoragePool):
            it = fType.__iter__()
            for i in range(random.randint(0, self.reflectiveInitSize - 1) % 200, 0, -1):
                it.__next__()
            return it.__next__()

        if fType.typeID() == 5:
            ts = sf.allTypes().__iter__()
            t = ts.__next__()
            for i in range(random.randint(0, 200), 0, -1):
                try:
                    t = ts.__next__()
                except StopIteration:
                    break
            it = t.__iter__()
            item = None
            for i in range(random.randint(0, min(200, self.reflectiveInitSize)) + 1, 0, -1):
                try:
                    item = it.__next__()
                except StopIteration:
                    break
            return item
        elif fType.typeID() == 6:
            return bool(random.getrandbits(1))
        elif fType.typeID() in [7, 8, 9, 10, 11]:
            return random.randint(0, self.reflectiveInitSize - 1)
        elif fType.typeID() in [12, 13]:
            return random.random()
        elif fType.typeID() == 14:
            return "☢☢☢"
        elif fType.typeID() == 15:
            rval = []
            for i in range(len(fType), 0, -1):
                rval.append(self.value(sf, fType.groundType))
            return rval
        elif fType.typeID() in [17, 18]:
            length = math.sqrt(self.reflectiveInitSize)
            rval = []
            while length != 0:
                length -= 1
                rval.append(self.value(sf, fType.groundType))
            return rval
        elif fType.typeID() == 19:
            length = math.sqrt(self.reflectiveInitSize)
            rval = set()
            while length != 0:
                length -= 1
                rval.add(self.value(sf, fType.groundType))
        elif fType.typeID() == 20:
            return {}
        else:
            getLogger().error("wrong field type in CommonTest")
            raise Exception()

    @staticmethod
    def arrayList(*ts):
        rval = []
        for t in ts:
            rval.append(t)
        return rval

    @staticmethod
    def sets(*ts):
        rval = set()
        for t in ts:
            rval.add(t)
        return rval

    @staticmethod
    def put(m: {}, key, value):
        m[key] = value
        return m
