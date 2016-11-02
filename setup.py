# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension('bg.dana.cdana', ['bg/dana/cdana.pyx'], include_dirs = [np.get_include()]),
]
setup(
    name="bg",
    version="0.2",
    maintainer= "Nicolas P. Rougier",
    maintainer_email="Nicolas.Rougier@inria.fr",
    install_requires=['numpy', 'cython', 'tqdm'],
    license = "BSD License",
    packages=['bg', 'bg.dana'],
    ext_modules = cythonize(extensions)
)
