import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from expanen.expanen import Expanen
from expanen.conflicting_enum_field import ConflictingEnumField

# this is a base enum which is intended to be extended by its specializations
class GenericError(Expanen):
    INVALID_TOKEN = 0
    CONNECTION_DROPPED = 1
# this is an extended enum - it allows for accessing all the values existing in its base class (GenericError), but
# extends it with some more specific values
class SpecializedError(GenericError):
    INCORRECT_PRICE = 2
    OUT_OF_FUNDS = 3
# this extended enum is invalid because its field INVALID_ARGUMENT has the same value (1) as CONNECTION_DROPPED from
# its base class (GenericError)
try:
    class IncorrectSpecializationDuplicatedValue(GenericError):
        INVALID_ARGUMENT = 1
except ConflictingEnumField as e:
    print(f"ERROR: {e}")
# this extended enum is also invalid because its field CONNECTION_DROPPED has the same name (1) as the field from
# its base class (GenericError)
try:
    class IncorrectSpecializationDuplicatedName(GenericError):
        CONNECTION_DROPPED = 2
except ConflictingEnumField as e:
    print(f"ERROR: {e}")
# example of how to:
#  * access values in expandable enums
#  * access base expandable enum values via specialized enum
#  * access specialized enum values
gen_error_1 = GenericError.INVALID_TOKEN
gen_error_2 = GenericError.CONNECTION_DROPPED
gen_via_spec_error_1 = SpecializedError.INVALID_TOKEN
gen_via_spec_error_2 = SpecializedError.CONNECTION_DROPPED
spec_error_1 = SpecializedError.INCORRECT_PRICE
spec_error_2 = SpecializedError.OUT_OF_FUNDS
# GenericError values are of type GenericError
print(f"gen_error_1 = {gen_error_1}, type: {type(gen_error_1)}")
print(f"gen_error_2 = {gen_error_2}, type: {type(gen_error_2)}")
# SpecializedError values derived from GenericError are also of type GenericError
print(f"gen_via_spec_error_1 = {gen_via_spec_error_1}, type: {type(gen_via_spec_error_1)}")
print(f"gen_via_spec_error_2 = {gen_via_spec_error_2}, type: {type(gen_via_spec_error_2)}")
# SpecializedError values are of type SpecializedError
print(f"spec_error_1 = {spec_error_1}, type: {type(spec_error_1)}")
print(f"spec_error_2 = {spec_error_2}, type: {type(spec_error_2)}")
