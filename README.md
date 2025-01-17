# ExpanEn for Python
Table of contents:

[What is it?](#what_is_it)<br>
[Expandable enums properties](#expandable_enums_properties)<br>
[How to use it?](#how_to_use_it)<br>
&emsp;[Creating first expandable enum](#creating_first_expandable_enum)<br>
&emsp;[Creating first expanded enum](#creating_first_expanded_enum)<br>
&emsp;[Creating enum with a custom field type](#creating_enum_with_custom_field_type)<br>
[Errors](#errors)<br>
&emsp;[Duplicated field name](#duplicated_field_name)<br>
&emsp;[Duplicated field value](#duplicated_field_value)<br>

## <a name="what_is_it"></a>What is it?

ExpanEn (**Expan**dable **En**um) is a Python utility allowing user to define an expandable enum type. By default, Python enums
don't allow for derivation of any kind from other enum types. ExpanEn allows you to do exactly that - define a base
enum with some set of values and then extend it by other values specified in the classes deriving from it, remaining
type consistency.

## <a name="expandable_enums_properties"></a>Expandable enums properties

Let's say there are two expandable enums `B` and `E` with the following properties:
* `B` contains field `F1`
* `E` contains field `F2`
* `E` derives from `B`

Then the generic expandable enum properties are defined as:
* `B::F1` and `E::F1` are of type `B`
* `B::F1` == `E.F1`
* `E::F2` is of type `E`

Additionally, none of the fields in `E` can share the same field name **or** field value as any of the fields in `B`. To 
read more details about expandable enum properties, visit https://pikotutorial.com/ .

## <a name="how_to_use_it"></a>How to use it?

### <a name="creating_first_expandable_enum"></a>Creating first expandable enum

Expandable enums are created in the same way as the default Python enums, i.e. by derivation from the specific base class:

```python
from expanen_py import Expanen

class GenericError(Expanen):
    INVALID_TOKEN = 0
    CONNECTION_DROPPED = 1
```

This is a base enum which can be used like every other enum, but it can also function as a base enum for other expanded
enums. You can access its fields' names and values in the same way as in case of the default Python enums:

```python
print(GenericError.INVALID_TOKEN)                   # prints "(GenericError.INVALID_TOKEN: 0)"
print(f"name: {GenericError.INVALID_TOKEN.name}")   # prints "name: GenericError.INVALID_TOKEN"
print(f"value: {GenericError.INVALID_TOKEN.value}") # prints "value: 0"
```

### <a name="creating_first_expanded_enum"></a>Creating first expanded enum

After you have a base enum to derive from, you can use it define other enums by deriving from it:

```python
class TransactionError(GenericError):
    INCORRECT_PRICE = 2

class AccountError(GenericError):
    OUT_OF_FUNDS = 2
```

`TransactionError` and `AccountError` share `INVALID_TOKEN` and `CONNECTION_DROPPED` fields derived from `GenericError`,
but they also provide fields specific to their domains (`INCORRECT_PRICE` and `OUT_OF_FUNDS`). The types are consistent
across this hierarchy, so accordingly to [expandable enums properties](#expandable_enums_properties), in this case the 
types are:

```python
print(type(GenericError.INVALID_TOKEN))          # prints "<class '__main__.GenericError'>"
print(type(GenericError.CONNECTION_DROPPED))     # prints "<class '__main__.GenericError'>"
print(type(TransactionError.INVALID_TOKEN))      # prints "<class '__main__.GenericError'>"
print(type(TransactionError.CONNECTION_DROPPED)) # prints "<class '__main__.GenericError'>"
print(type(TransactionError.INCORRECT_PRICE))    # prints "<class '__main__.TransactionError'>"
```

The behavior of AccountError fields' types is analogous.

### <a name="creating_enum_with_custom_field_type"></a>Creating enum with a custom field type

As shown above, the default enum field type allows you to access enum field's `name` and `value`. If this is however not
enough for your application and you want to apply some custom behavior, you can do it by defining a custom enum field
type which must derive from `ExpanenField`. The base class provides basic constructor and implementation of 
the properties `name` and `value`, so that custom field types may re-use it.

Let's say that the value of an enum is not a simple value, but encodes complex information. For example, 
value of an enum field of a certain error may contain a string with an error code and a detailed description of that 
error in the following format:

```
error_code: Error description
```

While using such enum you would most probably want to use error code and error description separately for different purposes,
so you would have to have some utility which allows you to parse the field's value and extract error code and error
description from it. With **ExpanEn**, you can embed such utility directly in the enum field's type by defining a custom
enum field type:

```python
class ErrorCodeAndDescription:
    @property
    def code(self) -> int:
        return int(self.value.split(": ")[0])

    @property
    def description(self) -> str:
        return self.value.split(": ")[1]
```

Such type can be then to derive from when creating an expandable enum:

```python
class GenericError(Expanen, ErrorCodeDescription):
    INVALID_TOKEN = "4837: Invalid token has been provided"
    CONNECTION_DROPPED = "9572: Connection dropped due to API policy violation"
```

From now on, `INVALID_TOKEN`, `CONNECTION_DROPPED` and every other field of `GenericError` enum will derive from 
`ErrorCodeAndDescription` type allowing to utilize its functionalities:

```python
error = GenericError.CONNECTION_DROPPED

print(error.name)        # prints "GenericError.CONNECTION_DROPPED"
print(error.value)       # prints "9572: Connection dropped due to API policy violation"
print(error.code)        # prints "9572"
print(error.description) # prints "Connection dropped due to API policy violation"
```

Although it's most probably not the best practice, it is technically allowed to have different enum field types across 
the entire enum hierarchy. For example, such code is valid and works:

```python
class Square:
    def get_area(self):
        return self.value ** 2

class Point:
    def get_coordinates(self):
        return f"x = {self.value[0]}, y = {self.value[1]}"

class B(Expanen, Square):
    F1 = 5

class E(B, Point):
    F2 = (12, 24)

print(B.F1.get_area())         # prints "25"
print(E.F2.get_coordinates())  # prints "x = 12, y = 24"
```

## <a name="errors"></a>Errors

There are 2 main errors which you may expect when misusing ExpanEn.

### <a name="duplicated_field_name"></a>Duplicated field name

It is forbidden to define 2 fields with the same name across the entire enum hierarchy:

```python
class Base(Expanen):
    FIELD = 0

class Extended(Base):
    FIELD = 1
```

The above code will raise `ConflictingEnumField` exception with the following error prompt:

```
ConflictingEnumField: Failed to create an expandable enum Extended due to duplicated enum field! Extended.FIELD: 1 
conflicts with Base.FIELD: 0
```

### <a name="duplicated_field_value"></a>Duplicated field value

It is forbidden to define 2 fields with the same value across the entire enum hierarchy:

```python
class Base(Expanen):
    FIELD = 0

class Extended(Base):
    OTHER_FIELD = 0
```

The above code will raise `ConflictingEnumField` exception with the following error prompt:

```
ConflictingEnumField: Failed to create an expandable enum Extended due to duplicated enum field! Extended.OTHER_FIELD: 0 
conflicts with Base.FIELD: 0
```
