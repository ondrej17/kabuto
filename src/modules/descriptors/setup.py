from distutils.core import setup, Extension

module1 = Extension(
      "descriptors",
      sources=['descriptorsmodule.cpp'],
)

setup(name="descriptors",
      version="1.0",
      description="This is descriptors module",
      author="Ondrej Bily",
      ext_modules=[module1])


