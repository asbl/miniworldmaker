import pkgutil
from miniworldmaker import config
from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module
    for attribute_name in dir(_module):
        attribute = getattr(_module, attribute_name)
        if isclass(attribute):  
            globals()[attribute_name] = attribute
            __all__.append(attribute.__name__)

# needed for decorators:
from miniworldmaker.tools.timer import timer
from miniworldmaker.tools.timer import loop

__all__.append(timer.__name__)
__all__.append(loop.__name__)