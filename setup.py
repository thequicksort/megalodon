import imp
import os
import re
import subprocess
import sys
import time

from glob import glob
from setuptools import setup, find_packages
from setuptools.extension import Extension


__pkg_name__ = 'megalodon'

# Get the version number from _version.py, and exe_path
verstrline = open(os.path.join('megalodon', '_version.py'), 'r').readlines()[-1]
vsre = r"^MEGALODON_VERSION = ['\"]([^'\"]*)['\"]"
mo = re.search(vsre, verstrline)
if mo:
    __version__ = mo.group(1)
else:
    raise RuntimeError('Unable to find version string in "megalodon/_version.py".')


install_requires = [
    "h5py >= 2.2.1",
    "numpy >= 1.9.0",
    "Cython >= 0.25.2",
    "mappy >= 2.15",
    "pysam >= 0.15",
    "ont_fast5_api >= 1.1",
    "tqdm",
]


#  Build extensions
try:
    import numpy as np
    from Cython.Build import cythonize
    extensions = cythonize([
        Extension(__pkg_name__ + ".decode", [
            os.path.join(__pkg_name__, "_decode.pyx"),
            os.path.join(__pkg_name__, "_c_decode.c")],
                  include_dirs=[np.get_include()],
                  extra_compile_args=["-O3", "-fopenmp", "-std=c99",
                                      "-march=native"],
                  extra_link_args=["-fopenmp"]),
    ])
except ImportError:
    extensions = []
    sys.stderr.write("WARNING: Numpy and Cython are required to build " +
                     "megalodon extensions\n")
    if any([cmd in sys.argv for cmd in [
            "install", "build", "build_clib", "build_ext", "bdist_wheel"]]):
        raise


setup(
    name=__pkg_name__,
    version=__version__,
    description='Nanopore base calling augmentation',
    maintainer='Marcus Stoiber',
    maintainer_email='marcus.stoiber@nanoporetech.com',
    url='http://www.nanoporetech.com',
    long_description=(
        'Megalodon contains base calling augmentation capabilities, mainly ' +
        'including direct, reference-guided SNP and modified base detection.'),

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],

    packages=find_packages(exclude=[
        "*.test", "*.test.*", "test.*", "test", "bin"]),
    package_data={'configs': 'data/configs/*'},
    exclude_package_data={'': ['*.hdf', '*.c', '*.h']},
    ext_modules=extensions,
    install_requires=install_requires,
    dependency_links=[],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            '{0} = {0}.{0}:_main'.format(__pkg_name__)
        ]
    },

)
