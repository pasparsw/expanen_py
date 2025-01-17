from expanen.conflicting_enum_field import ConflictingEnumField
from expanen.expanen_field import ExpanenField


class ExpandableEnumType(type):
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        existing_fields = {field for base in bases for field in base.__dict__.values() if
                           isinstance(field, ExpanenField)}

        for name, value in dct.items():
            if name.startswith("__"):
                continue
            for field in existing_fields:
                raw_field_name: str = field.name.split(".")[-1]

                if raw_field_name == name or field.value == value:
                    raise ConflictingEnumField(f"Failed to create an expandable enum {new_class.__name__} due to "
                                               f"duplicated enum field! {new_class.__name__}.{name}: {value} conflicts "
                                               f"with {field.name}: {field.value}")

            cls.__setattr__(new_class, name, value)
            existing_fields.add(new_class(name, value))

        return new_class

    def __setattr__(cls, name, value):
        super().__setattr__(name, cls(f"{cls.__name__}.{name}", value))

    def __repr__(cls):
        return f"<enum '{cls.__name__}'>"
