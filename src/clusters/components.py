from dataclasses import dataclass


@dataclass
class Unit:
    def __init__(self, name, cost, traits) -> None:
        self.name : str = name
        self.cost : int = cost  # maybe change to rarity/enum?
        self.traits : list(Trait) = traits

    def __repr__(self) -> str:
        return self.name


@dataclass
class Trait:
    def __init__(self, name, group_sizes) -> None:
        self.name : str = name
        self.group_sizes = sorted(group_sizes)

    def __repr__(self) -> str:
        return self.name
