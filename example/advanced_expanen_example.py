import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.expandable_enum import ExpandableEnum
from src.expandable_enum_field_base import ExpandableEnumFieldBase
# Error defines a custom type for each expandable enum field
class Error(ExpandableEnumFieldBase):
    @property
    def code(self) -> any:
        return self._value.split(": ")[0]

    @property
    def description(self) -> str:
        return self._value.split(": ")[1]

    def __str__(self) -> str:
        return f"{self.name}: {self.value}"
# define an expandable enum with a custom field type
class GenericError(ExpandableEnum):
    # custom underlying type of each enum field
    _field_type = Error

    CONNECTION_DROPPED: Error = "472: Connection has been dropped due to API policy violation"

error = GenericError.CONNECTION_DROPPED
# display standard properties of the enum field (name and value) and properties brought by the custom field Error
# (code and description)
print(f"error name: {error.name}")
print(f"error value: {error.value}")
print(f"error code: {error.code}")
print(f"error description: {error.description}")
