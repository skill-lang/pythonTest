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
            p = poolByName.get("comment")
            self.Comment = p if (p is not None) else Parser.newPool("comment", None, types, self._knownTypes[0])
            p = poolByName.get("defaultboardercases")
            self.DefaultBoarderCases = p if (p is not None) else Parser.newPool("defaultboardercases", None, types, self._knownTypes[1])
            p = poolByName.get("operator")
            self.Operator = p if (p is not None) else Parser.newPool("operator", None, types, self._knownTypes[2])
            p = poolByName.get("properties")
            self.Properties = p if (p is not None) else Parser.newPool("properties", None, types, self._knownTypes[3])
            p = poolByName.get("none")
            self.ZNone = p if (p is not None) else Parser.newPool("none", self.Properties, types, self._knownTypes[4])
            p = poolByName.get("regularproperty")
            self.RegularProperty = p if (p is not None) else Parser.newPool("regularproperty", self.Properties, types, self._knownTypes[5])
            p = poolByName.get("system")
            self.System = p if (p is not None) else Parser.newPool("system", self.Properties, types, self._knownTypes[6])
            p = poolByName.get("rangeboardercases")
            self.RangeBoarderCases = p if (p is not None) else Parser.newPool("rangeboardercases", None, types, self._knownTypes[7])
            p = poolByName.get("term")
            self.Term = p if (p is not None) else Parser.newPool("term", None, types, self._knownTypes[8])
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
            if name == "comment":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "defaultboardercases":
                superPool = P1(len(types), cls)
                return superPool
            elif name == "operator":
                superPool = P2(len(types), cls)
                return superPool
            elif name == "properties":
                superPool = P3(len(types), cls)
                return superPool
            elif name == "none":
                superPool = P4(len(types), superPool, cls)
                return superPool
                 
            elif name == "regularproperty":
                superPool = P5(len(types), superPool, cls)
                return superPool
                 
            elif name == "system":
                superPool = P6(len(types), superPool, cls)
                return superPool
                 
            elif name == "rangeboardercases":
                superPool = P7(len(types), cls)
                return superPool
            elif name == "term":
                superPool = P8(len(types), cls)
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
        super(P0, self).__init__(poolIndex, "comment", ["property", "target", "text"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "property":
            F0(self.owner().Properties, self)

        elif name == "target":
            F1(annotation, self)
                
        elif name == "text":
            F2(string, self)
                
    def addField(self, fType, name):
        if name == "property":
            return F0(fType, self)

        if name == "target":
            return F1(fType, self)

        if name == "text":
            return F2(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, Zproperty=None, target=None, text=None):
        """
        :return a new Comment instance with the argument field values
        """
        rval = self._cls(-1, Zproperty, target, text)
        self.add(rval)
        return rval

class P1(BasePool):

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "defaultboardercases", ["float", "message", "none", "nopdefault", "system"], [None for i in range(0, 1)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "float":
            F3(F32(), self)

        elif name == "message":
            F4(string, self)
                
        elif name == "none":
            F5(self.owner().Properties, self)
                
        elif name == "nopdefault":
            F6(V64(), self)
                
        elif name == "system":
            F7(annotation, self)
                
    def addField(self, fType, name):
        if name == "float":
            return F3(fType, self)

        if name == "message":
            return F4(fType, self)

        if name == "none":
            return F5(fType, self)

        if name == "nopdefault":
            return F6(fType, self)

        elif name == "system":
            raise SkillException(
                "The file contains a field declaration %s.%s, but there is an auto field of similar name!".format(
                    self.name(), name))
        else:
            return LazyField(fType, name, self)

    def make(self, Zfloat=0.0, message=None, none=None, nopDefault=0, system=None):
        """
        :return a new DefaultBoarderCases instance with the argument field values
        """
        rval = self._cls(-1, Zfloat, message, none, nopDefault, system)
        self.add(rval)
        return rval

class P2(BasePool):

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P2, self).__init__(poolIndex, "operator", ["name"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "name":
            F8(string, self)

    def addField(self, fType, name):
        if name == "name":
            return F8(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, name=None):
        """
        :return a new Operator instance with the argument field values
        """
        rval = self._cls(-1, name)
        self.add(rval)
        return rval

class P3(BasePool):

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P3, self).__init__(poolIndex, "properties", [], [None for i in range(0, 0)], cls)


    def make(self):
        """
        :return a new Properties instance with the argument field values
        """
        rval = self._cls(-1)
        self.add(rval)
        return rval

class P4(StoragePool):

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P4, self).__init__(poolIndex, "none", superPool, [], [None for i in range(0, 0)], cls)


    def make(self):
        """
        :return a new ZNone instance with the argument field values
        """
        rval = self._cls(-1)
        self.add(rval)
        return rval

class P5(StoragePool):
    """
     some regular property
    """

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P5, self).__init__(poolIndex, "regularproperty", superPool, [], [None for i in range(0, 0)], cls)


    def make(self):
        """
        :return a new RegularProperty instance with the argument field values
        """
        rval = self._cls(-1)
        self.add(rval)
        return rval

class P6(StoragePool):
    """
     some properties of the target system
    """

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P6, self).__init__(poolIndex, "system", superPool, ["name", "version"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "name":
            F9(string, self)

        elif name == "version":
            F10(F32(), self)
                
    def addField(self, fType, name):
        if name == "name":
            return F9(fType, self)

        if name == "version":
            return F10(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, name=None, version=0.0):
        """
        :return a new System instance with the argument field values
        """
        rval = self._cls(-1, name, version)
        self.add(rval)
        return rval

class P7(BasePool):

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P7, self).__init__(poolIndex, "rangeboardercases", ["degrees", "degrees2", "negative", "negative2", "positive", "positive2"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "degrees":
            F11(F32(), self)

        elif name == "degrees2":
            F12(F64(), self)
                
        elif name == "negative":
            F13(I32(), self)
                
        elif name == "negative2":
            F14(V64(), self)
                
        elif name == "positive":
            F15(I8(), self)
                
        elif name == "positive2":
            F16(I16(), self)
                
    def addField(self, fType, name):
        if name == "degrees":
            return F11(fType, self)

        if name == "degrees2":
            return F12(fType, self)

        if name == "negative":
            return F13(fType, self)

        if name == "negative2":
            return F14(fType, self)

        if name == "positive":
            return F15(fType, self)

        if name == "positive2":
            return F16(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, degrees=0.0, degrees2=0.0, negative=0, negative2=0, positive=0, positive2=0):
        """
        :return a new RangeBoarderCases instance with the argument field values
        """
        rval = self._cls(-1, degrees, degrees2, negative, negative2, positive, positive2)
        self.add(rval)
        return rval

class P8(BasePool):

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P8, self).__init__(poolIndex, "term", ["arguments", "operator"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "arguments":
            F17(VariableLengthArray(self.owner().Term), self)

        elif name == "operator":
            F18(self.owner().Operator, self)
                
    def addField(self, fType, name):
        if name == "arguments":
            return F17(fType, self)

        if name == "operator":
            return F18(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, arguments=None, operator=None):
        """
        :return a new Term instance with the argument field values
        """
        rval = self._cls(-1, arguments, operator)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    properties Comment.property
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "property", owner)
        
        if fType.name() != "properties":
            raise SkillException("Expected field type properties in Comment.property but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].Zproperty = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].Zproperty
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].Zproperty
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.Zproperty

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Zproperty = value


class F1(KnownDataField):
    """
    annotation Comment.target
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "target", owner)
        
        if self.fieldType().typeID() != 5:
            raise SkillException("Expected field type annotation in Comment.target but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].target = t.readSingleField(inStream)


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].target
            if v is None:
                result += 2
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].target, out)


    def get(self, ref):
        return ref.target

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.target = value


class F2(KnownDataField):
    """
    string Comment.text
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "text", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in Comment.text but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].text = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].text
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].text, out)


    def get(self, ref):
        return ref.text

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.text = value


class F3(KnownDataField):
    """
    f32 DefaultBoarderCases.float
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "float", owner)
        
        if self.fieldType().typeID() != 12:
            raise SkillException("Expected field type f32 in DefaultBoarderCases.float but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].Zfloat = inStream.f32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f32(d[i].Zfloat)


    def get(self, ref):
        return ref.Zfloat

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Zfloat = value


class F4(KnownDataField):
    """
    string DefaultBoarderCases.message
    """
    def __init__(self, fType, owner):
        super(F4, self).__init__(fType, "message", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in DefaultBoarderCases.message but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].message = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].message
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].message, out)


    def get(self, ref):
        return ref.message

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.message = value


class F5(KnownDataField):
    """
    properties DefaultBoarderCases.none
    """
    def __init__(self, fType, owner):
        super(F5, self).__init__(fType, "none", owner)
        
        if fType.name() != "properties":
            raise SkillException("Expected field type properties in DefaultBoarderCases.none but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].none = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].none
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].none
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.none

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.none = value


class F6(KnownDataField):
    """
    v64 DefaultBoarderCases.nopDefault
    """
    def __init__(self, fType, owner):
        super(F6, self).__init__(fType, "nopdefault", owner)
        
        if self.fieldType().typeID() != 11:
            raise SkillException("Expected field type v64 in DefaultBoarderCases.nopDefault but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].nopDefault = inStream.v64()


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            result += V64.singleV64Offset(d[i].nopDefault)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.v64(d[i].nopDefault)


    def get(self, ref):
        return ref.nopDefault

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.nopDefault = value


class F7(AutoField):
    """
    annotation DefaultBoarderCases.system
    """
    def __init__(self, fType, owner):
        super(F7, self).__init__(fType, "system", owner, 0)
        

    
    def get(self, ref):
        return ref.system

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.system = value


class F8(KnownDataField):
    """
    string Operator.name
    """
    def __init__(self, fType, owner):
        super(F8, self).__init__(fType, "name", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in Operator.name but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].name = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].name
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].name, out)


    def get(self, ref):
        return ref.name

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.name = value


class F9(KnownDataField):
    """
    string System.name
    """
    def __init__(self, fType, owner):
        super(F9, self).__init__(fType, "name", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in System.name but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].name = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].name
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].name, out)


    def get(self, ref):
        return ref.name

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.name = value


class F10(KnownDataField):
    """
    f32 System.version
    """
    def __init__(self, fType, owner):
        super(F10, self).__init__(fType, "version", owner)
        
        if self.fieldType().typeID() != 12:
            raise SkillException("Expected field type f32 in System.version but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        for i in range(i, h):
            d[i].version = inStream.f32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        for i in range(i, h):
            out.f32(d[i].version)


    def get(self, ref):
        return ref.version

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.version = value


class F11(KnownDataField):
    """
    f32 RangeBoarderCases.degrees
    """
    def __init__(self, fType, owner):
        super(F11, self).__init__(fType, "degrees", owner)
        
        if self.fieldType().typeID() != 12:
            raise SkillException("Expected field type f32 in RangeBoarderCases.degrees but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].degrees = inStream.f32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f32(d[i].degrees)


    def get(self, ref):
        return ref.degrees

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.degrees = value


class F12(KnownDataField):
    """
    f64 RangeBoarderCases.degrees2
    """
    def __init__(self, fType, owner):
        super(F12, self).__init__(fType, "degrees2", owner)
        
        if self.fieldType().typeID() != 13:
            raise SkillException("Expected field type f64 in RangeBoarderCases.degrees2 but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].degrees2 = inStream.f64()


    def _osc(self, i, h):
        self._offset += (h-i) << 3

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.f64(d[i].degrees2)


    def get(self, ref):
        return ref.degrees2

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.degrees2 = value


class F13(KnownDataField):
    """
    i32 RangeBoarderCases.negative
    """
    def __init__(self, fType, owner):
        super(F13, self).__init__(fType, "negative", owner)
        
        if self.fieldType().typeID() != 9:
            raise SkillException("Expected field type i32 in RangeBoarderCases.negative but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].negative = inStream.i32()


    def _osc(self, i, h):
        self._offset += (h-i) << 2

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.i32(d[i].negative)


    def get(self, ref):
        return ref.negative

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.negative = value


class F14(KnownDataField):
    """
    v64 RangeBoarderCases.negative2
    """
    def __init__(self, fType, owner):
        super(F14, self).__init__(fType, "negative2", owner)
        
        if self.fieldType().typeID() != 11:
            raise SkillException("Expected field type v64 in RangeBoarderCases.negative2 but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].negative2 = inStream.v64()


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            result += V64.singleV64Offset(d[i].negative2)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.v64(d[i].negative2)


    def get(self, ref):
        return ref.negative2

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.negative2 = value


class F15(KnownDataField):
    """
    i8 RangeBoarderCases.positive
    """
    def __init__(self, fType, owner):
        super(F15, self).__init__(fType, "positive", owner)
        
        if self.fieldType().typeID() != 7:
            raise SkillException("Expected field type i8 in RangeBoarderCases.positive but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].positive = inStream.i8()


    def _osc(self, i, h):
        self._offset += (h-i)

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.i8(d[i].positive)


    def get(self, ref):
        return ref.positive

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.positive = value


class F16(KnownDataField):
    """
    i16 RangeBoarderCases.positive2
    """
    def __init__(self, fType, owner):
        super(F16, self).__init__(fType, "positive2", owner)
        
        if self.fieldType().typeID() != 8:
            raise SkillException("Expected field type i16 in RangeBoarderCases.positive2 but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].positive2 = inStream.i16()


    def _osc(self, i, h):
        self._offset += (h-i) << 1

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.i16(d[i].positive2)


    def get(self, ref):
        return ref.positive2

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.positive2 = value


class F17(KnownDataField):
    """
    term[] Term.arguments
    """
    def __init__(self, fType, owner):
        super(F17, self).__init__(fType, "arguments", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type term[] in Term.arguments but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        
        t = fType.groundType
        for i in range(i, h):
            size = inStream.v64()
            v = []
            for k in range(0, size):
                v.append(t.getByID(inStream.v64()))
            d[i].arguments = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].arguments
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
            
            x = d[i].arguments
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
        return ref.arguments

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.arguments = value


class F18(KnownDataField):
    """
    operator Term.operator
    """
    def __init__(self, fType, owner):
        super(F18, self).__init__(fType, "operator", owner)
        
        if fType.name() != "operator":
            raise SkillException("Expected field type operator in Term.operator but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].operator = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].operator
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            
            v = d[i].operator
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.operator

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.operator = value

