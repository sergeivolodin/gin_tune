from copy import deepcopy
import gin
from ray import tune
from functools import partial

from gin_tune.tune_funcs import OVERRIDE_ATTR, FUNCS
from gin_tune.tune_funcs import register_functions

register_functions()

PREFIX = '_gin'
SEPARATOR = '__'


@gin.configurable
def gin_tune_config(**kwargs):
    """Get tune config from gin config."""
    config = kwargs

    # loop over config rows
    for (scope, fcn), args in gin.config._CONFIG.items():

        # loop over functions
        for fcn_name, f in FUNCS.items():
            full_fcn_name = f['orig'].__module__ + '.' + fcn_name
            if fcn == full_fcn_name:
                with gin.config_scope(scope):
                    config[f"{PREFIX}{SEPARATOR}{scope}{SEPARATOR}{fcn_name}"] = f['gin'](pass_through=True, _scope=scope)

    return config

def _tune_gin_wrap_inner(config, function, checkpoint_dir=None, gin_config_str=None, pre_parse=None):
    """Bind gin parameters from tune config and call function on the resulting config."""
    if callable(pre_parse):
        pre_parse()

    gin.parse_config(gin_config_str)

    for key, value in config.items():
        if key.startswith(PREFIX):
            _, scope, name = key.split(SEPARATOR)
            gin.bind_parameter(scope + '/' + name + '.' + OVERRIDE_ATTR, value)
            gin.bind_parameter(scope + '/' + name + '._scope', scope)

    return function(config, checkpoint_dir=checkpoint_dir)

def tune_gin_wrap(function, pre_parse, gin_config_str):
    """Wrap around a function and process tune-gin parameters."""

    inner = partial(_tune_gin_wrap_inner, function=function, pre_parse=pre_parse,
                    gin_config_str=gin_config_str)
    inner.__name__ = function.__name__

    return inner


@gin.configurable
def tune_run(*args, **kwargs):
    """Run tune trial, gin-configurable."""
    return tune.run(*args, **kwargs)


@gin.configurable
def tune_gin(func, config_update=None, pre_parse=None, **kwargs):
    """Tune with gin capability."""
    gin_config_str = gin.config_str()
    func_wrapped = tune_gin_wrap(func, pre_parse=pre_parse, gin_config_str=gin_config_str)
    config = config_update if config_update else {}
    config.update(gin_tune_config())
    return tune_run(func_wrapped, config=config, **kwargs)
