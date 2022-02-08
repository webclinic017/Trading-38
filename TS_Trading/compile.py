from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
ext_modules = [
    Extension("trader",  ['C:/Users/m_bot/AppData/Local/Programs/Python/Python38/Trading/trader.py']) #name and extension of py file to compile
#   ... add more on new line if you like ...
]
setup(
    name = 'trader', #name for idk? it's built with the name above
    cmdclass = {'build_ext': build_ext},#leave the rest
    ext_modules = ext_modules
)