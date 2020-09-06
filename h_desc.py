from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple, Union, List

from lark import Lark, Token, v_args, Discard
from lark.visitors import Transformer

parser = Lark(open('h_desc.lark').read(), parser='lalr', maybe_placeholders=True)


class CType(ABC):
    @abstractmethod
    def for_ctypes(self):
        pass


FUNCTYPE = 'PYFUNCTYPE'
DLL_SOURCE = ''
DLL_VAR_NAME = 'pythonapi'

BUILTINS_TYPES = {
    'void': 'None',
    'size_t': 'c_size_t',
    'ssize_t': 'c_ssize_t',
    'char': 'c_char',
    'int': 'c_int',
    'long': 'c_long',
}

UNSIGNED_BUILTINS_TYPES = {
    'int': 'c_uint',
    'long': 'c_ulong',
}


@dataclass(frozen=True)
class TypeReference(CType):
    name: str
    __slots__ = 'name',

    def for_ctypes(self):
        return self.name if self.name not in BUILTINS_TYPES else BUILTINS_TYPES[self.name]


@dataclass(frozen=True)
class UnsignedTypeReference(CType):
    name: str
    __slots__ = 'name',

    def for_ctypes(self):
        return UNSIGNED_BUILTINS_TYPES[self.name]


@dataclass(frozen=True)
class StructReference(CType):
    name: str
    __slots__ = 'name',

    def for_ctypes(self):
        return f"Struct_{self.name}"


@dataclass(frozen=True)
class Pointer(CType):
    base: CType
    __slots__ = 'base',

    def for_ctypes(self):
        base = self.base.for_ctypes()
        if base is None or base == 'None':
            return "c_void_p"
        elif base == 'PyObject':
            return "py_object"
        else:
            return f"POINTER({base})"


@dataclass(frozen=True)
class Struct(CType):
    name: Optional[str]
    fields: Tuple[Tuple[str, CType], ...]
    __slots__ = 'name', 'fields'

    def for_ctypes(self):
        return f"Struct_{self.name}" if self.name is not None else None

    def get_ctypes_declaration(self, synonym: str = None):
        if self.name is None:
            name, synonym = synonym, None
        else:
            name = f"Struct_{self.name}"
        if synonym is not None:
            synonym_line = f"\n{synonym} = {name}\n"
        else:
            synonym_line = ""
        assert name is not None, "Need a name to create declaration"
        return f"""class {name}(Structure):\n    pass\n{synonym_line}""", name

    def get_ctypes_definition(self, actual_name: str):
        fields = [f"({n!r}, {t.for_ctypes()})" for n, t in self.fields]
        res = ',\n    '.join(fields)
        return f"{actual_name}._fields_ = [\n    {res}]\n"


@dataclass(frozen=True)
class FunctionType(CType):
    return_type: CType
    parameter: Tuple[Tuple[Optional[str], CType]]
    __slots__ = 'return_type', 'parameter'

    def for_ctypes(self):
        return f"{FUNCTYPE}({self.return_type.for_ctypes()}, {', '.join(t[1].for_ctypes() for t in self.parameter)})"

@dataclass(frozen=True)
class FunctionDecl:
    name: str
    func_type: FunctionType

    def get_ctypes_definition(self):
        return f"{self.name} = {self.func_type.for_ctypes()}(({self.name!r}, {DLL_VAR_NAME}))"

@v_args(inline=True)
class Translator(Transformer):
    def __init__(self):
        super(Translator, self).__init__(False)
        self.typedefs = {}
        self.structs = set()
        self.functions = []

    def __default__(self, *args):
        raise NotImplementedError(args)

    def type_reference(self, name: Token):
        return TypeReference(name.value)

    def unsigned_type(self, name: Token):
        return UnsignedTypeReference(name.value)

    def named_type(self, t: CType, name: Token):
        return name.value, t

    def function_type(self, return_type: CType, name: Token, *parameters: Tuple[Optional[str], CType]):
        return name.value, FunctionType(return_type, parameters)

    def struct_reference(self, name: Token):
        return StructReference(name.value)

    def ptr_type(self, base: CType):
        return Pointer(base)

    def full_struct(self, name: Optional[Token], *fields: Tuple[str, CType]):
        s = Struct(name if name is None else name.value, fields)
        self.structs.add(s)
        return s

    def typedef(self, named_type: Tuple[str, CType]):
        n, t = named_type
        self.typedefs[n] = t
        raise Discard
    
    def parameters(self, *params: Tuple[str, CType]):
        return params

    def type_decl(self, decl_type: CType):
        raise Discard

    def parameter(self, base: Union[Tuple[str, CType], CType]):
        if not isinstance(base, tuple):
            return None, base
        else:
            return base[0], base[1]

    def func_decl(self, ret_name: Tuple[str, CType], *params: Tuple[Optional[str], CType]):
        self.functions.append(FunctionDecl(ret_name[0], FunctionType(ret_name[1], params)))
        raise Discard

    def start(self):
        parts = []
        decls = []
        structs = {}
        for n, t in self.typedefs.items():
            if not isinstance(t, Struct):
                parts.append(f"{n} = {t.for_ctypes()}")
            else:
                p, an = t.get_ctypes_declaration(n)
                decls.append(p)
                structs[t] = an
        for s in self.structs:
            if s not in structs:
                p, an = s.get_ctypes_declaration()
                decls.append(p)
                structs[s] = an
        for f in self.functions:
            parts.append(f.get_ctypes_definition())
        for s, an in structs.items():
            parts.append(s.get_ctypes_definition(an))
        return '\n'.join(['from ctypes import *'] + decls + parts)


tree = parser.parse(open('object.h.desc').read())
trans = Translator()
print(trans.transform(tree), file=open("object_h.py", "w"))
