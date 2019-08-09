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
            p = poolByName.get("d")
            self.D = p if (p is not None) else Parser.newPool("d", self.B, types, self._knownTypes[2])
            p = poolByName.get("c")
            self.C = p if (p is not None) else Parser.newPool("c", self.A, types, self._knownTypes[3])
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
                 
            elif name == "d":
                superPool = P2(len(types), superPool, cls)
                return superPool
                 
            elif name == "c":
                superPool = P3(len(types), superPool, cls)
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
        super(P0, self).__init__(poolIndex, "a", ["a"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "a":
            F0(self.owner().A, self)

    def addField(self, fType, name):
        if name == "a":
            return F0(fType, self)

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
        super(P1, self).__init__(poolIndex, "b", superPool, ["b"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "b":
            F1(self.owner().B, self)

    def addField(self, fType, name):
        if name == "b":
            return F1(fType, self)

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
        super(P2, self).__init__(poolIndex, "d", superPool, ["d"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "d":
            F2(self.owner().D, self)

    def addField(self, fType, name):
        if name == "d":
            return F2(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, d=None, b=None, a=None):
        """
        :return a new D instance with the argument field values
        """
        rval = self._cls(-1, d, b, a)
        self.add(rval)
        return rval

class P3(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P3, self).__init__(poolIndex, "c", superPool, ["c"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "c":
            F3(self.owner().C, self)

    def addField(self, fType, name):
        if name == "c":
            return F3(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, c=None, a=None):
        """
        :return a new C instance with the argument field values
        """
        rval = self._cls(-1, c, a)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    a A.a
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "a", owner)
        
        if fType.name() != "a":
            raise SkillException("Expected field type a in A.a but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].a = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].a
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].a
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.a

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.a = value


class F1(KnownDataField):
    """
    b B.b
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "b", owner)
        
        if fType.name() != "b":
            raise SkillException("Expected field type b in B.b but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].b = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].b
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        for i in range(i, h):
            
            v = d[i].b
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.b

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.b = value


class F2(KnownDataField):
    """
    d D.d
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "d", owner)
        
        if fType.name() != "d":
            raise SkillException("Expected field type d in D.d but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].d = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].d
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        for i in range(i, h):
            
            v = d[i].d
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.d

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.d = value


class F3(KnownDataField):
    """
    c C.c
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "c", owner)
        
        if fType.name() != "c":
            raise SkillException("Expected field type c in C.c but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].c = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].c
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        for i in range(i, h):
            
            v = d[i].c
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.c

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.c = value

