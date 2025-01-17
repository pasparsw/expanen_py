from expanen.expandable_enum_type import ExpandableEnumType
from expanen.expanen_field import ExpanenField


class Expanen(ExpanenField, metaclass=ExpandableEnumType):
    pass
