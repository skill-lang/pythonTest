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
            p = poolByName.get("doubletest")
            self.DoubleTest = p if (p is not None) else Parser.newPool("doubletest", None, types, self._knownTypes[0])
            p = poolByName.get("floattest")
            self.FloatTest = p if (p is not None) else Parser.newPool("floattest", None, types, self._knownTypes[1])
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
            if name == "doubletest":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "floattest":
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
     check some double values.
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "doubletest", ["minuszero", "nan", "pi", "two", "zero"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "minuszero":
            F0(F64(), self)

        elif name == "nan":
            F1(F64(), self)
                
        elif name == "pi":
            F2(F64(), self)
                
        elif name == "two":
            F3(F64(), self)
                
        elif name == "zero":
            F4(F64(), self)
                
    def addField(self, fType, name):
        if name == "minuszero":
            return F0(fType, self)

        if name == "nan":
            return F1(fType, self)

        if name == "pi":
            return F2(fType, self)

        if name == "two":
            return F3(fType, self)

        if name == "zero":
            return F4(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, minusZZero=0.0, NaN=0.0, pi=0.0, two=0.0, zero=0.0):
        """
        :return a new DoubleTest instance with the argument field values
        """
        rval = self._cls(-1, minusZZero, NaN, pi, two, zero)
        self.add(rval)
        return rval

class P1(BasePool):
    """
     check some float values.
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "floattest", ["minuszero", "nan", "pi", "two", "zero"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "minuszero":
            F5(F32(), self)

        elif name == "nan":
            F6(F32(), self)
                
        elif name == "pi":
            F7(F32(), self)
                
        elif name == "two":
            F8(F32(), self)
                
        elif name == "zero":
            F9(F32(), self)
                
    def addField(self, fType, name):
        if name == "minuszero":
            return F5(fType, self)

        if name == "nan":
            return F6(fType, self)

        if name == "pi":
            return F7(fType, self)

        if name == "two":
            return F8(fType, self)

        if name == "zero":
            return F9(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, minusZZero=0.0, NaN=0.0, pi=0.0, two=0.0, zero=0.0):
        """
        :return a new FloatTest instance with the argument field values
        """
        rval = self._cls(-1, minusZZero, NaN, pi, two, zero)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    f64 DoubleTest.minusZero
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "minuszero", owner)
        
        if self.fieldType().typeID() != 13:
            raise SkillException("Expected field type f64 in DoubleTest.minusZero but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].minusZZero = inStream.f64()


    def _osc(self, i, h):
        self._offset += (h-i) << 3

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f64(d[i].minusZZero)


    def get(self, ref):
        return ref.minusZZero

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.minusZZero = value


class F1(KnownDataField):
    """
    f64 DoubleTest.NaN
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "nan", owner)
        
        if self.fieldType().typeID() != 13:
            raise SkillException("Expected field type f64 in DoubleTest.NaN but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].NaN = inStream.f64()


    def _osc(self, i, h):
        self._offset += (h-i) << 3

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f64(d[i].NaN)


    def get(self, ref):
        return ref.NaN

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.NaN = value


class F2(KnownDataField):
    """
    f64 DoubleTest.pi
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "pi", owner)
        
        if self.fieldType().typeID() != 13:
            raise SkillException("Expected field type f64 in DoubleTest.pi but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].pi = inStream.f64()


    def _osc(self, i, h):
        self._offset += (h-i) << 3

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f64(d[i].pi)


    def get(self, ref):
        return ref.pi

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.pi = value


class F3(KnownDataField):
    """
    f64 DoubleTest.two
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "two", owner)
        
        if self.fieldType().typeID() != 13:
            raise SkillException("Expected field type f64 in DoubleTest.two but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].two = inStream.f64()


    def _osc(self, i, h):
        self._offset += (h-i) << 3

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f64(d[i].two)


    def get(self, ref):
        return ref.two

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.two = value


class F4(KnownDataField):
    """
    f64 DoubleTest.zero
    """
    def __init__(self, fType, owner):
        super(F4, self).__init__(fType, "zero", owner)
        
        if self.fieldType().typeID() != 13:
            raise SkillException("Expected field type f64 in DoubleTest.zero but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].zero = inStream.f64()


    def _osc(self, i, h):
        self._offset += (h-i) << 3

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f64(d[i].zero)


    def get(self, ref):
        return ref.zero

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.zero = value


class F5(KnownDataField):
    """
    f32 FloatTest.minusZero
    """
    def __init__(self, fType, owner):
        super(F5, self).__init__(fType, "minuszero", owner)
        
        if self.fieldType().typeID() != 12:
            raise SkillException("Expected field type f32 in FloatTest.minusZero but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].minusZZero = inStream.f32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f32(d[i].minusZZero)


    def get(self, ref):
        return ref.minusZZero

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.minusZZero = value


class F6(KnownDataField):
    """
    f32 FloatTest.NaN
    """
    def __init__(self, fType, owner):
        super(F6, self).__init__(fType, "nan", owner)
        
        if self.fieldType().typeID() != 12:
            raise SkillException("Expected field type f32 in FloatTest.NaN but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].NaN = inStream.f32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f32(d[i].NaN)


    def get(self, ref):
        return ref.NaN

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.NaN = value


class F7(KnownDataField):
    """
    f32 FloatTest.pi
    """
    def __init__(self, fType, owner):
        super(F7, self).__init__(fType, "pi", owner)
        
        if self.fieldType().typeID() != 12:
            raise SkillException("Expected field type f32 in FloatTest.pi but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].pi = inStream.f32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f32(d[i].pi)


    def get(self, ref):
        return ref.pi

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.pi = value


class F8(KnownDataField):
    """
    f32 FloatTest.two
    """
    def __init__(self, fType, owner):
        super(F8, self).__init__(fType, "two", owner)
        
        if self.fieldType().typeID() != 12:
            raise SkillException("Expected field type f32 in FloatTest.two but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].two = inStream.f32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f32(d[i].two)


    def get(self, ref):
        return ref.two

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.two = value


class F9(KnownDataField):
    """
    f32 FloatTest.zero
    """
    def __init__(self, fType, owner):
        super(F9, self).__init__(fType, "zero", owner)
        
        if self.fieldType().typeID() != 12:
            raise SkillException("Expected field type f32 in FloatTest.zero but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].zero = inStream.f32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f32(d[i].zero)


    def get(self, ref):
        return ref.zero

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.zero = value

