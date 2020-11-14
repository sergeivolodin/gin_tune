import gin
import gin_tune
import os
from ray import tune
from gin_tune import tune_gin
import logging


@gin.configurable
def f(x):
    """A function with one argument."""
    return x

@gin.configurable
def g(x1, x2):
    """A function with two arguments"""
    return (x1, x2)


def fcn(config, checkpoint_dir=None):
    """Function to run."""
    logging.basicConfig(level=logging.INFO)
    res = g()
    tune.report(res=res)

def test_tune(caplog):
    caplog.set_level(logging.INFO)
    logging.basicConfig(level=logging.INFO)
    conf_test = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.gin')
    gin.parse_config_file(conf_test)

    # running tune
    res = tune_gin(fcn)

    # checking results
    res = {x['res'] for x in res.results.values()}

    assert res == {(456, 'caba'), (456, 999), (123, 'caba'), (123, 999)}

    gin.clear_config()
