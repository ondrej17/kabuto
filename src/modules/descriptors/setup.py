from distutils.core import setup, Extension

module1 = Extension(
    "descriptors",
    # TODO: modify list of cpp files
    sources=['descriptors_module.cpp',
             #'descriptors_func_module.cpp',
             'descriptors_utility.cpp',
             'VerletList.cpp',
             'Box.cpp',
             'Atom.cpp',
             'Timestep.cpp'],
)

setup(name="descriptors",
      version="1.0",
      description="This is descriptors module",
      author="Ondrej Bily",
      ext_modules=[module1])
