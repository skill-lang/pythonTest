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
            p = poolByName.get("container")
            self.Container = p if (p is not None) else Parser.newPool("container", None, types, self._knownTypes[0])
            p = poolByName.get("somethingelse")
            self.SomethingElse = p if (p is not None) else Parser.newPool("somethingelse", None, types, self._knownTypes[1])
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
            if name == "container":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "somethingelse":
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
        super(P0, self).__init__(poolIndex, "container", ["arr", "f", "l", "s", "someset", "varr"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "arr":
            F0(ConstantLengthArray(3, V64()), self)

        elif name == "f":
            F1(MapType(string, MapType(V64(), V64())), self)
                
        elif name == "l":
            F2(ListType(V64()), self)
                
        elif name == "s":
            F3(SetType(V64()), self)
                
        elif name == "someset":
            F4(SetType(self.owner().SomethingElse), self)
                
        elif name == "varr":
            F5(VariableLengthArray(V64()), self)
                
    def addField(self, fType, name):
        if name == "arr":
            return F0(fType, self)

        if name == "f":
            return F1(fType, self)

        if name == "l":
            return F2(fType, self)

        if name == "s":
            return F3(fType, self)

        if name == "someset":
            return F4(fType, self)

        if name == "varr":
            return F5(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, arr=None, f=None, l=None, s=None, someSet=None, varr=None):
        """
        :return a new Container instance with the argument field values
        """
        rval = self._cls(-1, arr, f, l, s, someSet, varr)
        self.add(rval)
        return rval

class P1(BasePool):
    """
     no instance of this is required
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "somethingelse", [], [None for i in range(0, 0)], cls)


    def make(self):
        """
        :return a new SomethingElse instance with the argument field values
        """
        rval = self._cls(-1)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    v64[3] Container.arr
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "arr", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type v64[3] in Container.arr but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        size = len(fType)
        
        for i in range(i, h):
            v = []
            for _ in range(0,size):
                v.append(inStream.v64())
            d[i].arr = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        size = len(fType)
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].arr
            if len(v) != len(self.fieldType()):
                raise Exception("constant length array has wrong size")

            for x in v:
                    result += V64.singleV64Offset(x)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        fType = self.fieldType()
        size = len(fType)
        
        for i in range(i, h):
            
            x = d[i].arr
            for e in x:
                out.v64(e)
            


    def get(self, ref):
        return ref.arr

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.arr = value


class F1(KnownDataField):
    """
    map<string,v64,v64> Container.f
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "f", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type map<string,v64,v64> in Container.f but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        for i in range(i, h):
            d[i].f = fType.readSingleField(inStream)


    def _osc(self, i, h):
        
        fType = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].f
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
            self.fieldType().writeSingleField(d[i].f, out)


    def get(self, ref):
        return ref.f

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.f = value


class F2(KnownDataField):
    """
    list<v64> Container.l
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "l", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type list<v64> in Container.l but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            size = inStream.v64()
            v = []
            for k in range(0, size):
                v.append(inStream.v64())
            d[i].l = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].l
            if v is None:
                size = 0
            else:
                size = len(v)
            if 0 == size:
                result += 1
            else:
                result += V64.singleV64Offset(size)
                for x in v:
                    result += V64.singleV64Offset(x)
            
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            
            x = d[i].l
            size = 0 if x is None else len(x)
            if size == 0:
                out.i8(0)
            else:
                out.v64(size)
                for e in x:
                    out.v64(e)

        


    def get(self, ref):
        return ref.l

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.l = value


class F3(KnownDataField):
    """
    set<v64> Container.s
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "s", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type set<v64> in Container.s but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            size = inStream.v64()
            v = set()
            t = self.fieldType().groundType
            for k in range(0, size):
                v.add(inStream.v64())
            d[i].s = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].s
            if v is None:
                size = 0
            else:
                size = len(v)
            if 0 == size:
                result += 1
            else:
                result += V64.singleV64Offset(size)
                for x in v:
                    result += V64.singleV64Offset(x)
            
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            
            x = d[i].s
            size = 0 if x is None else len(x)
            if size == 0:
                out.i8(0)
            else:
                out.v64(size)
                for e in x:
                    out.v64(e)

        


    def get(self, ref):
        return ref.s

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.s = value


class F4(KnownDataField):
    """
    set<somethingelse> Container.someSet
    """
    def __init__(self, fType, owner):
        super(F4, self).__init__(fType, "someset", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type set<somethingelse> in Container.someSet but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        
        t = fType.groundType
        for i in range(i, h):
            size = inStream.v64()
            v = set()
            t = self.fieldType().groundType
            for k in range(0, size):
                v.add(t.getByID(inStream.v64()))
            d[i].someSet = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].someSet
            if v is None:
                size = 0
            else:
                size = len(v)
            if 0 == size:
                result += 1
            else:
                result += V64.singleV64Offset(size)
                for x in v:
                    if x is None:
                        result += 1
                    else:
                        result += V64.singleV64Offset(x.getSkillID())
            
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            
            x = d[i].someSet
            size = 0 if x is None else len(x)
            if size == 0:
                out.i8(0)
            else:
                out.v64(size)
                for e in x:
                    
                    v = e
                    if v is None:
                        out.i8(0)
                    else:
                        out.v64(v.getSkillID())

        


    def get(self, ref):
        return ref.someSet

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.someSet = value


class F5(KnownDataField):
    """
    v64[] Container.varr
    """
    def __init__(self, fType, owner):
        super(F5, self).__init__(fType, "varr", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type v64[] in Container.varr but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            size = inStream.v64()
            v = []
            for k in range(0, size):
                v.append(inStream.v64())
            d[i].varr = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].varr
            if v is None:
                size = 0
            else:
                size = len(v)
            if 0 == size:
                result += 1
            else:
                result += V64.singleV64Offset(size)
                for x in v:
                    result += V64.singleV64Offset(x)
            
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            
            x = d[i].varr
            size = 0 if x is None else len(x)
            if size == 0:
                out.i8(0)
            else:
                out.v64(size)
                for e in x:
                    out.v64(e)

        


    def get(self, ref):
        return ref.varr

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.varr = value

