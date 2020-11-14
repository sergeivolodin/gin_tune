import ray.tune as tune
import gin
import types
from functools import partial
import logging


# function argument the value of which the function returns
OVERRIDE_ATTR = '_override'

# map name -> function
FUNCS = {}

OVERRIDE_ERROR = \
"""No parameter provided for function {func_name} in scope {scope}. Please check that
 1. You are running tune_gin() instead of simply tune.run(),
 2. Your gin config file is loaded, and
 3. Your gin config file is written properly
 
Provided kwargs: {kwargs}"""

def register_func(f, func_name=None):
    """Register tune function."""
    if func_name is None:
        func_name = f.__name__
    override = make_override(func_name)
    f_gin = gin.configurable(func_name, module=f.__module__)(override)
        
    FUNCS[func_name] = {'orig': f, 'gin': f_gin}
    return f

def register_module(module):
    """Register all functions in a module."""
    for func_name in dir(module):
        obj = getattr(module, func_name)
        if not isinstance(obj, types.FunctionType): continue
        if not obj.__module__.startswith("ray"): continue
        register_func(obj, func_name=func_name)

def make_override(func_name):
    """Return a function which returns OVERRIDE_ATTR or returns an error."""
    
    def override(pass_through=False, scope="", **kwargs):
        if OVERRIDE_ATTR in kwargs:
            logging.info(f"gin_tune: selected value for @{scope}/{func_name}: {kwargs[OVERRIDE_ATTR]}")
            return kwargs[OVERRIDE_ATTR]
        elif pass_through:
            logging.info(f"gin_tune: passing arguments for @{scope}/{func_name}: {kwargs}")
            return FUNCS[func_name]['orig'](**kwargs)
        else:
            raise ValueError(OVERRIDE_ERROR.format(scope=gin.current_scope(),
                                                   func_name=func_name,
                                                   kwargs=kwargs))
    return override

def register_functions():
    """Register functions from tune."""
    # wrap all functions from tune.sample
    register_module(tune.sample)
    register_func(tune.grid_search)