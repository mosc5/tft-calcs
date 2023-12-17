from dataclasses import dataclass


@dataclass
class Unit:
    def __init__(self, name, cost, traits) -> None:
        self.name : str = name
        self.cost : int = cost  # maybe change to rarity/enum?
        self.traits : list[Trait] = traits

    def __repr__(self) -> str:
        return self.name


@dataclass
class Trait:
    def __init__(self, name, group_sizes) -> None:
        self.name : str = name
        self.group_sizes = sorted(group_sizes)

    def __repr__(self) -> str:
        return self.name
    
    def __hash__(self) -> int:
        return hash((self.name))
    
    def __eq__(self, other) -> int:
        return (self.name, self.group_sizes) == (other.name, other.group_sizes)
    
    def __ne__(self, other) -> int:
        return not(self == other)
    
    def __lt__(self, other):
         return self.name < other.name
    
    # TODO property for csv line repr
