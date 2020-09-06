from __future__ import annotations

from inspect import stack

from object_h import *

def set_custom_getattr(t, f):
    """
    `f` will act as `__getattr__` for type `t` (as an additional layer on top of the internal machinery)
    """
    Py_TPFLAGS_HEAPTYPE = 1 << 9
    t_type = cast(id(t), POINTER(PyTypeObject))
    if t_type.contents.tp_flags & Py_TPFLAGS_HEAPTYPE:
        t.__getattr__ = f
    else:
        t_type.contents.tp_flags ^= Py_TPFLAGS_HEAPTYPE # DO AS LITTLE AS POSSIBLE. Will complelty break the interpreter if used on the wrong types
        t.__getattr__ = f
        t_type.contents.tp_flags ^= Py_TPFLAGS_HEAPTYPE


class Test:
    pass

if __name__ == "__main__":
    def wrap(obj, f):
        if callable(f):
            return lambda *args: f(obj, *args)
        else:
            raise AttributeError
    def resolve_outer_method(obj, name,recurse=[]):
        if recurse:
            raise AttributeError
        else:
            recurse.append(0)
        to_search = stack()[1]
        if name in to_search.frame.f_locals:
            f = to_search.frame.f_locals[name]
        elif name in to_search.frame.f_globals:
            f = to_search.frame.f_globals[name]
        elif name in __builtins__.__dict__:
            f = __builtins__.__dict__[name]
        else:
            raise AttributeError
        recurse.pop()
        return wrap(obj, f)
    set_custom_getattr(object, resolve_outer_method)
    print((lambda a: a**2).map([1, 2, 3]).list())