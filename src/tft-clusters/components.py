from dataclasses import dataclass


@dataclass
class Unit:
    def __init__(self, name, cost, origins, traits) -> None:
        self.name : str = name
        self.cost : int = cost  # maybe change to rarity/enum?
        self.origin : list(Origin) = origins
        self.trait : list(Trait) = traits


@dataclass
class Origin:
    def __init__(self, name, group_sizes) -> None:
        self.name : str = name
        self.group_sizes = sorted(group_sizes)


@dataclass
class Trait:
    def __init__(self, name, group_sizes) -> None:
        self.name : str = name
        self.group_sizes = sorted(group_sizes)
