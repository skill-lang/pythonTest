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
            p = poolByName.get("boolean")
            self.Boolean = p if (p is not None) else Parser.newPool("boolean", None, types, self._knownTypes[0])
            p = poolByName.get("if")
            self.If = p if (p is not None) else Parser.newPool("if", None, types, self._knownTypes[1])
            p = poolByName.get("int")
            self.Int = p if (p is not None) else Parser.newPool("int", None, types, self._knownTypes[2])
            p = poolByName.get("∀")
            self.Z2200 = p if (p is not None) else Parser.newPool("∀", None, types, self._knownTypes[3])
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
            if name == "boolean":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "if":
                superPool = P1(len(types), cls)
                return superPool
            elif name == "int":
                superPool = P2(len(types), cls)
                return superPool
            elif name == "∀":
                superPool = P3(len(types), cls)
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
     Representation of another type.
     @note  Caused by a Bug in the C generator.
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "boolean", ["bool", "boolean"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "bool":
            F0(self.owner().Boolean, self)

        elif name == "boolean":
            F1(BoolType(), self)
                
    def addField(self, fType, name):
        if name == "bool":
            return F0(fType, self)

        if name == "boolean":
            return F1(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, Zbool=None, boolean=False):
        """
        :return a new Boolean instance with the argument field values
        """
        rval = self._cls(-1, Zbool, boolean)
        self.add(rval)
        return rval

class P1(BasePool):
    """
     Another stupid typename
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "if", [], [None for i in range(0, 0)], cls)


    def make(self):
        """
        :return a new If instance with the argument field values
        """
        rval = self._cls(-1)
        self.add(rval)
        return rval

class P2(BasePool):
    """
     Stupid typename
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P2, self).__init__(poolIndex, "int", ["for", "if"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "for":
            F2(self.owner().If, self)

        elif name == "if":
            F3(self.owner().Int, self)
                
    def addField(self, fType, name):
        if name == "for":
            return F2(fType, self)

        if name == "if":
            return F3(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, Zfor=None, Zif=None):
        """
        :return a new Int instance with the argument field values
        """
        rval = self._cls(-1, Zfor, Zif)
        self.add(rval)
        return rval

class P3(BasePool):
    """
     non-printable unicode characters
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P3, self).__init__(poolIndex, "∀", ["€", "☢"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "€":
            F4(self.owner().Z2200, self)

        elif name == "☢":
            F5(string, self)
                
    def addField(self, fType, name):
        if name == "€":
            return F4(fType, self)

        if name == "☢":
            return F5(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, euro=None, Z2622=None):
        """
        :return a new Z2200 instance with the argument field values
        """
        rval = self._cls(-1, euro, Z2622)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    boolean Boolean.bool
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "bool", owner)
        
        if fType.name() != "boolean":
            raise SkillException("Expected field type boolean in Boolean.bool but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].Zbool = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].Zbool
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].Zbool
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.Zbool

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Zbool = value


class F1(KnownDataField):
    """
    bool Boolean.boolean
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "boolean", owner)
        
        if self.fieldType().typeID() != 6:
            raise SkillException("Expected field type bool in Boolean.boolean but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].boolean = inStream.bool()


    def _osc(self, i, h):
        self._offset += (h-i)

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.bool(d[i].boolean)


    def get(self, ref):
        return ref.boolean

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.boolean = value


class F2(KnownDataField):
    """
    if Int.for
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "for", owner)
        
        if fType.name() != "if":
            raise SkillException("Expected field type if in Int.for but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].Zfor = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].Zfor
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].Zfor
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.Zfor

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Zfor = value


class F3(KnownDataField):
    """
    int Int.if
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "if", owner)
        
        if fType.name() != "int":
            raise SkillException("Expected field type int in Int.if but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].Zif = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].Zif
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].Zif
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.Zif

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Zif = value


class F4(KnownDataField):
    """
    ∀ ∀.€
    """
    def __init__(self, fType, owner):
        super(F4, self).__init__(fType, "€", owner)
        
        if fType.name() != "∀":
            raise SkillException("Expected field type ∀ in ∀.€ but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].euro = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].euro
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].euro
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.euro

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.euro = value


class F5(KnownDataField):
    """
    string ∀.☢
    """
    def __init__(self, fType, owner):
        super(F5, self).__init__(fType, "☢", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in ∀.☢ but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].Z2622 = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].Z2622
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].Z2622, out)


    def get(self, ref):
        return ref.Z2622

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Z2622 = value

