from abc import abstractmethod


class ExpandableEnumFieldInterface:
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def value(self) -> any:
        pass
