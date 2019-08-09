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
            p = poolByName.get("basicbool")
            self.BasicBool = p if (p is not None) else Parser.newPool("basicbool", None, types, self._knownTypes[0])
            p = poolByName.get("basicfloat32")
            self.BasicFloat32 = p if (p is not None) else Parser.newPool("basicfloat32", None, types, self._knownTypes[1])
            p = poolByName.get("basicfloat64")
            self.BasicFloat64 = p if (p is not None) else Parser.newPool("basicfloat64", None, types, self._knownTypes[2])
            p = poolByName.get("basicfloats")
            self.BasicFloats = p if (p is not None) else Parser.newPool("basicfloats", None, types, self._knownTypes[3])
            p = poolByName.get("basicint16")
            self.BasicInt16 = p if (p is not None) else Parser.newPool("basicint16", None, types, self._knownTypes[4])
            p = poolByName.get("basicint32")
            self.BasicInt32 = p if (p is not None) else Parser.newPool("basicint32", None, types, self._knownTypes[5])
            p = poolByName.get("basicint64i")
            self.BasicInt64I = p if (p is not None) else Parser.newPool("basicint64i", None, types, self._knownTypes[6])
            p = poolByName.get("basicint64v")
            self.BasicInt64V = p if (p is not None) else Parser.newPool("basicint64v", None, types, self._knownTypes[7])
            p = poolByName.get("basicint8")
            self.BasicInt8 = p if (p is not None) else Parser.newPool("basicint8", None, types, self._knownTypes[8])
            p = poolByName.get("basicintegers")
            self.BasicIntegers = p if (p is not None) else Parser.newPool("basicintegers", None, types, self._knownTypes[9])
            p = poolByName.get("basicstring")
            self.BasicString = p if (p is not None) else Parser.newPool("basicstring", None, types, self._knownTypes[10])
            p = poolByName.get("basictypes")
            self.BasicTypes = p if (p is not None) else Parser.newPool("basictypes", None, types, self._knownTypes[11])
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
            if name == "basicbool":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "basicfloat32":
                superPool = P1(len(types), cls)
                return superPool
            elif name == "basicfloat64":
                superPool = P2(len(types), cls)
                return superPool
            elif name == "basicfloats":
                superPool = P3(len(types), cls)
                return superPool
            elif name == "basicint16":
                superPool = P4(len(types), cls)
                return superPool
            elif name == "basicint32":
                superPool = P5(len(types), cls)
                return superPool
            elif name == "basicint64i":
                superPool = P6(len(types), cls)
                return superPool
            elif name == "basicint64v":
                superPool = P7(len(types), cls)
                return superPool
            elif name == "basicint8":
                superPool = P8(len(types), cls)
                return superPool
            elif name == "basicintegers":
                superPool = P9(len(types), cls)
                return superPool
            elif name == "basicstring":
                superPool = P10(len(types), cls)
                return superPool
            elif name == "basictypes":
                superPool = P11(len(types), cls)
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
     Contains a basic bool
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "basicbool", ["basicbool"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "basicbool":
            F0(BoolType(), self)

    def addField(self, fType, name):
        if name == "basicbool":
            return F0(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, basicBool=False):
        """
        :return a new BasicBool instance with the argument field values
        """
        rval = self._cls(-1, basicBool)
        self.add(rval)
        return rval

class P1(BasePool):
    """
     Contains a basic Float32
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "basicfloat32", ["basicfloat"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "basicfloat":
            F1(F32(), self)

    def addField(self, fType, name):
        if name == "basicfloat":
            return F1(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, basicFloat=0.0):
        """
        :return a new BasicFloat32 instance with the argument field values
        """
        rval = self._cls(-1, basicFloat)
        self.add(rval)
        return rval

class P2(BasePool):
    """
     Contains a basic Float64
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P2, self).__init__(poolIndex, "basicfloat64", ["basicfloat"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "basicfloat":
            F2(F64(), self)

    def addField(self, fType, name):
        if name == "basicfloat":
            return F2(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, basicFloat=0.0):
        """
        :return a new BasicFloat64 instance with the argument field values
        """
        rval = self._cls(-1, basicFloat)
        self.add(rval)
        return rval

class P3(BasePool):
    """
     Contains all basic float types
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P3, self).__init__(poolIndex, "basicfloats", ["float32", "float64"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "float32":
            F3(self.owner().BasicFloat32, self)

        elif name == "float64":
            F4(self.owner().BasicFloat64, self)
                
    def addField(self, fType, name):
        if name == "float32":
            return F3(fType, self)

        if name == "float64":
            return F4(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, float32=None, float64=None):
        """
        :return a new BasicFloats instance with the argument field values
        """
        rval = self._cls(-1, float32, float64)
        self.add(rval)
        return rval

class P4(BasePool):
    """
     Contains a basic Int16
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P4, self).__init__(poolIndex, "basicint16", ["basicint"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "basicint":
            F5(I16(), self)

    def addField(self, fType, name):
        if name == "basicint":
            return F5(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, basicInt=0):
        """
        :return a new BasicInt16 instance with the argument field values
        """
        rval = self._cls(-1, basicInt)
        self.add(rval)
        return rval

class P5(BasePool):
    """
     Contains a basic Int32
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P5, self).__init__(poolIndex, "basicint32", ["basicint"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "basicint":
            F6(I32(), self)

    def addField(self, fType, name):
        if name == "basicint":
            return F6(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, basicInt=0):
        """
        :return a new BasicInt32 instance with the argument field values
        """
        rval = self._cls(-1, basicInt)
        self.add(rval)
        return rval

class P6(BasePool):
    """
     Contains a basic Int64 with i64
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P6, self).__init__(poolIndex, "basicint64i", ["basicint"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "basicint":
            F7(I64(), self)

    def addField(self, fType, name):
        if name == "basicint":
            return F7(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, basicInt=0):
        """
        :return a new BasicInt64I instance with the argument field values
        """
        rval = self._cls(-1, basicInt)
        self.add(rval)
        return rval

class P7(BasePool):
    """
     Contains a basic Int64 with v64
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P7, self).__init__(poolIndex, "basicint64v", ["basicint"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "basicint":
            F8(V64(), self)

    def addField(self, fType, name):
        if name == "basicint":
            return F8(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, basicInt=0):
        """
        :return a new BasicInt64V instance with the argument field values
        """
        rval = self._cls(-1, basicInt)
        self.add(rval)
        return rval

class P8(BasePool):
    """
     Contains a basic Int8
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P8, self).__init__(poolIndex, "basicint8", ["basicint"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "basicint":
            F9(I8(), self)

    def addField(self, fType, name):
        if name == "basicint":
            return F9(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, basicInt=0):
        """
        :return a new BasicInt8 instance with the argument field values
        """
        rval = self._cls(-1, basicInt)
        self.add(rval)
        return rval

class P9(BasePool):
    """
     Contains all basic int types
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P9, self).__init__(poolIndex, "basicintegers", ["int16", "int32", "int64i", "int64v", "int8"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "int16":
            F10(self.owner().BasicInt16, self)

        elif name == "int32":
            F11(self.owner().BasicInt32, self)
                
        elif name == "int64i":
            F12(self.owner().BasicInt64I, self)
                
        elif name == "int64v":
            F13(self.owner().BasicInt64V, self)
                
        elif name == "int8":
            F14(self.owner().BasicInt8, self)
                
    def addField(self, fType, name):
        if name == "int16":
            return F10(fType, self)

        if name == "int32":
            return F11(fType, self)

        if name == "int64i":
            return F12(fType, self)

        if name == "int64v":
            return F13(fType, self)

        if name == "int8":
            return F14(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, int16=None, int32=None, int64I=None, int64V=None, int8=None):
        """
        :return a new BasicIntegers instance with the argument field values
        """
        rval = self._cls(-1, int16, int32, int64I, int64V, int8)
        self.add(rval)
        return rval

class P10(BasePool):
    """
     Contains a basic String
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P10, self).__init__(poolIndex, "basicstring", ["basicstring"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "basicstring":
            F15(string, self)

    def addField(self, fType, name):
        if name == "basicstring":
            return F15(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, basicString=None):
        """
        :return a new BasicString instance with the argument field values
        """
        rval = self._cls(-1, basicString)
        self.add(rval)
        return rval

class P11(BasePool):
    """
     Includes all basic types
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P11, self).__init__(poolIndex, "basictypes", ["abool", "alist", "amap", "anannotation", "anarray", "anotherusertype", "aset", "astring", "ausertype"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "abool":
            F16(self.owner().BasicBool, self)

        elif name == "alist":
            F17(ListType(F32()), self)
                
        elif name == "amap":
            F18(MapType(I16(), I8()), self)
                
        elif name == "anannotation":
            F19(annotation, self)
                
        elif name == "anarray":
            F20(VariableLengthArray(self.owner().BasicIntegers), self)
                
        elif name == "anotherusertype":
            F21(self.owner().BasicFloats, self)
                
        elif name == "aset":
            F22(SetType(I8()), self)
                
        elif name == "astring":
            F23(self.owner().BasicString, self)
                
        elif name == "ausertype":
            F24(self.owner().BasicIntegers, self)
                
    def addField(self, fType, name):
        if name == "abool":
            return F16(fType, self)

        if name == "alist":
            return F17(fType, self)

        if name == "amap":
            return F18(fType, self)

        if name == "anannotation":
            return F19(fType, self)

        if name == "anarray":
            return F20(fType, self)

        if name == "anotherusertype":
            return F21(fType, self)

        if name == "aset":
            return F22(fType, self)

        if name == "astring":
            return F23(fType, self)

        if name == "ausertype":
            return F24(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, aBool=None, aList=None, aMap=None, anAnnotation=None, anArray=None, anotherUserType=None, aSet=None, aString=None, aUserType=None):
        """
        :return a new BasicTypes instance with the argument field values
        """
        rval = self._cls(-1, aBool, aList, aMap, anAnnotation, anArray, anotherUserType, aSet, aString, aUserType)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    bool BasicBool.basicBool
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "basicbool", owner)
        
        if self.fieldType().typeID() != 6:
            raise SkillException("Expected field type bool in BasicBool.basicBool but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].basicBool = inStream.bool()


    def _osc(self, i, h):
        self._offset += (h-i)

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.bool(d[i].basicBool)


    def get(self, ref):
        return ref.basicBool

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.basicBool = value


class F1(KnownDataField):
    """
    f32 BasicFloat32.basicFloat
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "basicfloat", owner)
        
        if self.fieldType().typeID() != 12:
            raise SkillException("Expected field type f32 in BasicFloat32.basicFloat but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].basicFloat = inStream.f32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f32(d[i].basicFloat)


    def get(self, ref):
        return ref.basicFloat

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.basicFloat = value


class F2(KnownDataField):
    """
    f64 BasicFloat64.basicFloat
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "basicfloat", owner)
        
        if self.fieldType().typeID() != 13:
            raise SkillException("Expected field type f64 in BasicFloat64.basicFloat but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].basicFloat = inStream.f64()


    def _osc(self, i, h):
        self._offset += (h-i) << 3

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f64(d[i].basicFloat)


    def get(self, ref):
        return ref.basicFloat

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.basicFloat = value


class F3(KnownDataField):
    """
    basicfloat32 BasicFloats.float32
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "float32", owner)
        
        if fType.name() != "basicfloat32":
            raise SkillException("Expected field type basicfloat32 in BasicFloats.float32 but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].float32 = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].float32
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].float32
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.float32

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.float32 = value


class F4(KnownDataField):
    """
    basicfloat64 BasicFloats.float64
    """
    def __init__(self, fType, owner):
        super(F4, self).__init__(fType, "float64", owner)
        
        if fType.name() != "basicfloat64":
            raise SkillException("Expected field type basicfloat64 in BasicFloats.float64 but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].float64 = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].float64
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].float64
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.float64

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.float64 = value


class F5(KnownDataField):
    """
    i16 BasicInt16.basicInt
    """
    def __init__(self, fType, owner):
        super(F5, self).__init__(fType, "basicint", owner)
        
        if self.fieldType().typeID() != 8:
            raise SkillException("Expected field type i16 in BasicInt16.basicInt but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].basicInt = inStream.i16()


    def _osc(self, i, h):
        self._offset += (h-i) << 1

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.i16(d[i].basicInt)


    def get(self, ref):
        return ref.basicInt

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.basicInt = value


class F6(KnownDataField):
    """
    i32 BasicInt32.basicInt
    """
    def __init__(self, fType, owner):
        super(F6, self).__init__(fType, "basicint", owner)
        
        if self.fieldType().typeID() != 9:
            raise SkillException("Expected field type i32 in BasicInt32.basicInt but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].basicInt = inStream.i32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.i32(d[i].basicInt)


    def get(self, ref):
        return ref.basicInt

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.basicInt = value


class F7(KnownDataField):
    """
    i64 BasicInt64I.basicInt
    """
    def __init__(self, fType, owner):
        super(F7, self).__init__(fType, "basicint", owner)
        
        if self.fieldType().typeID() != 10:
            raise SkillException("Expected field type i64 in BasicInt64I.basicInt but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].basicInt = inStream.i64()


    def _osc(self, i, h):
        self._offset += (h-i) << 3

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.i64(d[i].basicInt)


    def get(self, ref):
        return ref.basicInt

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.basicInt = value


class F8(KnownDataField):
    """
    v64 BasicInt64V.basicInt
    """
    def __init__(self, fType, owner):
        super(F8, self).__init__(fType, "basicint", owner)
        
        if self.fieldType().typeID() != 11:
            raise SkillException("Expected field type v64 in BasicInt64V.basicInt but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].basicInt = inStream.v64()


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            result += V64.singleV64Offset(d[i].basicInt)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.v64(d[i].basicInt)


    def get(self, ref):
        return ref.basicInt

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.basicInt = value


class F9(KnownDataField):
    """
    i8 BasicInt8.basicInt
    """
    def __init__(self, fType, owner):
        super(F9, self).__init__(fType, "basicint", owner)
        
        if self.fieldType().typeID() != 7:
            raise SkillException("Expected field type i8 in BasicInt8.basicInt but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].basicInt = inStream.i8()


    def _osc(self, i, h):
        self._offset += (h-i)

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.i8(d[i].basicInt)


    def get(self, ref):
        return ref.basicInt

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.basicInt = value


class F10(KnownDataField):
    """
    basicint16 BasicIntegers.int16
    """
    def __init__(self, fType, owner):
        super(F10, self).__init__(fType, "int16", owner)
        
        if fType.name() != "basicint16":
            raise SkillException("Expected field type basicint16 in BasicIntegers.int16 but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].int16 = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].int16
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].int16
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.int16

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.int16 = value


class F11(KnownDataField):
    """
    basicint32 BasicIntegers.int32
    """
    def __init__(self, fType, owner):
        super(F11, self).__init__(fType, "int32", owner)
        
        if fType.name() != "basicint32":
            raise SkillException("Expected field type basicint32 in BasicIntegers.int32 but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].int32 = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].int32
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].int32
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.int32

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.int32 = value


class F12(KnownDataField):
    """
    basicint64i BasicIntegers.int64I
    """
    def __init__(self, fType, owner):
        super(F12, self).__init__(fType, "int64i", owner)
        
        if fType.name() != "basicint64i":
            raise SkillException("Expected field type basicint64i in BasicIntegers.int64I but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].int64I = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].int64I
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].int64I
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.int64I

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.int64I = value


class F13(KnownDataField):
    """
    basicint64v BasicIntegers.int64V
    """
    def __init__(self, fType, owner):
        super(F13, self).__init__(fType, "int64v", owner)
        
        if fType.name() != "basicint64v":
            raise SkillException("Expected field type basicint64v in BasicIntegers.int64V but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].int64V = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].int64V
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].int64V
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.int64V

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.int64V = value


class F14(KnownDataField):
    """
    basicint8 BasicIntegers.int8
    """
    def __init__(self, fType, owner):
        super(F14, self).__init__(fType, "int8", owner)
        
        if fType.name() != "basicint8":
            raise SkillException("Expected field type basicint8 in BasicIntegers.int8 but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].int8 = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].int8
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].int8
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.int8

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.int8 = value


class F15(KnownDataField):
    """
    string BasicString.basicString
    """
    def __init__(self, fType, owner):
        super(F15, self).__init__(fType, "basicstring", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in BasicString.basicString but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].basicString = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].basicString
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].basicString, out)


    def get(self, ref):
        return ref.basicString

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.basicString = value


class F16(KnownDataField):
    """
    basicbool BasicTypes.aBool
    """
    def __init__(self, fType, owner):
        super(F16, self).__init__(fType, "abool", owner)
        
        if fType.name() != "basicbool":
            raise SkillException("Expected field type basicbool in BasicTypes.aBool but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].aBool = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].aBool
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].aBool
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.aBool

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.aBool = value


class F17(KnownDataField):
    """
    list<f32> BasicTypes.aList
    """
    def __init__(self, fType, owner):
        super(F17, self).__init__(fType, "alist", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type list<f32> in BasicTypes.aList but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            size = inStream.v64()
            v = []
            for k in range(0, size):
                v.append(inStream.f32())
            d[i].aList = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].aList
            if v is None:
                size = 0
            else:
                size = len(v)
            if 0 == size:
                result += 1
            else:
                result += V64.singleV64Offset(size)
                result += (size<<2)
            
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            
            x = d[i].aList
            size = 0 if x is None else len(x)
            if size == 0:
                out.i8(0)
            else:
                out.v64(size)
                for e in x:
                    out.f32(e)

        


    def get(self, ref):
        return ref.aList

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.aList = value


class F18(KnownDataField):
    """
    map<i16,i8> BasicTypes.aMap
    """
    def __init__(self, fType, owner):
        super(F18, self).__init__(fType, "amap", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type map<i16,i8> in BasicTypes.aMap but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
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
        d = self.owner.data()
        fType = self.fieldType()
        for i in range(i, h):
            self.fieldType().writeSingleField(d[i].aMap, out)


    def get(self, ref):
        return ref.aMap

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.aMap = value


class F19(KnownDataField):
    """
    annotation BasicTypes.anAnnotation
    """
    def __init__(self, fType, owner):
        super(F19, self).__init__(fType, "anannotation", owner)
        
        if self.fieldType().typeID() != 5:
            raise SkillException("Expected field type annotation in BasicTypes.anAnnotation but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].anAnnotation = t.readSingleField(inStream)


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].anAnnotation
            if v is None:
                result += 2
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].anAnnotation, out)


    def get(self, ref):
        return ref.anAnnotation

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.anAnnotation = value


class F20(KnownDataField):
    """
    basicintegers[] BasicTypes.anArray
    """
    def __init__(self, fType, owner):
        super(F20, self).__init__(fType, "anarray", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type basicintegers[] in BasicTypes.anArray but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        
        t = fType.groundType
        for i in range(i, h):
            size = inStream.v64()
            v = []
            for k in range(0, size):
                v.append(t.getByID(inStream.v64()))
            d[i].anArray = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].anArray
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
            
            x = d[i].anArray
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
        return ref.anArray

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.anArray = value


class F21(KnownDataField):
    """
    basicfloats BasicTypes.anotherUserType
    """
    def __init__(self, fType, owner):
        super(F21, self).__init__(fType, "anotherusertype", owner)
        
        if fType.name() != "basicfloats":
            raise SkillException("Expected field type basicfloats in BasicTypes.anotherUserType but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].anotherUserType = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].anotherUserType
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].anotherUserType
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.anotherUserType

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.anotherUserType = value


class F22(KnownDataField):
    """
    set<i8> BasicTypes.aSet
    """
    def __init__(self, fType, owner):
        super(F22, self).__init__(fType, "aset", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type set<i8> in BasicTypes.aSet but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            size = inStream.v64()
            v = set()
            t = self.fieldType().groundType
            for k in range(0, size):
                v.add(inStream.i8())
            d[i].aSet = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].aSet
            if v is None:
                size = 0
            else:
                size = len(v)
            if 0 == size:
                result += 1
            else:
                result += V64.singleV64Offset(size)
                result += size
            
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            
            x = d[i].aSet
            size = 0 if x is None else len(x)
            if size == 0:
                out.i8(0)
            else:
                out.v64(size)
                for e in x:
                    out.i8(e)

        


    def get(self, ref):
        return ref.aSet

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.aSet = value


class F23(KnownDataField):
    """
    basicstring BasicTypes.aString
    """
    def __init__(self, fType, owner):
        super(F23, self).__init__(fType, "astring", owner)
        
        if fType.name() != "basicstring":
            raise SkillException("Expected field type basicstring in BasicTypes.aString but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].aString = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].aString
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].aString
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.aString

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.aString = value


class F24(KnownDataField):
    """
    basicintegers BasicTypes.aUserType
    """
    def __init__(self, fType, owner):
        super(F24, self).__init__(fType, "ausertype", owner)
        
        if fType.name() != "basicintegers":
            raise SkillException("Expected field type basicintegers in BasicTypes.aUserType but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].aUserType = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].aUserType
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].aUserType
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.aUserType

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.aUserType = value

