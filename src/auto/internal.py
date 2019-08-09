#  ___ _  ___ _ _                                                                                                      #
# / __| |/ (_) | |     Your SKilL python Binding                                                                       #
# \__ \ ' <| | | |__   <<debug>>                                                                                       #
# |___/_|\_\_|_|____|  by: <<some developer>>                                                                          #
#                                                                                                                      #

from common.internal.FileParser import FileParser
from common.internal.SkillState import SkillState as State
from common.internal.Exceptions import SkillException, ParseException
from common.internal.BasePool import BasePool
from common.internal.FieldDeclaration import FieldDeclaration
from common.internal.FieldType import FieldType
from common.internal.KnownDataField import KnownDataField
from common.internal.SkillObject import SkillObject
from common.internal.StoragePool import StoragePool
from common.internal.StringPool import StringPool
from common.internal.AutoField import AutoField
from common.internal.LazyField import LazyField
from common.internal.fieldTypes.Annotation import Annotation
from common.internal.fieldTypes.BoolType import BoolType
from common.internal.fieldTypes.ConstantLengthArray import ConstantLengthArray
from common.internal.fieldTypes.ConstantTypes import ConstantI8, ConstantI16, ConstantI32, ConstantI64, ConstantV64
from common.internal.fieldTypes.FloatType import F32, F64
from common.internal.fieldTypes.IntegerTypes import I8, I16, I32, I64, V64
from common.internal.fieldTypes.ListType import ListType
from common.internal.fieldTypes.MapType import MapType
from common.internal.fieldTypes.SetType import SetType
from common.internal.fieldTypes.SingleArgumentType import SingleArgumentType
from common.internal.fieldTypes.VariableLengthArray import VariableLengthArray
from common.internal.Blocks import *
from common.streams.FileInputStream import FileInputStream
from common.internal.Mode import ActualMode, Mode


class SkillState(State):
    """
    Internal implementation of SkillFile.
    note: type access fields start with a capital letter to avoid collisions
    """

    @staticmethod
    def open(path, mode: [], knownTypes: []):
        """
        Create a new skill file based on argument path and mode.
        """
        actualMode = ActualMode(mode)
        try:
            if actualMode.openMode == Mode.Create:
                strings = StringPool(None)
                types = []
                annotation = Annotation(types)
                return SkillState({}, strings, annotation, types,
                                    FileInputStream.open(path), actualMode.closeMode, knownTypes)
            elif actualMode.openMode == Mode.Read:
                p = Parser(FileInputStream.open(path), knownTypes)
                return p.read(SkillState, actualMode.closeMode, knownTypes)
            else:
                raise Exception("should never happen")
        except SkillException as e:
            raise e
        except Exception as e:
            raise SkillException(e)

    def __init__(self, poolByName, strings, annotationType, types, inStream, mode, knownTypes):
        super(SkillState, self).__init__(strings, inStream.path, mode, types, poolByName, annotationType)
        self._knownTypes = knownTypes

        try:
            p = poolByName.get("a")
            self.A = p if (p is not None) else Parser.newPool("a", None, types, self._knownTypes[0])
            p = poolByName.get("b")
            self.B = p if (p is not None) else Parser.newPool("b", self.A, types, self._knownTypes[1])
            p = poolByName.get("c")
            self.C = p if (p is not None) else Parser.newPool("c", self.B, types, self._knownTypes[2])
            p = poolByName.get("d")
            self.D = p if (p is not None) else Parser.newPool("d", self.B, types, self._knownTypes[3])
            p = poolByName.get("noserializeddata")
            self.NoSerializedData = p if (p is not None) else Parser.newPool("noserializeddata", None, types, self._knownTypes[4])
        except Exception as e:
            raise ParseException(inStream, -1, e,
                                 "A super type does not match the specification; see cause for details.")
        for t in types:
            self._poolByName[t.name()] = t

        self._finalizePools(inStream)

class Parser(FileParser):

    def __init__(self, inStream, knownTypes):
        super(Parser, self).__init__(inStream, knownTypes)

    @staticmethod
    def newPool(name: str, superPool, types: [], cls):
        """allocate correct pool type and add it to types"""
        try:
            if name == "a":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "b":
                superPool = P1(len(types), superPool, cls)
                return superPool
                 
            elif name == "c":
                superPool = P2(len(types), superPool, cls)
                return superPool
                 
            elif name == "d":
                superPool = P3(len(types), superPool, cls)
                return superPool
                 
            elif name == "noserializeddata":
                superPool = P4(len(types), cls)
                return superPool
            else:
                if superPool is None:
                    superPool = BasePool(len(types), name, StoragePool.noKnownFields, StoragePool.noAutoFields, cls)
                else:
                    superPool = superPool.makeSubPool(len(types), name, cls)
            return superPool
        finally:
            types.append(superPool)

class P0(BasePool):
    """
     Check subtyping; use single fields only, because otherwise field IDs are underspecified
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "a", ["a"], [None for i in range(0, 1)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "a":
            F0(self.owner().A, self)

    def addField(self, fType, name):
        if name == "a":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        else:
            return LazyField(fType, name, self)

    def make(self, a=None):
        """
        :return a new A instance with the argument field values
        """
        rval = self._cls(-1, a)
        self.add(rval)
        return rval

class P1(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "b", superPool, ["b"], [None for i in range(0, 1)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "b":
            F1(self.owner().B, self)

    def addField(self, fType, name):
        if name == "b":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        else:
            return LazyField(fType, name, self)

    def make(self, b=None, a=None):
        """
        :return a new B instance with the argument field values
        """
        rval = self._cls(-1, b, a)
        self.add(rval)
        return rval

class P2(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P2, self).__init__(poolIndex, "c", superPool, ["c"], [None for i in range(0, 1)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "c":
            F2(self.owner().C, self)

    def addField(self, fType, name):
        if name == "c":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        else:
            return LazyField(fType, name, self)

    def make(self, c=None, b=None, a=None):
        """
        :return a new C instance with the argument field values
        """
        rval = self._cls(-1, c, b, a)
        self.add(rval)
        return rval

class P3(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P3, self).__init__(poolIndex, "d", superPool, ["d"], [None for i in range(0, 1)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "d":
            F3(self.owner().D, self)

    def addField(self, fType, name):
        if name == "d":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        else:
            return LazyField(fType, name, self)

    def make(self, d=None, b=None, a=None):
        """
        :return a new D instance with the argument field values
        """
        rval = self._cls(-1, d, b, a)
        self.add(rval)
        return rval

class P4(BasePool):
    """
     All fields of this type are auto.
     @author  Timm Felden
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P4, self).__init__(poolIndex, "noserializeddata", ["age", "name", "seen", "someintegersinalist", "somemap", "somereference"], [None for i in range(0, 6)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "age":
            F4(V64(), self)

        elif name == "name":
            F5(string, self)
                
        elif name == "seen":
            F6(BoolType(), self)
                
        elif name == "someintegersinalist":
            F7(ListType(I32()), self)
                
        elif name == "somemap":
            F8(MapType(string, string), self)
                
        elif name == "somereference":
            F9(self.owner().NoSerializedData, self)
                
    def addField(self, fType, name):
        if name == "age":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        elif name == "name":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        elif name == "seen":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        elif name == "someintegersinalist":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        elif name == "somemap":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        elif name == "somereference":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        else:
            return LazyField(fType, name, self)

    def make(self, age=0, name=None, seen=False, someIntegersInAList=None, someMap=None, someReference=None):
        """
        :return a new NoSerializedData instance with the argument field values
        """
        rval = self._cls(-1, age, name, seen, someIntegersInAList, someMap, someReference)
        self.add(rval)
        return rval


class F0(AutoField):
    """
    a A.a
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "a", owner, 0)
        

    
    def get(self, ref):
        return ref.a

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.a = value


class F1(AutoField):
    """
    b B.b
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "b", owner, 0)
        

    
    def get(self, ref):
        return ref.b

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.b = value


class F2(AutoField):
    """
    c C.c
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "c", owner, 0)
        

    
    def get(self, ref):
        return ref.c

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.c = value


class F3(AutoField):
    """
    d D.d
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "d", owner, 0)
        

    
    def get(self, ref):
        return ref.d

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.d = value


class F4(AutoField):
    """
    v64 NoSerializedData.age
    """
    def __init__(self, fType, owner):
        super(F4, self).__init__(fType, "age", owner, 0)
        

    
    def get(self, ref):
        return ref.age

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.age = value


class F5(AutoField):
    """
    string NoSerializedData.name
    """
    def __init__(self, fType, owner):
        super(F5, self).__init__(fType, "name", owner, -1)
        

    
    def get(self, ref):
        return ref.name

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.name = value


class F6(AutoField):
    """
    bool NoSerializedData.seen
    """
    def __init__(self, fType, owner):
        super(F6, self).__init__(fType, "seen", owner, -2)
        

    
    def get(self, ref):
        return ref.seen

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.seen = value


class F7(AutoField):
    """
    list<i32> NoSerializedData.someIntegersInAList
    """
    def __init__(self, fType, owner):
        super(F7, self).__init__(fType, "someintegersinalist", owner, -3)
        

    
    def get(self, ref):
        return ref.someIntegersInAList

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.someIntegersInAList = value


class F8(AutoField):
    """
    map<string,string> NoSerializedData.someMap
    """
    def __init__(self, fType, owner):
        super(F8, self).__init__(fType, "somemap", owner, -4)
        

    
    def get(self, ref):
        return ref.someMap

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.someMap = value


class F9(AutoField):
    """
    noserializeddata NoSerializedData.someReference
    """
    def __init__(self, fType, owner):
        super(F9, self).__init__(fType, "somereference", owner, -5)
        

    
    def get(self, ref):
        return ref.someReference

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.someReference = value

