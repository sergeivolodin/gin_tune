import ray.tune as tune
import gin

# function argument the value of which the function returns
OVERRIDE_ATTR = '_override'

# map name -> function
FUNCS = {}

DEFAULT_OVERRIDE = "Use tune_gin() instead of tune.run()"

def register_func(f):
    """Register tune function."""
    FUNCS[f.__name__] = f
    return f

@gin.configurable
@register_func
def grid_search(values, _override=DEFAULT_OVERRIDE):
    if _override == DEFAULT_OVERRIDE:
        raise ValueError(DEFAULT_OVERRIDE)
    return _override

@gin.configurable
@register_func
def choice(categories, _override=DEFAULT_OVERRIDE):
    if _override == DEFAULT_OVERRIDE:
        raise ValueError(DEFAULT_OVERRIDE)
    return _override

@gin.configurable
@register_func
def sample_from(func, _override=DEFAULT_OVERRIDE):
    if _override == DEFAULT_OVERRIDE:
        raise ValueError(DEFAULT_OVERRIDE)
    return _override

@gin.configurable
@register_func
def uniform(lower, upper, _override=DEFAULT_OVERRIDE):
    if _override == DEFAULT_OVERRIDE:
        raise ValueError(DEFAULT_OVERRIDE)
    return _override

@gin.configurable
@register_func
def loguniform(lower, upper, base=10, _override=DEFAULT_OVERRIDE):
    if _override == DEFAULT_OVERRIDE:
        raise ValueError(DEFAULT_OVERRIDE)
    return _override