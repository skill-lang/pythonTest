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
            p = poolByName.get("constant")
            self.Constant = p if (p is not None) else Parser.newPool("constant", None, types, self._knownTypes[0])
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
            if name == "constant":
                superPool = P0(len(types), cls)
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
     Check for constant integerers.
     @author  Dennis Przytarski
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "constant", ["a", "b", "c", "d", "e"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "a":
            F0(ConstantI8(8), self)

        elif name == "b":
            F1(ConstantI16(16), self)
                
        elif name == "c":
            F2(ConstantI32(32), self)
                
        elif name == "d":
            F3(ConstantI64(64), self)
                
        elif name == "e":
            F4(ConstantV64(46), self)
                
    def addField(self, fType, name):
        if name == "a":
            return F0(fType, self)

        if name == "b":
            return F1(fType, self)

        if name == "c":
            return F2(fType, self)

        if name == "d":
            return F3(fType, self)

        if name == "e":
            return F4(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self):
        """
        :return a new Constant instance with the argument field values
        """
        rval = self._cls(-1)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    i8 Constant.a
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "a", owner)
        
        if self.fieldType().typeID() != 0:
            raise SkillException("Expected field type i8 in Constant.a but found {}".format(fType))

    
    def _rsc(self, i, h, inStream): pass

    def _osc(self, i, h): pass

    def _wsc(self, i, h, outStream): pass

    def get(self, ref):
        return ref.a

    def set(self, ref, value):
        raise Exception("a is a constant!")


class F1(KnownDataField):
    """
    i16 Constant.b
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "b", owner)
        
        if self.fieldType().typeID() != 1:
            raise SkillException("Expected field type i16 in Constant.b but found {}".format(fType))

    
    def _rsc(self, i, h, inStream): pass

    def _osc(self, i, h): pass

    def _wsc(self, i, h, outStream): pass

    def get(self, ref):
        return ref.b

    def set(self, ref, value):
        raise Exception("b is a constant!")


class F2(KnownDataField):
    """
    i32 Constant.c
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "c", owner)
        
        if self.fieldType().typeID() != 2:
            raise SkillException("Expected field type i32 in Constant.c but found {}".format(fType))

    
    def _rsc(self, i, h, inStream): pass

    def _osc(self, i, h): pass

    def _wsc(self, i, h, outStream): pass

    def get(self, ref):
        return ref.c

    def set(self, ref, value):
        raise Exception("c is a constant!")


class F3(KnownDataField):
    """
    i64 Constant.d
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "d", owner)
        
        if self.fieldType().typeID() != 3:
            raise SkillException("Expected field type i64 in Constant.d but found {}".format(fType))

    
    def _rsc(self, i, h, inStream): pass

    def _osc(self, i, h): pass

    def _wsc(self, i, h, outStream): pass

    def get(self, ref):
        return ref.d

    def set(self, ref, value):
        raise Exception("d is a constant!")


class F4(KnownDataField):
    """
    v64 Constant.e
    """
    def __init__(self, fType, owner):
        super(F4, self).__init__(fType, "e", owner)
        
        if self.fieldType().typeID() != 4:
            raise SkillException("Expected field type v64 in Constant.e but found {}".format(fType))

    
    def _rsc(self, i, h, inStream): pass

    def _osc(self, i, h): pass

    def _wsc(self, i, h, outStream): pass

    def get(self, ref):
        return ref.e

    def set(self, ref, value):
        raise Exception("e is a constant!")

