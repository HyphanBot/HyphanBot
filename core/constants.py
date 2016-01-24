# This file exists because fuck Python.

import os

# Get Hyphan's root directory from the environment variable (exported in run.sh)
HYPHAN_DIR = os.getenv('HYPHAN_DIR', os.path.dirname(os.getcwd()))