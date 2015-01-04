# command line argument
CMD_ARGS = ['build_ext', '--inplace']

# setup.
from sys import argv
argv.extend(CMD_ARGS)
from distutils.core import setup
from Cython.Build import cythonize
setup(
  name = 'dijkstra',
  ext_modules = cythonize(['dijkstra1.pyx', 'dijkstra2.pyx']),
)

print '\n%s Completed successfully!!!\n' % ('-' * 10)

import test
test.test()
