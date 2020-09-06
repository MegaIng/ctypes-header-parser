from __future__ import annotations

from typing import Mapping, Any, List, Tuple, Dict
import operator

AUTO_ACTIVE = None


class _Template:
    def __init__(self):
        self.__active__ = AUTO_ACTIVE

    def __get_arguments__(self) -> List[Argument]:
        pass

    def __get_value__(self, passed: Mapping[str, Any]) -> Any:
        pass

    def __call__(self, *args, **kwargs):
        def do_call():
            params = self.__get_arguments__()
            params.sort(key=lambda a: (a.__arg_order__, a.__arg_name__))
            if args:
                assert not kwargs
                passed = {p.__arg_name__: v for p, v in zip(params, args)}
            elif kwargs:
                assert set(kwargs.keys()) == {p.__arg_name__ for p in params}
                passed = kwargs
            else:
                raise ValueError
            return self.__get_value__(passed)

        if self.__active__ is False:
            return _Call(self, args, kwargs)
        elif self.__active__ is True:
            return do_call()
        else:
            if args and kwargs:
                return _Call(self, args, kwargs)
            if not args:
                args_ = tuple(kwargs.values())
            else:
                args_ = args
            p = len(self.__get_arguments__())
            if p == len(args_):
                for a in args_:
                    if isinstance(a, _Template):
                        break
                else:
                    return do_call()
            return _Call(self, args, kwargs)

    def __getattr__(self, item):
        if item[:2] == item[-2:] == '__':
            raise AttributeError
        return _Attribute(self, item)

    def __lt__(self, other):
        return _BinOp(self, operator.__lt__, other)

    def __le__(self, other):
        return _BinOp(self, operator.__le__, other)

    def __eq__(self, other):
        return _BinOp(self, operator.__eq__, other)

    def __ne__(self, other):
        return _BinOp(self, operator.__ne__, other)

    def __ge__(self, other):
        return _BinOp(self, operator.__ge__, other)

    def __gt__(self, other):
        return _BinOp(self, operator.__gt__, other)

    def __add__(self, other):
        return _BinOp(self, operator.__add__, other)

    def __radd__(self, other):
        return _BinOp(other, operator.__add__, other)

    def __and__(self, other):
        return _BinOp(self, operator.__and__, other)

    def __rand__(self, other):
        return _BinOp(other, operator.__and__, other)

    def __floordiv__(self, other):
        return _BinOp(self, operator.__floordiv__, other)

    def __rfloordiv__(self, other):
        return _BinOp(other, operator.__floordiv__, other)

    def __lshift__(self, other):
        return _BinOp(self, operator.__lshift__, other)

    def __rlshift__(self, other):
        return _BinOp(other, operator.__lshift__, other)

    def __mod__(self, other):
        return _BinOp(self, operator.__mod__, other)

    def __rmod__(self, other):
        return _BinOp(other, operator.__mod__, other)

    def __mul__(self, other):
        return _BinOp(self, operator.__mul__, other)

    def __rmul__(self, other):
        return _BinOp(other, operator.__mul__, other)

    def __matmul__(self, other):
        return _BinOp(self, operator.__matmul__, other)

    def __rmatmul__(self, other):
        return _BinOp(other, operator.__matmul__, other)

    def __or__(self, other):
        return _BinOp(self, operator.__or__, other)

    def __ror__(self, other):
        return _BinOp(other, operator.__or__, other)

    def __pow__(self, other):
        return _BinOp(self, operator.__pow__, other)

    def __rpow__(self, other):
        return _BinOp(other, operator.__pow__, other)

    def __rshift__(self, other):
        return _BinOp(self, operator.__rshift__, other)

    def __rrshift__(self, other):
        return _BinOp(other, operator.__rshift__, other)

    def __sub__(self, other):
        return _BinOp(self, operator.__sub__, other)

    def __rsub__(self, other):
        return _BinOp(other, operator.__sub__, other)

    def __truediv__(self, other):
        return _BinOp(self, operator.__truediv__, other)

    def __rtruediv__(self, other):
        return _BinOp(other, operator.__truediv__, other)

    def __xor__(self, other):
        return _BinOp(self, operator.__xor__, other)

    def __rxor__(self, other):
        return _BinOp(other, operator.__xor__, other)

    def __contains__(self, other):
        return _BinOp(self, operator.__contains__, other)

    def __delitem__(self, other):
        return _BinOp(self, operator.__delitem__, other)

    def __getitem__(self, other):
        return _BinOp(self, operator.__getitem__, other)

    def __iadd__(self, other):
        return _BinOp(self, operator.__iadd__, other)

    def __iand__(self, other):
        return _BinOp(self, operator.__iand__, other)

    def __ifloordiv__(self, other):
        return _BinOp(self, operator.__ifloordiv__, other)

    def __ilshift__(self, other):
        return _BinOp(self, operator.__ilshift__, other)

    def __imod__(self, other):
        return _BinOp(self, operator.__imod__, other)

    def __imul__(self, other):
        return _BinOp(self, operator.__imul__, other)

    def __imatmul__(self, other):
        return _BinOp(self, operator.__imatmul__, other)

    def __ior__(self, other):
        return _BinOp(self, operator.__ior__, other)

    def __ipow__(self, other):
        return _BinOp(self, operator.__ipow__, other)

    def __irshift__(self, other):
        return _BinOp(self, operator.__irshift__, other)

    def __isub__(self, other):
        return _BinOp(self, operator.__isub__, other)

    def __itruediv__(self, other):
        return _BinOp(self, operator.__itruediv__, other)

    def __ixor__(self, other):
        return _BinOp(self, operator.__ixor__, other)


def __get_value__(a: Any, passed: Mapping[str, Any]):
    # Maybe extend to list/tuple/dict recognition
    if isinstance(a, _Template):
        return a.__get_value__(passed)
    else:
        return a

def __get_arguments__(a: Any):
    # Maybe extend to list/tuple/dict recognition
    if isinstance(a, _Template):
        return a.__get_arguments__()
    else:
        return []


def _filter_arguments(args: List[Argument]) -> List[Argument]:
    seen = {}
    for a in args:
        if a.__arg_name__ in seen:
            assert seen[a.__arg_name__].__arg_order__ == a.__arg_order__
        else:
            seen[a.__arg_name__] = a
    return list(seen.values())


class Argument(_Template):
    def __init__(self, name: str, order: int = 0):
        super(Argument, self).__init__()
        self.__arg_name__ = name
        self.__arg_order__ = order

    def __get_arguments__(self) -> List[Argument]:
        return [self]

    def __get_value__(self, passed: Mapping[str, Any]) -> Any:
        return passed[self.__arg_name__]


class _Attribute(_Template):
    def __init__(self, base: _Template, name: str):
        super(_Attribute, self).__init__()
        self.__base_template__ = base
        self.__target_name__ = name

    def __get_arguments__(self) -> List[Argument]:
        return __get_arguments__(self.__base_template__)

    def __get_value__(self, passed: Mapping[str, Any]) -> Any:
        return getattr(self.__base_template__.__get_value__(passed), self.__target_name__)


class _Call(_Template):
    def __init__(self, base: _Template, args: Tuple, kwargs: Dict):
        super(_Call, self).__init__()
        self.__base_template__ = base
        self.__args_template__ = args
        self.__kwargs_template__ = kwargs

    def __get_arguments__(self) -> List[Argument]:
        out = __get_arguments__(self.__base_template__)
        for a in self.__args_template__:
            out.extend(__get_arguments__(a))
        for a in self.__kwargs_template__.values():
            out.extend(__get_arguments__(a))
        return _filter_arguments(out)

    def __get_value__(self, passed: Mapping[str, Any]) -> Any:
        args = []
        for a in self.__args_template__:
            args.append(__get_value__(a, passed))
        kwargs = {}
        for n, a in self.__kwargs_template__.items():
            kwargs[n] = __get_value__(a, passed)
        return self.__base_template__.__get_value__(passed)(*args, **kwargs)


class _BinOp(_Template):
    def __init__(self, left: _Template, op, right: _Template):
        super(_BinOp, self).__init__()
        self.__left_template__ = left
        self.__op__ = op
        self.__right_template__ = right

    def __get_arguments__(self) -> List[Argument]:
        return _filter_arguments(__get_arguments__(self.__left_template__) + __get_arguments__(self.__right_template__))

    def __get_value__(self, passed: Mapping[str, Any]) -> Any:
        return self.__op__(__get_value__(self.__left_template__, passed), __get_value__(self.__right_template__, passed))


def lam(t: _Template):
    t.__active__ = True


l = λ = lam

a = Argument('a')
b = Argument('b')
c = Argument('c')
x = Argument('x')
y = Argument('y')
z = Argument('z')