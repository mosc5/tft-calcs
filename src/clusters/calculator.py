from clusters.components import Unit, Trait

from bisect import bisect
import itertools
import json
import pathlib


class SetBasics:
    def __init__(self, json_path: pathlib.Path) -> None:
        self.traits : dict(str, Trait) = None
        self.units : dict(str, Unit) = None

        self._setup_from_json(json_path)


    def _setup_from_json(self, json_path: pathlib.Path):
        if not json_path.exists():
            raise FileNotFoundError(f"Input file does not exist at {json_path}!")

        with open(json_path, "r") as f:
            data = json.load(f)
        
        # create traits, units
        self._create_traits(data["components"]["traits"])
        self._create_units(data["components"]["units"])

    def _create_traits(self, trait_dict):
        if self.traits is not None:
            raise ValueError("Traits already exist and can't be created.")
        self.traits = {}
        for name, value in trait_dict.items():
            self.traits[name] = Trait(name, value["group_sizes"])

    def _create_units(self, unit_dict):
        if self.units is not None:
            raise ValueError("Units already exist and can't be created.")
        self.units = {}
        for name, value in unit_dict.items():
            # TODO errors if traits don't exist
            traits = [self.traits[trait_name] for trait_name in value["traits"]]
            self.units[name] = Unit(name, value["cost"], traits)


class Calculator:
    def __init__(self, basics: SetBasics) -> None:
        self.basics : SetBasics = basics
    
    def calculate_clusters(self, min_size=2, max_size=4, duplicate_unit_filter: str=None, max_score_below_clustersize:int=1):
        clusters = []
        for i in range(min_size, max_size + 1):
            for unit_cluster in list(itertools.combinations(self.basics.units.values(), i)):
                if duplicate_unit_filter is not None:
                    filter_units = [u for u in unit_cluster if duplicate_unit_filter in u.name]
                    if len(filter_units) > 1:
                        continue
                cluster = Cluster(unit_cluster)
                cluster.calculate_score(self.basics)
                if cluster.score and cluster.score >= i - max_score_below_clustersize:
                    clusters.append(cluster)

        return sorted(clusters, key=lambda y: (-y.score, y.num_units))



class Cluster:
    def __init__(self, units) -> None:
        self.units = units
        self.score = 0
        self.trait_scores = None
    
    def calculate_score(self, basics):
        score = self.calculate_breakpoint_number(basics)
        # if any unit doesn't contribute to the score, return 0 (cluster is bad)
        for unit in self.units:
            new_cluster = [u for u in self.units if u is not unit]
            new_score = self.calculate_breakpoint_number(basics, new_cluster)
            if new_score >= score:
                return 0
        self.score = score

    def calculate_breakpoint_number(self, basics, alt_cluster=None):
        counters = {}
        units = self.units if alt_cluster is None else alt_cluster
        for unit in units:
            for trait in unit.traits:
                if trait in counters:
                    counters[trait] += 1
                else:
                    counters[trait] = 1
        score = 0
        trait_scores = {}
        for trait, counter in counters.items():
            trait_score = bisect(trait.group_sizes, counter)
            score += trait_score
            if trait_score:
                trait_scores[trait] = {"score": trait_score, "group_size": counter}
        if alt_cluster is None:
            self.trait_scores = counters
        return score

    @property
    def num_units(self):
        return len(self.units)
    
    @property
    def costs(self):
        return sorted(list(set([u.cost for u in self.units])))
    
    @property
    def traits(self):
        if self.trait_scores:
            return sorted(list(set([x for x in self.trait_scores])))
