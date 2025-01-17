import os
import sys

EXPANDABLE_ENUM_DIR: str = os.path.dirname(os.path.realpath(__file__))
sys.path.append(EXPANDABLE_ENUM_DIR)

from .expanen.expanen import Expanen
