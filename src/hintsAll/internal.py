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
            p = poolByName.get("abuser")
            self.Abuser = p if (p is not None) else Parser.newPool("abuser", None, types, self._knownTypes[0])
            p = poolByName.get("badtype")
            self.BadType = p if (p is not None) else Parser.newPool("badtype", None, types, self._knownTypes[1])
            p = poolByName.get("expression")
            self.Expression = p if (p is not None) else Parser.newPool("expression", None, types, self._knownTypes[2])
            p = poolByName.get("externmixin")
            self.ExternMixin = p if (p is not None) else Parser.newPool("externmixin", None, types, self._knownTypes[3])
            p = poolByName.get("nowasingleton")
            self.NowASingleton = p if (p is not None) else Parser.newPool("nowasingleton", None, types, self._knownTypes[4])
            p = poolByName.get("uid")
            self.UID = p if (p is not None) else Parser.newPool("uid", None, types, self._knownTypes[5])
            p = poolByName.get("user")
            self.User = p if (p is not None) else Parser.newPool("user", None, types, self._knownTypes[6])
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
            if name == "abuser":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "badtype":
                superPool = P1(len(types), cls)
                return superPool
            elif name == "expression":
                superPool = P2(len(types), cls)
                return superPool
            elif name == "externmixin":
                superPool = P3(len(types), cls)
                return superPool
            elif name == "nowasingleton":
                superPool = P4(len(types), cls)
                return superPool
            elif name == "uid":
                superPool = P5(len(types), cls)
                return superPool
            elif name == "user":
                superPool = P6(len(types), cls)
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
     Just for fun
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "abuser", ["abusedescription"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "abusedescription":
            F0(string, self)

    def addField(self, fType, name):
        if name == "abusedescription":
            return F0(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, abuseDescription=None):
        """
        :return a new Abuser instance with the argument field values
        """
        rval = self._cls(-1, abuseDescription)
        self.add(rval)
        return rval

class P1(BasePool):

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "badtype", ["ignoreddata", "reflectivelyinvisible"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "ignoreddata":
            F1(string, self)

        elif name == "reflectivelyinvisible":
            F2(string, self)
                
    def addField(self, fType, name):
        if name == "ignoreddata":
            return F1(fType, self)

        if name == "reflectivelyinvisible":
            return F2(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, ignoredData=None, reflectivelyInVisible=None):
        """
        :return a new BadType instance with the argument field values
        """
        rval = self._cls(-1, ignoredData, reflectivelyInVisible)
        self.add(rval)
        return rval

class P2(BasePool):
    """
     all expressions are pure
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P2, self).__init__(poolIndex, "expression", [], [None for i in range(0, 0)], cls)


    def make(self):
        """
        :return a new Expression instance with the argument field values
        """
        rval = self._cls(-1)
        self.add(rval)
        return rval

class P3(BasePool):
    """
     A type mixed into our hirarchy.
     @todo  provide tests for programming languages using actual user defined implementations
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P3, self).__init__(poolIndex, "externmixin", ["unknownstuff"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "unknownstuff":
            F3(annotation, self)

    def addField(self, fType, name):
        if name == "unknownstuff":
            return F3(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, unknownStuff=None):
        """
        :return a new ExternMixin instance with the argument field values
        """
        rval = self._cls(-1, unknownStuff)
        self.add(rval)
        return rval

class P4(BasePool):
    """
     what ever it was before, now it is a singleton
     @todo  provide a test binary to check this hint (where it should be abstract; and a fail, where it has a subclass,
     because it can not be a singleton in that case)
     @note  this is readOnly; should not matter, because it has no mutable state
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P4, self).__init__(poolIndex, "nowasingleton", ["guard"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "guard":
            F4(ConstantI16(43981), self)

    def addField(self, fType, name):
        if name == "guard":
            return F4(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self):
        """
        :return a new NowASingleton instance with the argument field values
        """
        rval = self._cls(-1)
        self.add(rval)
        return rval

class P5(BasePool):
    """
     Unique Identifiers are unique and appear as if they were longs
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P5, self).__init__(poolIndex, "uid", ["identifier"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "identifier":
            F5(I64(), self)

    def addField(self, fType, name):
        if name == "identifier":
            return F5(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, identifier=0):
        """
        :return a new UID instance with the argument field values
        """
        rval = self._cls(-1, identifier)
        self.add(rval)
        return rval

class P6(BasePool):
    """
     A user has a name and an age.
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P6, self).__init__(poolIndex, "user", ["age", "name", "reflectivelyvisible"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "age":
            F6(V64(), self)

        elif name == "name":
            F7(string, self)
                
        elif name == "reflectivelyvisible":
            F8(string, self)
                
    def addField(self, fType, name):
        if name == "age":
            return F6(fType, self)

        if name == "name":
            return F7(fType, self)

        if name == "reflectivelyvisible":
            return F8(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, age=0, name=None, reflectivelyVisible=None):
        """
        :return a new User instance with the argument field values
        """
        rval = self._cls(-1, age, name, reflectivelyVisible)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    string Abuser.abuseDescription
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "abusedescription", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in Abuser.abuseDescription but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].abuseDescription = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].abuseDescription
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].abuseDescription, out)


    def get(self, ref):
        return ref.abuseDescription

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.abuseDescription = value


class F1(KnownDataField):
    """
    string BadType.ignoredData
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "ignoreddata", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in BadType.ignoredData but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].ignoredData = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].ignoredData
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].ignoredData, out)


    def get(self, ref):
        return ref.ignoredData

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.ignoredData = value


class F2(KnownDataField):
    """
    string BadType.reflectivelyInVisible
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "reflectivelyinvisible", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in BadType.reflectivelyInVisible but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].reflectivelyInVisible = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].reflectivelyInVisible
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].reflectivelyInVisible, out)


    def get(self, ref):
        return ref.reflectivelyInVisible

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.reflectivelyInVisible = value


class F3(KnownDataField):
    """
    annotation ExternMixin.unknownStuff
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "unknownstuff", owner)
        
        if self.fieldType().typeID() != 5:
            raise SkillException("Expected field type annotation in ExternMixin.unknownStuff but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].unknownStuff = t.readSingleField(inStream)


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].unknownStuff
            if v is None:
                result += 2
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].unknownStuff, out)


    def get(self, ref):
        return ref.unknownStuff

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.unknownStuff = value


class F4(KnownDataField):
    """
    i16 NowASingleton.guard
    """
    def __init__(self, fType, owner):
        super(F4, self).__init__(fType, "guard", owner)
        
        if self.fieldType().typeID() != 1:
            raise SkillException("Expected field type i16 in NowASingleton.guard but found {}".format(fType))

    
    def _rsc(self, i, h, inStream): pass

    def _osc(self, i, h): pass

    def _wsc(self, i, h, outStream): pass

    def get(self, ref):
        return ref.guard

    def set(self, ref, value):
        raise Exception("guard is a constant!")


class F5(KnownDataField):
    """
    i64 UID.identifier
    """
    def __init__(self, fType, owner):
        super(F5, self).__init__(fType, "identifier", owner)
        
        if self.fieldType().typeID() != 10:
            raise SkillException("Expected field type i64 in UID.identifier but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].identifier = inStream.i64()


    def _osc(self, i, h):
        self._offset += (h-i) << 3

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.i64(d[i].identifier)


    def get(self, ref):
        return ref.identifier

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.identifier = value


class F6(KnownDataField):
    """
    v64 User.age
    """
    def __init__(self, fType, owner):
        super(F6, self).__init__(fType, "age", owner)
        
        if self.fieldType().typeID() != 11:
            raise SkillException("Expected field type v64 in User.age but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].age = inStream.v64()


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            result += V64.singleV64Offset(d[i].age)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            out.v64(d[i].age)


    def get(self, ref):
        return ref.age

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.age = value


class F7(KnownDataField):
    """
    string User.name
    """
    def __init__(self, fType, owner):
        super(F7, self).__init__(fType, "name", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in User.name but found {}".format(fType))

    
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


class F8(KnownDataField):
    """
    string User.reflectivelyVisible
    """
    def __init__(self, fType, owner):
        super(F8, self).__init__(fType, "reflectivelyvisible", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in User.reflectivelyVisible but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].reflectivelyVisible = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].reflectivelyVisible
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].reflectivelyVisible, out)


    def get(self, ref):
        return ref.reflectivelyVisible

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.reflectivelyVisible = value

