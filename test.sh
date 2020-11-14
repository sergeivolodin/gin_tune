#!/bin/bash

set -e

# running tests
pytest -o log_cli=True -s

# running the second test
cd small_test
python tune.py
cd ..
