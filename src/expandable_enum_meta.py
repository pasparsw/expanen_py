from src.duplicated_enum_field import DuplicatedEnumField
from src.expandable_enum_field_base import ExpandableEnumFieldBase

FIELD_TYPE_SPECIFIER_NAME: str = "_field_type"


class ExpandableEnumMeta(type):
    def __new__(cls, name, bases, dct):
        enum_field_type = dct.get(FIELD_TYPE_SPECIFIER_NAME, ExpandableEnumFieldBase)

        if not any(issubclass(base, enum_field_type) for base in bases):
            bases = (enum_field_type,) + bases

        new_class = super().__new__(cls, name, bases, dct)
        existing_fields = {field for base in bases for field in base.__dict__.values() if isinstance(field, enum_field_type)}

        for name, value in dct.items():
            if name.startswith("__") or name == FIELD_TYPE_SPECIFIER_NAME:
                continue
            for field in existing_fields:
                raw_field_name: str = field.name.split(".")[-1]

                if raw_field_name == name or field.value == value:
                    raise DuplicatedEnumField(f"Failed to create an expandable enum {new_class.__name__} due to "
                                              f"duplicated enum field! {new_class.__name__}.{name}: {value} conflicts "
                                              f"with {field.name}: {field.value}")

            cls.__setattr__(new_class, name, value)
            existing_fields.add(new_class(name, value))

        return new_class

    def __setattr__(cls, name, value):
        super().__setattr__(name, cls(f"{cls.__name__}.{name}", value))