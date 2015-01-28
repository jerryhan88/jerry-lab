# command line argument
CMD_ARGS = ['build_ext', '--inplace']

from sys import argv
argv.extend(CMD_ARGS)
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("interitance",
              ["interitance.pyx"]) # Unix-like specific
]

setup(
  name = "interitance",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
      
print '\n%s Completed successfully!!!\n' % ('-' * 10)