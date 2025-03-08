import os
import sys
import pytest
from pathlib import Path

# Get the project root directory (parent of tests directory)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
SRC_DIR = PROJECT_ROOT / 'src'

# Add the project root and src directory to PYTHONPATH if not already there
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR)) 