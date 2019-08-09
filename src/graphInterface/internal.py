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
            p = poolByName.get("colorholder")
            self.ColorHolder = p if (p is not None) else Parser.newPool("colorholder", None, types, self._knownTypes[0])
            p = poolByName.get("abstractnode")
            self.AbstractNode = p if (p is not None) else Parser.newPool("abstractnode", None, types, self._knownTypes[1])
            p = poolByName.get("node")
            self.Node = p if (p is not None) else Parser.newPool("node", self.AbstractNode, types, self._knownTypes[2])
            p = poolByName.get("subnode")
            self.SubNode = p if (p is not None) else Parser.newPool("subnode", self.Node, types, self._knownTypes[3])
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
            if name == "colorholder":
                superPool = P0(len(types), cls)
                return superPool
            elif name == "abstractnode":
                superPool = P1(len(types), cls)
                return superPool
            elif name == "node":
                superPool = P2(len(types), superPool, cls)
                return superPool
                 
            elif name == "subnode":
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
    """
     check that abstract colors are in fact annotations
    """

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P0, self).__init__(poolIndex, "colorholder", ["anabstractnode", "anannotation"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "anabstractnode":
            F0(self.owner().AbstractNode, self)

        elif name == "anannotation":
            F1(annotation, self)
                
    def addField(self, fType, name):
        if name == "anabstractnode":
            return F0(fType, self)

        if name == "anannotation":
            return F1(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, anAbstractNode=None, anAnnotation=None):
        """
        :return a new ColorHolder instance with the argument field values
        """
        rval = self._cls(-1, anAbstractNode, anAnnotation)
        self.add(rval)
        return rval

class P1(BasePool):

    def __init__(self, poolIndex, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P1, self).__init__(poolIndex, "abstractnode", ["edges", "map"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "edges":
            F2(SetType(self.owner().AbstractNode), self)

        elif name == "map":
            F3(MapType(self.owner().Node, MapType(self.owner().AbstractNode, annotation)), self)
                
    def addField(self, fType, name):
        if name == "edges":
            return F2(fType, self)

        if name == "map":
            return F3(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, edges=None, Zmap=None):
        """
        :return a new AbstractNode instance with the argument field values
        """
        rval = self._cls(-1, edges, Zmap)
        self.add(rval)
        return rval

class P2(StoragePool):
    """
     a graph of colored nodes
    """

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P2, self).__init__(poolIndex, "node", superPool, ["next", "color", "mark"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "next":
            F4(annotation, self)

        elif name == "color":
            F5(string, self)
                
        elif name == "mark":
            F6(string, self)
                
    def addField(self, fType, name):
        if name == "next":
            return F4(fType, self)

        if name == "color":
            return F5(fType, self)

        if name == "mark":
            return F6(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, Znext=None, color=None, mark=None, edges=None, Zmap=None):
        """
        :return a new Node instance with the argument field values
        """
        rval = self._cls(-1, Znext, color, mark, edges, Zmap)
        self.add(rval)
        return rval

class P3(StoragePool):
    """
     check that projection wont interfere with regular subtyping
    """

    def __init__(self, poolIndex, superPool, cls):
        """
        Can only be constructed by the SkillFile in this package.
        """
        super(P3, self).__init__(poolIndex, "subnode", superPool, ["f", "n"], [None for i in range(0, 0)], cls)

    def addKnownField(self, name, string, annotation):
        if name == "f":
            F7(annotation, self)

        elif name == "n":
            F8(self.owner().Node, self)
                
    def addField(self, fType, name):
        if name == "f":
            return F7(fType, self)

        if name == "n":
            return F8(fType, self)

        else:
            return LazyField(fType, name, self)

    def make(self, f=None, n=None, Znext=None, color=None, mark=None, edges=None, Zmap=None):
        """
        :return a new SubNode instance with the argument field values
        """
        rval = self._cls(-1, f, n, Znext, color, mark, edges, Zmap)
        self.add(rval)
        return rval


class F0(KnownDataField):
    """
    abstractnode ColorHolder.anAbstractNode
    """
    def __init__(self, fType, owner):
        super(F0, self).__init__(fType, "anabstractnode", owner)
        
        if ():
            raise SkillException("Expected field type abstractnode in ColorHolder.anAbstractNode but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        for i in range(i, h):
            d[i].anAbstractNode = fType.readSingleField(inStream)


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            raise AttributeError()
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        for i in range(i, h):
            self.fieldType().writeSingleField(d[i].anAbstractNode, out)


    def get(self, ref):
        return ref.anAbstractNode

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.anAbstractNode = value


class F1(KnownDataField):
    """
    annotation ColorHolder.anAnnotation
    """
    def __init__(self, fType, owner):
        super(F1, self).__init__(fType, "anannotation", owner)
        
        if fType.typeID() != 5:
            raise SkillException("Expected field type annotation in ColorHolder.anAnnotation but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        if isinstance(self.fieldType(), Annotation):
            t = (Annotation) (FieldType<?>) self.fieldType()
        for i in range(i, h):
            d[i].anAnnotation = t.readSingleField(inStream)


    def _osc(self, i, h):
        
        if isinstance(self.fieldType(), Annotation):
            t = (Annotation) (FieldType<?>) self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            raise AttributeError()
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        if isinstance(self.fieldType(), Annotation):
            t = (Annotation) (FieldType<?>) self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].anAnnotation, out)


    def get(self, ref):
        return ref.anAnnotation

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.anAnnotation = value


class F2(KnownDataField):
    """
    set<abstractnode> AbstractNode.edges
    """
    def __init__(self, fType, owner):
        super(F2, self).__init__(fType, "edges", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type set<abstractnode> in AbstractNode.edges but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            size = inStream.v64()
            v = set()
            t = self.fieldType().groundType
            for k in range(0, size):
                v.add(fType.readSingleField(inStream))
            d[i].edges = v


    def _osc(self, i, h):
        
        fType = self.fieldType()
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].edges
            if v is None:
                size = 0
            else:
                size = len(v)
            if 0 == size:
                result += 1
            else:
                result += V64.singleV64Offset(size)
                result += self.fieldType().groundType.calculateOffset(v)
            
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.data()
        fType = self.fieldType()
        
        for i in range(i, h):
            
            x = d[i].edges
            size = 0 if x is None else len(x)
            if size == 0:
                out.i8(0)
            else:
                out.v64(size)
                for e in x:
                    self.fieldType().writeSingleField(e, out)

        


    def get(self, ref):
        return ref.edges

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.edges = value


class F3(KnownDataField):
    """
    map<node,abstractnode,annotation> AbstractNode.map
    """
    def __init__(self, fType, owner):
        super(F3, self).__init__(fType, "map", owner)
        
        if False:  # TODO type check!:
            raise SkillException("Expected field type map<node,abstractnode,annotation> in AbstractNode.map but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.data()
        fType = self.fieldType()
        for i in range(i, h):
            d[i].Zmap = fType.readSingleField(inStream)


    def _osc(self, i, h):
        
        fType = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].Zmap
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
            self.fieldType().writeSingleField(d[i].Zmap, out)


    def get(self, ref):
        return ref.Zmap

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Zmap = value


class F4(KnownDataField):
    """
    annotation Node.next
    """
    def __init__(self, fType, owner):
        super(F4, self).__init__(fType, "next", owner)
        
        if fType.typeID() != 5:
            raise SkillException("Expected field type annotation in Node.next but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        if isinstance(self.fieldType(), Annotation):
            t = (Annotation) (FieldType<?>) self.fieldType()
        for i in range(i, h):
            d[i].Znext = t.readSingleField(inStream)


    def _osc(self, i, h):
        
        if isinstance(self.fieldType(), Annotation):
            t = (Annotation) (FieldType<?>) self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            raise AttributeError()
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        if isinstance(self.fieldType(), Annotation):
            t = (Annotation) (FieldType<?>) self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].Znext, out)


    def get(self, ref):
        return ref.Znext

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.Znext = value


class F5(KnownDataField):
    """
    string Node.color
    """
    def __init__(self, fType, owner):
        super(F5, self).__init__(fType, "color", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in Node.color but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].color = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].color
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].color, out)


    def get(self, ref):
        return ref.color

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.color = value


class F6(KnownDataField):
    """
    string Node.mark
    """
    def __init__(self, fType, owner):
        super(F6, self).__init__(fType, "mark", owner)
        
        if self.fieldType().typeID() != 14:
            raise SkillException("Expected field type string in Node.mark but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        t = self.owner.owner().Strings()
        for i in range(i, h):
            d[i].mark = t.get(inStream.v64())


    def _osc(self, i, h):
        
        t = self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            v = d[i].mark
            if v is None:
                result += 1
            else:
                result += self.fieldType().singleOffset(v)
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        t = self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].mark, out)


    def get(self, ref):
        return ref.mark

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.mark = value


class F7(KnownDataField):
    """
    annotation SubNode.f
    """
    def __init__(self, fType, owner):
        super(F7, self).__init__(fType, "f", owner)
        
        if fType.typeID() != 5:
            raise SkillException("Expected field type annotation in SubNode.f but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        if isinstance(self.fieldType(), Annotation):
            t = (Annotation) (FieldType<?>) self.fieldType()
        for i in range(i, h):
            d[i].f = t.readSingleField(inStream)


    def _osc(self, i, h):
        
        if isinstance(self.fieldType(), Annotation):
            t = (Annotation) (FieldType<?>) self.fieldType()
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            raise AttributeError()
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        if isinstance(self.fieldType(), Annotation):
            t = (Annotation) (FieldType<?>) self.fieldType()
        for i in range(i, h):
            t.writeSingleField(d[i].f, out)


    def get(self, ref):
        return ref.f

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.f = value


class F8(KnownDataField):
    """
    node SubNode.n
    """
    def __init__(self, fType, owner):
        super(F8, self).__init__(fType, "n", owner)
        
        if fType.name() != "node":
            raise SkillException("Expected field type node in SubNode.n but found {}".format(fType))

    
    def _rsc(self, i, h, inStream):
        d = self.owner.basePool.data()
        t = self.fieldType()
        for i in range(i, h):
            d[i].n = t.getByID(inStream.v64())


    def _osc(self, i, h):
        
        d = self.owner.basePool.data()
        result = 0
        for i in range(i, h):
            instance = d[i].n
            if instance is None:
                result += 1
                continue
            result += V64.singleV64Offset(instance.getSkillID())
        self._offset += result

    def _wsc(self, i, h, out):
        d = self.owner.basePool.data()
        for i in range(i, h):
            
            v = d[i].n
            if v is None:
                out.i8(0)
            else:
                out.v64(v.getSkillID())


    def get(self, ref):
        return ref.n

    def set(self, ref, value):
        assert isinstance(ref, self.owner._cls)
        ref.n = value

