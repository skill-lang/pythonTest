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
            p = poolByName.get("testenum")
            self.TestEnum = p if (p is not None) else Parser.newPool("testenum", None, types, self._knownTypes[0])
            p = poolByName.get("testenum:last")
            self.Testenum_last = p if (p is not None) else Parser.newPool("testenum:last", self.TestEnum, types, self._knownTypes[1])
            p = poolByName.get("testenum:third")
            self.Testenum_third = p if (p is not None) else Parser.newPool("testenum:third", self.TestEnum, types, self._knownTypes[2])
            p = poolByName.get("testenum:second")
            self.Testenum_second = p if (p is not None) else Parser.newPool("testenum:second", self.TestEnum, types, self._knownTypes[3])
            p = poolByName.get("testenum:default")
            self.Testenum_default = p if (p is not None) else Parser.newPool("testenum:default", self.TestEnum, types, self._knownTypes[4])
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
            if name == "testenum":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "testenum:last":
                superPool = P1(len(types), superPool, cls)
                return superPool
                 
            elif name == "testenum:third":
                superPool = P2(len(types), superPool, cls)
                return superPool
                 
            elif name == "testenum:second":
                superPool = P3(len(types), superPool, cls)
                return superPool
                 
            elif name == "testenum:default":
                superPool = P4(len(types), superPool, cls)
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
     Test of mapping of enums.
     @author  Timm Felden
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "testenum", ["name", "next"], [None for i in range(0, 1)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "name":
            F0(string, self)

        elif name == "next":
            F1(self.owner().TestEnum, self)
                
    def addField(self, fType, name):
        if name == "next":
            return F1(fType, self)

        if name == "name":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        else:
            return LazyField(fType, name, self)

    def make(self, name=None, Znext=None):
        """
        :return a new TestEnum instance with the argument field values
        """
        rval = self._cls(-1, name, Znext)
        self.add(rval)
        return rval

class P1(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "testenum:last", superPool, [], [None for i in range(0, 0)], cls)


    def make(self, name=None, Znext=None):
        """
        :return a new Testenum_last instance with the argument field values
        """
        rval = self._cls(-1, name, Znext)
        self.add(rval)
        return rval

class P2(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P2, self).__init__(poolIndex, "testenum:third", superPool, [], [None for i in range(0, 0)], cls)


    def make(self, name=None, Znext=None):
        """
        :return a new Testenum_third instance with the argument field values
        """
        rval = self._cls(-1, name, Znext)
        self.add(rval)
        return rval

class P3(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P3, self).__init__(poolIndex, "testenum:second", superPool, [], [None for i in range(0, 0)], cls)


    def make(self, name=None, Znext=None):
        """
        :return a new Testenum_second instance with the argument field values
        """
        rval = self._cls(-1, name, Znext)
        self.add(rval)
        return rval

class P4(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P4, self).__init__(poolIndex, "testenum:default", superPool, [], [None for i in range(0, 0)], cls)


    def make(self, name=None, Znext=None):
        """
        :return a new Testenum_default instance with the argument field values
        """
        rval = self._cls(-1, name, Znext)
        self.add(rval)
        return rval


class F0(AutoField):
    """
    string TestEnum.name
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "name", owner, 0)
        

    
    def get(self, ref):
        return ref.name

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.name = value


class F1(KnownDataField):
    """
    testenum TestEnum.next
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "next", owner)
        
        if fType.name() != "testenum":
            raise SkillException("Expected field type testenum in TestEnum.next but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].Znext = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].Znext
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].Znext
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.Znext

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Znext = value

