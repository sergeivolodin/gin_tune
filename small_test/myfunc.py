import gin
from ray import tune


@gin.configurable
def f(config, x1, x2, checkpoint_dir=None):
    """Example function to tune."""
    tune.report(sum=x1 + x2)
