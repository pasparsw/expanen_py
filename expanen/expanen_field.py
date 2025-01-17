class ExpanenField:
    def __init__(self, name: str, value: any):
        self.name: str = name
        self.value: any = value

    def __str__(self) -> str:
        return f"({self.name}: {self.value})"
