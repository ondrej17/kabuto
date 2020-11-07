"""
    Name:           setup.py
    Description:    Installer of DESCRIPTORS module for Python written in C++.
    Author:         Ondrej Bily
"""

from distutils.core import setup, Extension

module1 = Extension(
    "descriptors",
    sources=['descriptors_timestep.cpp',
             'descriptors_module.cpp',
             'descriptors_utility.cpp',
             'descriptors_verlet_list.cpp',
             'descriptors_atom.cpp',
             'descriptors_box.cpp'],
)

setup(name="descriptors",
      version="1.0",
      description="C++ library for calculating descriptors during MD simulation.",
      author="Ondrej Bily",
      ext_modules=[module1])
