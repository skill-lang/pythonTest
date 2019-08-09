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
            p = poolByName.get("l")
            self.L = p if (p is not None) else Parser.newPool("l", None, types, self._knownTypes[0])
            p = poolByName.get("t")
            self.T = p if (p is not None) else Parser.newPool("t", None, types, self._knownTypes[1])
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
            if name == "l":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "t":
                superPool = P1(len(types), cls)
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

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "l", [], [None for i in range(0, 0)], cls)


    def make(self):
        """
        :return a new L instance with the argument field values
        """
        rval = self._cls(-1)
        self.add(rval)
        return rval

class P1(BasePool):

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "t", ["ref"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "ref":
            F0(MapType(string, MapType(self.owner().L, string)), self)

    def addField(self, fType, name):
        if name == "ref":
            return F0(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, ref=None):
        """
        :return a new T instance with the argument field values
        """
        rval = self._cls(-1, ref)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    map<string,l,string> T.ref
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "ref", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type map<string,l,string> in T.ref but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        for i in range(i, h):
            d[i].ref = fType.readSingleField(inStream)


    def _osc(self, i, h):
        
        fType = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].ref
            if v is None or len(v) == 0:
                result += 1
            else:
                result += V64.singleV64Offset(len(v))
                result += fType.keyType.calculateOffset(v.keys())
                result += fType.valueType.calculateOffset(v.values())
            
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        fType = self.fieldType()
        for i in range(i, h):
            self.fieldType().writeSingleField(d[i].ref, out)


    def get(self, ref):
        return ref.ref

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.ref = value

