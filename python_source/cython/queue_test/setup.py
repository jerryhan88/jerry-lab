# command line argument
CMD_ARGS = ['build_ext', '--inplace']

from sys import argv
argv.extend(CMD_ARGS)
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
    ext_modules = cythonize([Extension("queue", ["queue.pyx"])])
)
      
print '\n%s Completed successfully!!!\n' % ('-' * 10)