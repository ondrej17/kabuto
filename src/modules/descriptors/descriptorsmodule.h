extern "C" {
    #include <Python.h>
}

static PyObject *descriptors_compute(PyObject* self, PyObject *args);
std::vector<float> listTupleToVector_Float(PyObject* incoming);