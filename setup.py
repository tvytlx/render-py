# distutils: define_macros=CYTHON_TRACE_NOGIL=1
import numpy

from distutils.core import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "speedup",
        ["render/speedup.pyx"],
        # define_macros=[("CYTHON_TRACE", "1")],
        include_dirs=[numpy.get_include()],
        libraries=["m"],
    )
]
setup(
    ext_modules=cythonize(
        extensions,
        annotate=True,
        compiler_directives={"linetrace": True, "binding": True},
    )
)
