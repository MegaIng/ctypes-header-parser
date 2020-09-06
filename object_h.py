from ctypes import *
class PyObject(Structure):
    pass

class PyVarObject(Structure):
    pass

class Struct_bufferinfo(Structure):
    pass

Py_buffer = Struct_bufferinfo

class PyType_Slot(Structure):
    pass

class PyType_Spec(Structure):
    pass

class Struct_PyMethodDef(Structure):
    pass

PyMethodDef = Struct_PyMethodDef

class Struct_PyGetSetDef(Structure):
    pass

PyGetSetDef = Struct_PyGetSetDef

class Struct_PyMemberDef(Structure):
    pass

PyMemberDef = Struct_PyMemberDef

class Struct__typeobject(Structure):
    pass

PyTypeObject = Struct__typeobject

class PyNumberMethods(Structure):
    pass

class PySequenceMethods(Structure):
    pass

class PyMappingMethods(Structure):
    pass

class PyAsyncMethods(Structure):
    pass

class PyBufferProcs(Structure):
    pass

class mappingproxyobject(Structure):
    pass

class PyDescrObject(Structure):
    pass

class PyWrapperDescrObject(Structure):
    pass

class Struct_wrapperbase(Structure):
    pass

Py_ssize_t = c_ssize_t
Py_hash_t = Py_ssize_t
unaryfunc = PYFUNCTYPE(py_object, py_object)
binaryfunc = PYFUNCTYPE(py_object, py_object, py_object)
ternaryfunc = PYFUNCTYPE(py_object, py_object, py_object, py_object)
inquiry = PYFUNCTYPE(c_int, py_object)
lenfunc = PYFUNCTYPE(Py_ssize_t, py_object)
ssizeargfunc = PYFUNCTYPE(py_object, py_object, Py_ssize_t)
ssizessizeargfunc = PYFUNCTYPE(py_object, py_object, Py_ssize_t, Py_ssize_t)
ssizeobjargproc = PYFUNCTYPE(c_int, py_object, Py_ssize_t, py_object)
ssizessizeobjargproc = PYFUNCTYPE(c_int, py_object, Py_ssize_t, Py_ssize_t, py_object)
objobjargproc = PYFUNCTYPE(c_int, py_object, py_object, py_object)
objobjproc = PYFUNCTYPE(c_int, py_object, py_object)
visitproc = PYFUNCTYPE(c_int, py_object, c_void_p)
traverseproc = PYFUNCTYPE(c_int, py_object, visitproc, c_void_p)
freefunc = PYFUNCTYPE(None, c_void_p)
destructor = PYFUNCTYPE(None, py_object)
getattrfunc = PYFUNCTYPE(py_object, py_object, POINTER(c_char))
getattrofunc = PYFUNCTYPE(py_object, py_object, py_object)
setattrfunc = PYFUNCTYPE(c_int, py_object, POINTER(c_char), py_object)
setattrofunc = PYFUNCTYPE(c_int, py_object, py_object, py_object)
reprfunc = PYFUNCTYPE(py_object, py_object)
hashfunc = PYFUNCTYPE(Py_hash_t, py_object)
richcmpfunc = PYFUNCTYPE(py_object, py_object, py_object, c_int)
getiterfunc = PYFUNCTYPE(py_object, py_object)
iternextfunc = PYFUNCTYPE(py_object, py_object)
descrgetfunc = PYFUNCTYPE(py_object, py_object, py_object, py_object)
descrsetfunc = PYFUNCTYPE(c_int, py_object, py_object, py_object)
initproc = PYFUNCTYPE(c_int, py_object, py_object, py_object)
newfunc = PYFUNCTYPE(py_object, POINTER(Struct__typeobject), py_object, py_object)
allocfunc = PYFUNCTYPE(py_object, POINTER(Struct__typeobject), Py_ssize_t)
getbufferproc = PYFUNCTYPE(c_int, py_object, POINTER(Py_buffer), c_int)
releasebufferproc = PYFUNCTYPE(None, py_object, POINTER(Py_buffer))
vectorcallfunc = PYFUNCTYPE(py_object, py_object, POINTER(py_object), c_size_t, py_object)
PyCFunction = PYFUNCTYPE(py_object, py_object, py_object)
getter = PYFUNCTYPE(py_object, py_object, c_void_p)
setter = PYFUNCTYPE(c_int, py_object, py_object, c_void_p)
wrapperfunc = PYFUNCTYPE(py_object, py_object, py_object, c_void_p)
PyType_ClearCache = PYFUNCTYPE(c_uint, )(('PyType_ClearCache', pythonapi))
PyObject._fields_ = [
    ('ob_refcnt', Py_ssize_t),
    ('ob_type', POINTER(Struct__typeobject))]

PyVarObject._fields_ = [
    ('ob_base', PyObject),
    ('ob_size', Py_ssize_t)]

Struct_bufferinfo._fields_ = [
    ('buf', c_void_p),
    ('obj', py_object),
    ('len', Py_ssize_t),
    ('itemsize', Py_ssize_t),
    ('readonly', c_int),
    ('ndim', c_int),
    ('format', POINTER(c_char)),
    ('shape', POINTER(Py_ssize_t)),
    ('strides', POINTER(Py_ssize_t)),
    ('suboffsets', POINTER(Py_ssize_t)),
    ('internal', c_void_p)]

PyType_Slot._fields_ = [
    ('slot', c_int),
    ('pfunc', c_void_p)]

PyType_Spec._fields_ = [
    ('name', POINTER(c_char)),
    ('basicsize', c_int),
    ('itemsize', c_int),
    ('flags', c_uint),
    ('slots', POINTER(PyType_Slot))]

Struct_PyMethodDef._fields_ = [
    ('ml_name', POINTER(c_char)),
    ('ml_meth', PyCFunction),
    ('ml_flags', c_int),
    ('ml_doc', POINTER(c_char))]

Struct_PyGetSetDef._fields_ = [
    ('name', POINTER(c_char)),
    ('get', getter),
    ('set', setter),
    ('doc', POINTER(c_char)),
    ('closure', c_void_p)]

Struct_PyMemberDef._fields_ = [
    ('name', POINTER(c_char)),
    ('type', c_int),
    ('offset', Py_ssize_t),
    ('flags', c_int),
    ('doc', POINTER(c_char))]

Struct__typeobject._fields_ = [
    ('ob_base', PyVarObject),
    ('tp_name', POINTER(c_char)),
    ('tp_basicsize', Py_ssize_t),
    ('tp_itemsize', Py_ssize_t),
    ('tp_dealloc', destructor),
    ('tp_vectorcall_offset', Py_ssize_t),
    ('tp_getattr', getattrfunc),
    ('tp_setattr', setattrfunc),
    ('tp_as_async', POINTER(PyAsyncMethods)),
    ('tp_repr', reprfunc),
    ('tp_as_number', POINTER(PyNumberMethods)),
    ('tp_as_sequence', POINTER(PySequenceMethods)),
    ('tp_as_mapping', POINTER(PyMappingMethods)),
    ('tp_hash', hashfunc),
    ('tp_call', ternaryfunc),
    ('tp_str', reprfunc),
    ('tp_getattro', getattrofunc),
    ('tp_setattro', setattrofunc),
    ('tp_as_buffer', POINTER(PyBufferProcs)),
    ('tp_flags', c_ulong),
    ('tp_doc', POINTER(c_char)),
    ('tp_traverse', traverseproc),
    ('tp_clear', inquiry),
    ('tp_richcompare', richcmpfunc),
    ('tp_weaklistoffset', Py_ssize_t),
    ('tp_iter', getiterfunc),
    ('tp_iternext', iternextfunc),
    ('tp_methods', POINTER(Struct_PyMethodDef)),
    ('tp_members', POINTER(Struct_PyMemberDef)),
    ('tp_getset', POINTER(Struct_PyGetSetDef)),
    ('tp_base', POINTER(Struct__typeobject)),
    ('tp_dict', py_object),
    ('tp_descr_get', descrgetfunc),
    ('tp_descr_set', descrsetfunc),
    ('tp_dictoffset', Py_ssize_t),
    ('tp_init', initproc),
    ('tp_alloc', allocfunc),
    ('tp_new', newfunc),
    ('tp_free', freefunc),
    ('tp_is_gc', inquiry),
    ('tp_bases', py_object),
    ('tp_mro', py_object),
    ('tp_cache', py_object),
    ('tp_subclasses', py_object),
    ('tp_weaklist', py_object),
    ('tp_del', destructor),
    ('tp_version_tag', c_uint),
    ('tp_finalize', destructor),
    ('tp_vectorcall', vectorcallfunc)]

PyNumberMethods._fields_ = [
    ('nb_add', binaryfunc),
    ('nb_subtract', binaryfunc),
    ('nb_multiply', binaryfunc),
    ('nb_remainder', binaryfunc),
    ('nb_divmod', binaryfunc),
    ('nb_power', ternaryfunc),
    ('nb_negative', unaryfunc),
    ('nb_positive', unaryfunc),
    ('nb_absolute', unaryfunc),
    ('nb_bool', inquiry),
    ('nb_invert', unaryfunc),
    ('nb_lshift', binaryfunc),
    ('nb_rshift', binaryfunc),
    ('nb_and', binaryfunc),
    ('nb_xor', binaryfunc),
    ('nb_or', binaryfunc),
    ('nb_int', unaryfunc),
    ('nb_reserved', c_void_p),
    ('nb_float', unaryfunc),
    ('nb_inplace_add', binaryfunc),
    ('nb_inplace_subtract', binaryfunc),
    ('nb_inplace_multiply', binaryfunc),
    ('nb_inplace_remainder', binaryfunc),
    ('nb_inplace_power', ternaryfunc),
    ('nb_inplace_lshift', binaryfunc),
    ('nb_inplace_rshift', binaryfunc),
    ('nb_inplace_and', binaryfunc),
    ('nb_inplace_xor', binaryfunc),
    ('nb_inplace_or', binaryfunc),
    ('nb_floor_divide', binaryfunc),
    ('nb_true_divide', binaryfunc),
    ('nb_inplace_floor_divide', binaryfunc),
    ('nb_inplace_true_divide', binaryfunc),
    ('nb_index', unaryfunc),
    ('nb_matrix_multiply', binaryfunc),
    ('nb_inplace_matrix_multiply', binaryfunc)]

PySequenceMethods._fields_ = [
    ('sq_length', lenfunc),
    ('sq_concat', binaryfunc),
    ('sq_repeat', ssizeargfunc),
    ('sq_item', ssizeargfunc),
    ('was_sq_slice', c_void_p),
    ('sq_ass_item', ssizeobjargproc),
    ('was_sq_ass_slice', c_void_p),
    ('sq_contains', objobjproc),
    ('sq_inplace_concat', binaryfunc),
    ('sq_inplace_repeat', ssizeargfunc)]

PyMappingMethods._fields_ = [
    ('mp_length', lenfunc),
    ('mp_subscript', binaryfunc),
    ('mp_ass_subscript', objobjargproc)]

PyAsyncMethods._fields_ = [
    ('am_await', unaryfunc),
    ('am_aiter', unaryfunc),
    ('am_anext', unaryfunc)]

PyBufferProcs._fields_ = [
    ('bf_getbuffer', getbufferproc),
    ('bf_releasebuffer', releasebufferproc)]

mappingproxyobject._fields_ = [
    ('ob_base', PyObject),
    ('mapping', py_object)]

PyDescrObject._fields_ = [
    ('ob_base', PyObject),
    ('d_type', POINTER(PyTypeObject)),
    ('d_name', py_object),
    ('d_qualname', py_object)]

PyWrapperDescrObject._fields_ = [
    ('d_common', PyDescrObject),
    ('d_base', POINTER(Struct_wrapperbase)),
    ('d_wrapped', c_void_p)]

Struct_wrapperbase._fields_ = [
    ('name', POINTER(c_char)),
    ('offset', c_int),
    ('function', c_void_p),
    ('wrapper', wrapperfunc),
    ('doc', POINTER(c_char)),
    ('flags', c_int),
    ('name_strobj', py_object)]

