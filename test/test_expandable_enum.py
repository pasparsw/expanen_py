import unittest

from expanen.expandable_enum_type import ExpandableEnumType
from expanen.expanen import Expanen
from expanen.conflicting_enum_field import ConflictingEnumField
from expanen.expanen_field import ExpanenField


class TestExpanen(unittest.TestCase):
    def test_simple_enum(self):
        class E(Expanen):
            F1 = 123
            F2 = 456

        class G(Expanen):
            F1 = 123
            F2 = 456

        self.assertEqual(type(E), ExpandableEnumType)
        self.assertEqual(type(E.F1), E)
        self.assertEqual(type(E.F2), E)

        self.assertEqual(str(type(E)), "<class 'expanen.expandable_enum_type.ExpandableEnumType'>")
        self.assertEqual(str(type(E.F1)), "<enum 'E'>")
        self.assertEqual(str(type(E.F2)), "<enum 'E'>")

        self.assertEqual(str(E.F1), "(E.F1: 123)")
        self.assertEqual(str(E.F2), "(E.F2: 456)")

        self.assertEqual(E.F1.name, "E.F1")
        self.assertEqual(E.F2.name, "E.F2")

        self.assertEqual(E.F1.value, 123)
        self.assertEqual(E.F2.value, 456)

        self.assertEqual(E.F1, E.F1)
        self.assertEqual(E.F2, E.F2)

        self.assertNotEqual(E.F1, E.F2)
        self.assertNotEqual(E.F1, G.F1)
        self.assertNotEqual(E.F2, G.F2)

        self.assertEqual(len(E.__bases__), 1)
        self.assertEqual(E.__bases__[0], Expanen)

        self.assertEqual(len(E.__bases__[0].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[0], ExpanenField)

        self.assertEqual(len(E.__bases__[0].__bases__[0].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[0].__bases__[0], object)

    def test_expanded_enum(self):
        class B(Expanen):
            F1 = 12
            F2 = 34

        class E(B):
            F3 = 56
            F4 = 78

        self.assertEqual(type(E), ExpandableEnumType)
        self.assertEqual(type(E.F1), B)
        self.assertEqual(type(E.F2), B)
        self.assertEqual(type(E.F3), E)
        self.assertEqual(type(E.F4), E)

        self.assertEqual(str(type(E)), "<class 'expanen.expandable_enum_type.ExpandableEnumType'>")
        self.assertEqual(str(type(E.F1)), "<enum 'B'>")
        self.assertEqual(str(type(E.F2)), "<enum 'B'>")
        self.assertEqual(str(type(E.F3)), "<enum 'E'>")
        self.assertEqual(str(type(E.F4)), "<enum 'E'>")

        self.assertEqual(str(E.F1), "(B.F1: 12)")
        self.assertEqual(str(E.F2), "(B.F2: 34)")
        self.assertEqual(str(E.F3), "(E.F3: 56)")
        self.assertEqual(str(E.F4), "(E.F4: 78)")

        self.assertEqual(E.F1.name, "B.F1")
        self.assertEqual(E.F2.name, "B.F2")
        self.assertEqual(E.F3.name, "E.F3")
        self.assertEqual(E.F4.name, "E.F4")

        self.assertEqual(E.F1.value, 12)
        self.assertEqual(E.F2.value, 34)
        self.assertEqual(E.F3.value, 56)
        self.assertEqual(E.F4.value, 78)

        self.assertEqual(E.F1, B.F1)
        self.assertEqual(E.F2, B.F2)
        self.assertEqual(E.F1, E.F1)
        self.assertEqual(E.F2, E.F2)
        self.assertEqual(E.F3, E.F3)
        self.assertEqual(E.F4, E.F4)

        self.assertEqual(len(E.__bases__), 1)
        self.assertEqual(E.__bases__[0], B)

        self.assertEqual(len(E.__bases__[0].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[0], Expanen)

        self.assertEqual(len(E.__bases__[0].__bases__[0].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[0].__bases__[0], ExpanenField)

        self.assertEqual(len(E.__bases__[0].__bases__[0].__bases__[0].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[0].__bases__[0].__bases__[0], object)

    def test_multiple_expansions(self):
        class B(Expanen):
            F1 = 12

        class E1(B):
            F2 = 34

        class E2(E1):
            F3 = 56

        self.assertEqual(type(E2), ExpandableEnumType)
        self.assertEqual(type(E2.F1), B)
        self.assertEqual(type(E2.F2), E1)
        self.assertEqual(type(E2.F3), E2)

        self.assertEqual(str(type(E2)), "<class 'expanen.expandable_enum_type.ExpandableEnumType'>")
        self.assertEqual(str(type(E2.F1)), "<enum 'B'>")
        self.assertEqual(str(type(E2.F2)), "<enum 'E1'>")
        self.assertEqual(str(type(E2.F3)), "<enum 'E2'>")

        self.assertEqual(str(E2.F1), "(B.F1: 12)")
        self.assertEqual(str(E2.F2), "(E1.F2: 34)")
        self.assertEqual(str(E2.F3), "(E2.F3: 56)")

        self.assertEqual(E2.F1.name, "B.F1")
        self.assertEqual(E2.F2.name, "E1.F2")
        self.assertEqual(E2.F3.name, "E2.F3")

        self.assertEqual(E2.F1.value, 12)
        self.assertEqual(E2.F2.value, 34)
        self.assertEqual(E2.F3.value, 56)

        self.assertEqual(E2.F1, B.F1)
        self.assertEqual(E2.F1, E1.F1)
        self.assertEqual(E2.F2, E1.F2)
        self.assertEqual(E2.F3, E2.F3)

    def test_duplicated_field_name(self):
        class B(Expanen):
            F = 0

        with self.assertRaises(ConflictingEnumField):
            class E(B):
                F = 1

    def test_duplicated_field_value(self):
        class B(Expanen):
            F = 0

        with self.assertRaises(ConflictingEnumField):
            class ExpandedEnum(B):
                G = 0

    def test_custom_enum_field_type(self):
        class CustomFieldType:
            @property
            def code(self) -> int:
                return int(self.value.split(": ")[0])

            @property
            def description(self) -> str:
                return self.value.split(": ")[1]

        class E(Expanen, CustomFieldType):
            F1 = "123: Some description"
            F2 = "456: Some other description"

        self.assertEqual(type(E), ExpandableEnumType)
        self.assertEqual(type(E.F1), E)
        self.assertEqual(type(E.F2), E)

        self.assertEqual(str(type(E)), "<class 'expanen.expandable_enum_type.ExpandableEnumType'>")
        self.assertEqual(str(type(E.F1)), "<enum 'E'>")
        self.assertEqual(str(type(E.F2)), "<enum 'E'>")

        self.assertEqual(str(E.F1), "(E.F1: 123: Some description)")
        self.assertEqual(str(E.F2), "(E.F2: 456: Some other description)")

        self.assertEqual(E.F1.name, "E.F1")
        self.assertEqual(E.F2.name, "E.F2")

        self.assertEqual(E.F1.value, "123: Some description")
        self.assertEqual(E.F2.value, "456: Some other description")

        self.assertEqual(E.F1.code, 123)
        self.assertEqual(E.F2.code, 456)

        self.assertEqual(E.F1.description, "Some description")
        self.assertEqual(E.F2.description, "Some other description")

        self.assertEqual(len(E.__bases__), 2)
        self.assertEqual(E.__bases__[0], Expanen)
        self.assertEqual(E.__bases__[1], CustomFieldType)

        self.assertEqual(len(E.__bases__[0].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[0], ExpanenField)

        self.assertEqual(len(E.__bases__[1].__bases__), 1)
        self.assertEqual(E.__bases__[1].__bases__[0], object)

        self.assertEqual(len(E.__bases__[0].__bases__[0].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[0].__bases__[0], object)

    def test_different_custom_enum_field_types_across_hierarchy(self):
        class BFieldType:
            pass

        class EFieldType:
            pass

        class B(Expanen, BFieldType):
            F1 = 0

        class E(B, EFieldType):
            F2 = 1

        self.assertEqual(type(E), ExpandableEnumType)
        self.assertEqual(type(E.F1), B)
        self.assertEqual(type(E.F2), E)

        self.assertEqual(str(type(E)), "<class 'expanen.expandable_enum_type.ExpandableEnumType'>")
        self.assertEqual(str(type(E.F1)), "<enum 'B'>")
        self.assertEqual(str(type(E.F2)), "<enum 'E'>")

        self.assertEqual(str(E.F1), "(B.F1: 0)")
        self.assertEqual(str(E.F2), "(E.F2: 1)")

        self.assertEqual(E.F1.name, "B.F1")
        self.assertEqual(E.F2.name, "E.F2")

        self.assertEqual(E.F1.value, 0)
        self.assertEqual(E.F2.value, 1)

        self.assertEqual(len(E.__bases__), 2)
        self.assertEqual(E.__bases__[0], B)
        self.assertEqual(E.__bases__[1], EFieldType)

        self.assertEqual(len(E.__bases__[0].__bases__), 2)
        self.assertEqual(E.__bases__[0].__bases__[0], Expanen)
        self.assertEqual(E.__bases__[0].__bases__[1], BFieldType)

        self.assertEqual(len(E.__bases__[1].__bases__), 1)
        self.assertEqual(E.__bases__[1].__bases__[0], object)

        self.assertEqual(len(E.__bases__[0].__bases__[0].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[0].__bases__[0], ExpanenField)

        self.assertEqual(len(E.__bases__[0].__bases__[0].__bases__[0].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[0].__bases__[0].__bases__[0], object)

        self.assertEqual(len(E.__bases__[0].__bases__[1].__bases__), 1)
        self.assertEqual(E.__bases__[0].__bases__[1].__bases__[0], object)
