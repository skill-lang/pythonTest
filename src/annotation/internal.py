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
            p = poolByName.get("date")
            self.Date = p if (p is not None) else Parser.newPool("date", None, types, self._knownTypes[0])
            p = poolByName.get("test")
            self.Test = p if (p is not None) else Parser.newPool("test", None, types, self._knownTypes[1])
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
            if name == "date":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "test":
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
    """
     A simple date test with known Translation
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "date", ["date"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "date":
            F0(V64(), self)

    def addField(self, fType, name):
        if name == "date":
            return F0(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, date=0):
        """
        :return a new Date instance with the argument field values
        """
        rval = self._cls(-1, date)
        self.add(rval)
        return rval

class P1(BasePool):
    """
     Test the implementation of annotations.
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "test", ["f"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "f":
            F1(annotation, self)

    def addField(self, fType, name):
        if name == "f":
            return F1(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, f=None):
        """
        :return a new Test instance with the argument field values
        """
        rval = self._cls(-1, f)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    v64 Date.date
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "date", owner)
        
        if self.fieldType().typeID() != 11:
            raise SkillException("Expected field type v64 in Date.date but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].date = inStream.v64()


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            result += V64.singleV64Offset(d[i].date)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.v64(d[i].date)


    def get(self, ref):
        return ref.date

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.date = value


class F1(KnownDataField):
    """
    annotation Test.f
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "f", owner)
        
        if self.fieldType().typeID() != 5:
            raise SkillException("Expected field type annotation in Test.f but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].f = t.readSingleField(inStream)


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].f
            if v is None:
                result += 2
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].f, out)


    def get(self, ref):
        return ref.f

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.f = value

