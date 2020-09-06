from __future__ import annotations

from inspect import stack

import builtins
import functools
from object_h import POINTER, PyTypeObject, cast


def set_custom_getattr(t, f):
    """
    `f` will act as `__getattr__` for type `t` (as an additional layer on top of the internal machinery)
    """
    try:
        t.__getattr__
        raise ValueError("Type t already has a __getattr__")
    except AttributeError:
        pass
    Py_TPFLAGS_HEAPTYPE = 1 << 9
    t_type = cast(id(t), POINTER(PyTypeObject))
    if t_type.contents.tp_flags & Py_TPFLAGS_HEAPTYPE:
        t.__getattr__ = f
    else:
        t_type.contents.tp_flags ^= Py_TPFLAGS_HEAPTYPE  # DO AS LITTLE AS POSSIBLE. Will complelty break the interpreter if used on the wrong types/wrong moments
        t.__getattr__ = f
        t_type.contents.tp_flags ^= Py_TPFLAGS_HEAPTYPE


class Test:
    pass

_map = builtins.map
_filter = builtins.filter

def map(a, b):
    if callable(a):
        return _map(a, b)
    else:
        return _map(b, a)


def filter(a, b):
    if callable(a):
        return _filter(a, b)
    else:
        return _filter(b, a)


builtins.map = map
builtins.filter = filter
builtins.reduce = functools.reduce

__in_recursion__ = []


def resolve_outer_method(obj, name):
    if name[:2] == name[-2:] == '__':
        raise AttributeError(name)
    if __in_recursion__:
        raise AttributeError(name)
    try:
        __in_recursion__.append(0)
        s = stack()
        if len(s) < 2:
            raise AttributeError(name)
        to_search = s[1]
        if name in to_search.frame.f_locals:
            f = to_search.frame.f_locals[name]
        elif name in to_search.frame.f_globals:
            f = to_search.frame.f_globals[name]
        elif name in builtins.__dict__:
            f = builtins.__dict__[name]
        else:
            raise AttributeError(name)
        if not callable(f):
            raise AttributeError(name)
        return lambda *args: f(obj, *args)
    finally:
        __in_recursion__.pop()


set_custom_getattr(object, resolve_outer_method)
