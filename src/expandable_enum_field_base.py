from src.expandable_enum_field_interface import ExpandableEnumFieldInterface


class ExpandableEnumFieldBase(ExpandableEnumFieldInterface):
    def __init__(self, name: str, value: any):
        self._name: str = name
        self._value: str = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> any:
        return self._value

    def __str__(self) -> str:
        return f"({self._name}: {self._value})"
