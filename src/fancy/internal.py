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
            self.D = p if (p is not None) else Parser.newPool("d", self.C, types, self._knownTypes[3])
            p = poolByName.get("g")
            self.G = p if (p is not None) else Parser.newPool("g", self.C, types, self._knownTypes[4])
            p = poolByName.get("h")
            self.H = p if (p is not None) else Parser.newPool("h", self.A, types, self._knownTypes[5])
            p = poolByName.get("i")
            self.I = p if (p is not None) else Parser.newPool("i", self.A, types, self._knownTypes[6])
            p = poolByName.get("j")
            self.J = p if (p is not None) else Parser.newPool("j", self.A, types, self._knownTypes[7])
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
                 
            elif name == "g":
                superPool = P4(len(types), superPool, cls)
                return superPool
                 
            elif name == "h":
                superPool = P5(len(types), superPool, cls)
                return superPool
                 
            elif name == "i":
                superPool = P6(len(types), superPool, cls)
                return superPool
                 
            elif name == "j":
                superPool = P7(len(types), superPool, cls)
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
        super(P0, self).__init__(poolIndex, "a", ["a", "parent"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "a":
            F0(annotation, self)

        elif name == "parent":
            F1(self.owner().A, self)
                
    def addField(self, fType, name):
        if name == "a":
            return F0(fType, self)

        if name == "parent":
            return F1(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, a=None, Parent=None):
        """
        :return a new A instance with the argument field values
        """
        rval = self._cls(-1, a, Parent)
        self.add(rval)
        return rval

class P1(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "b", superPool, [], [None for i in range(0, 0)], cls)


    def make(self, a=None, Parent=None):
        """
        :return a new B instance with the argument field values
        """
        rval = self._cls(-1, a, Parent)
        self.add(rval)
        return rval

class P2(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P2, self).__init__(poolIndex, "c", superPool, ["value"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "value":
            F2(self.owner().C, self)

    def addField(self, fType, name):
        if name == "value":
            return F2(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, Value=None, a=None, Parent=None):
        """
        :return a new C instance with the argument field values
        """
        rval = self._cls(-1, Value, a, Parent)
        self.add(rval)
        return rval

class P3(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P3, self).__init__(poolIndex, "d", superPool, [], [None for i in range(0, 0)], cls)


    def make(self, Value=None, a=None, Parent=None):
        """
        :return a new D instance with the argument field values
        """
        rval = self._cls(-1, Value, a, Parent)
        self.add(rval)
        return rval

class P4(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P4, self).__init__(poolIndex, "g", superPool, ["amap"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "amap":
            F3(MapType(self.owner().C, self.owner().C), self)

    def addField(self, fType, name):
        if name == "amap":
            return F3(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, aMap=None, Value=None, a=None, Parent=None):
        """
        :return a new G instance with the argument field values
        """
        rval = self._cls(-1, aMap, Value, a, Parent)
        self.add(rval)
        return rval

class P5(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P5, self).__init__(poolIndex, "h", superPool, [], [None for i in range(0, 0)], cls)


    def make(self, a=None, Parent=None):
        """
        :return a new H instance with the argument field values
        """
        rval = self._cls(-1, a, Parent)
        self.add(rval)
        return rval

class P6(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P6, self).__init__(poolIndex, "i", superPool, [], [None for i in range(0, 0)], cls)


    def make(self, a=None, Parent=None):
        """
        :return a new I instance with the argument field values
        """
        rval = self._cls(-1, a, Parent)
        self.add(rval)
        return rval

class P7(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P7, self).__init__(poolIndex, "j", superPool, [], [None for i in range(0, 0)], cls)


    def make(self, a=None, Parent=None):
        """
        :return a new J instance with the argument field values
        """
        rval = self._cls(-1, a, Parent)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    annotation A.a
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "a", owner)
        
        if self.fieldType().typeID() != 5:
            raise SkillException("Expected field type annotation in A.a but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].a = t.readSingleField(inStream)


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].a
            if v is None:
                result += 2
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].a, out)


    def get(self, ref):
        return ref.a

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.a = value


class F1(KnownDataField):
    """
    a A.Parent
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "parent", owner)
        
        if fType.name() != "a":
            raise SkillException("Expected field type a in A.Parent but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].Parent = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].Parent
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].Parent
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.Parent

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Parent = value


class F2(KnownDataField):
    """
    c C.Value
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "value", owner)
        
        if fType.name() != "c":
            raise SkillException("Expected field type c in C.Value but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].Value = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].Value
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        for i in range(i, h):
            
            v = d[i].Value
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.Value

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Value = value


class F3(KnownDataField):
    """
    map<c,c> G.aMap
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "amap", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type map<c,c> in G.aMap but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        fType = self.fieldType()
        for i in range(i, h):
            d[i].aMap = fType.readSingleField(inStream)


    def _osc(self, i, h):
        
        fType = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].aMap
            if v is None or len(v) == 0:
                result += 1
            else:
                result += V64.singleV64Offset(len(v))
                result += fType.keyType.calculateOffset(v.keys())
                result += fType.valueType.calculateOffset(v.values())
            
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        fType = self.fieldType()
        for i in range(i, h):
            self.fieldType().writeSingleField(d[i].aMap, out)


    def get(self, ref):
        return ref.aMap

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.aMap = value

