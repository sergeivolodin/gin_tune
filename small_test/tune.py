from gin_tune import tune_gin
from myfunc import f
import gin
import logging


if __name__ == '__main__':
    gin.parse_config_file('config.gin')
    analysis = tune_gin(f)
    logging.basicConfig(level=logging.INFO)

    print("Sum results")
    print(sorted([y['sum'] for y in analysis.results.values()]))
