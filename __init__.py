import os
import sys

EXPANDABLE_ENUM_DIR: str = os.path.dirname(os.path.realpath(__file__))
sys.path.append(EXPANDABLE_ENUM_DIR)

from .src.expandable_enum import ExpandableEnum
from .src.expandable_enum_field_base import ExpandableEnumFieldBase
from .src.duplicated_enum_field import DuplicatedEnumField
