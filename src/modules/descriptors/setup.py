"""
    Name:           setup.py
    Description:    Installer of DESCRIPTORS module for Python written in C++.
    Author:         Ondrej Bily
"""

from distutils.core import setup, Extension

module1 = Extension(
    "descriptors",
    sources=['src/descriptors_timestep.cpp',
             'src/descriptors_module.cpp',
             'src/descriptors_utility.cpp',
             'src/descriptors_verlet_list.cpp',
             'src/descriptors_atom.cpp',
             'src/descriptors_box.cpp'],
    extra_compile_args=['-std=c++17'],
)

setup(name="descriptors",
      version="1.0",
      description="C++ library for calculating descriptors during MD simulation.",
      author="Ondrej Bily",
      ext_modules=[module1])
