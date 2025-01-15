import unittest

from src.expandable_enum import ExpandableEnum
from src.duplicated_enum_field import DuplicatedEnumField
from src.expandable_enum_field_base import ExpandableEnumFieldBase


class TestExpandableEnum(unittest.TestCase):
    def test_simple_enum(self):
        class SimpleEnum(ExpandableEnum):
            FIELD_NAME_1 = 123
            FIELD_NAME_2 = 456

        instance_1 = SimpleEnum.FIELD_NAME_1
        instance_2 = SimpleEnum.FIELD_NAME_2

        self.assertTrue(isinstance(instance_1, SimpleEnum))
        self.assertTrue(isinstance(instance_2, SimpleEnum))

        self.assertEqual(instance_1, instance_1)
        self.assertNotEqual(instance_1, instance_2)

        self.assertEqual(instance_1.name, "SimpleEnum.FIELD_NAME_1")
        self.assertEqual(instance_2.name, "SimpleEnum.FIELD_NAME_2")
        self.assertEqual(instance_1.value, 123)
        self.assertEqual(instance_2.value, 456)

    def test_expanded_enum(self):
        class BaseEnum(ExpandableEnum):
            FIELD_NAME_1 = 12
            FIELD_NAME_2 = 34

        class ExpandedEnum(BaseEnum):
            FIELD_NAME_3 = 56
            FIELD_NAME_4 = 78

        base_instance_1 = BaseEnum.FIELD_NAME_1
        base_instance_2 = BaseEnum.FIELD_NAME_2
        base_via_spec_instance_1 = ExpandedEnum.FIELD_NAME_1
        base_via_spec_instance_2 = ExpandedEnum.FIELD_NAME_2
        spec_instance_1 = ExpandedEnum.FIELD_NAME_3
        spec_instance_2 = ExpandedEnum.FIELD_NAME_4

        self.assertTrue(isinstance(base_instance_1, BaseEnum))
        self.assertTrue(isinstance(base_instance_2, BaseEnum))
        self.assertTrue(isinstance(base_via_spec_instance_1, BaseEnum))
        self.assertTrue(isinstance(base_via_spec_instance_2, BaseEnum))
        self.assertTrue(isinstance(spec_instance_1, ExpandedEnum))
        self.assertTrue(isinstance(spec_instance_2, ExpandedEnum))

        self.assertEqual(base_instance_1, base_via_spec_instance_1)
        self.assertEqual(base_instance_2, base_via_spec_instance_2)

        self.assertEqual(base_instance_1.name, "BaseEnum.FIELD_NAME_1")
        self.assertEqual(base_instance_1.value, 12)
        self.assertEqual(base_instance_2.name, "BaseEnum.FIELD_NAME_2")
        self.assertEqual(base_instance_2.value, 34)

        self.assertEqual(base_via_spec_instance_1.name, "BaseEnum.FIELD_NAME_1")
        self.assertEqual(base_via_spec_instance_1.value, 12)
        self.assertEqual(base_via_spec_instance_2.name, "BaseEnum.FIELD_NAME_2")
        self.assertEqual(base_via_spec_instance_2.value, 34)

        self.assertEqual(spec_instance_1.name, "ExpandedEnum.FIELD_NAME_3")
        self.assertEqual(spec_instance_1.value, 56)
        self.assertEqual(spec_instance_2.name, "ExpandedEnum.FIELD_NAME_4")
        self.assertEqual(spec_instance_2.value, 78)

    def test_multiple_expansions(self):
        class BaseEnum(ExpandableEnum):
            FIELD_NAME_1 = 12

        class ExpandedEnumLevel1(BaseEnum):
            FIELD_NAME_2 = 34

        class ExpandedEnumLevel2(ExpandedEnumLevel1):
            FIELD_NAME_3 = 56

        base_instance = BaseEnum.FIELD_NAME_1
        base_via_level_1_instance = ExpandedEnumLevel1.FIELD_NAME_1
        level_1_instance = ExpandedEnumLevel1.FIELD_NAME_2
        base_via_level_2_instance = ExpandedEnumLevel2.FIELD_NAME_1
        level_1_via_level_2_instance = ExpandedEnumLevel2.FIELD_NAME_2
        level_2_instance = ExpandedEnumLevel2.FIELD_NAME_3

        self.assertTrue(isinstance(base_instance, BaseEnum))
        self.assertTrue(isinstance(base_via_level_1_instance, BaseEnum))
        self.assertTrue(isinstance(level_1_instance, ExpandedEnumLevel1))
        self.assertTrue(isinstance(base_via_level_2_instance, BaseEnum))
        self.assertTrue(isinstance(level_1_via_level_2_instance, ExpandedEnumLevel1))
        self.assertTrue(isinstance(level_2_instance, ExpandedEnumLevel2))

        self.assertEqual(base_instance, base_via_level_1_instance)
        self.assertEqual(base_instance, base_via_level_2_instance)
        self.assertEqual(level_1_instance, level_1_via_level_2_instance)

        self.assertEqual(base_instance.name, "BaseEnum.FIELD_NAME_1")
        self.assertEqual(base_instance.value, 12)
        self.assertEqual(base_via_level_1_instance.name, "BaseEnum.FIELD_NAME_1")
        self.assertEqual(base_via_level_1_instance.value, 12)
        self.assertEqual(base_via_level_2_instance.name, "BaseEnum.FIELD_NAME_1")
        self.assertEqual(base_via_level_2_instance.value, 12)

        self.assertEqual(level_1_instance.name, "ExpandedEnumLevel1.FIELD_NAME_2")
        self.assertEqual(level_1_instance.value, 34)
        self.assertEqual(level_1_via_level_2_instance.name, "ExpandedEnumLevel1.FIELD_NAME_2")
        self.assertEqual(level_1_via_level_2_instance.value, 34)

        self.assertEqual(level_2_instance.name, "ExpandedEnumLevel2.FIELD_NAME_3")
        self.assertEqual(level_2_instance.value, 56)
        
    def test_duplicated_field_name(self):
        class BaseEnum(ExpandableEnum):
            FIELD_NAME = 0

        with self.assertRaises(DuplicatedEnumField):
            class ExpandedEnum(BaseEnum):
                FIELD_NAME = 1

    def test_duplicated_field_value(self):
        class BaseEnum(ExpandableEnum):
            FIELD_NAME = 0

        with self.assertRaises(DuplicatedEnumField):
            class ExpandedEnum(BaseEnum):
                FIELD_OTHER_NAME = 0

    def test_custom_enum_field_type(self):
        class CustomFieldType(ExpandableEnumFieldBase):
            @property
            def code(self) -> int:
                return int(self.value.split(": ")[0])

            @property
            def description(self) -> str:
                return self.value.split(": ")[1]

        class BaseEnum(ExpandableEnum):
            _field_type = CustomFieldType

            FIELD_NAME = "123: Some description"
            FIELD_OTHER_NAME = "456: Some other description"

        instance_1 = BaseEnum.FIELD_NAME
        instance_2 = BaseEnum.FIELD_OTHER_NAME

        self.assertTrue(isinstance(instance_1, BaseEnum))
        self.assertTrue(isinstance(instance_2, BaseEnum))
        self.assertTrue(isinstance(instance_1, CustomFieldType))
        self.assertTrue(isinstance(instance_2, CustomFieldType))

        self.assertEqual(instance_1.name, "BaseEnum.FIELD_NAME")
        self.assertEqual(instance_1.value, "123: Some description")
        self.assertEqual(instance_1.code, 123)
        self.assertEqual(instance_1.description, "Some description")

        self.assertEqual(instance_2.name, "BaseEnum.FIELD_OTHER_NAME")
        self.assertEqual(instance_2.value, "456: Some other description")
        self.assertEqual(instance_2.code, 456)
        self.assertEqual(instance_2.description, "Some other description")
