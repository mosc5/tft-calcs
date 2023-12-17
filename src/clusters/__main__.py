from clusters.calculator import Calculator, SetBasics, get_perfect_clusters

import pathlib


def main():
    json_path = pathlib.Path("data", "set_10", "components.json")
    save_path = pathlib.Path("data", "set_10", "clusters.csv")
    save_path_2 = pathlib.Path("data", "set_10", "perfect_clusters.csv")

    set_basics = SetBasics(json_path)
    calculator = Calculator(set_basics)
    # clusters = calculator.calculate_clusters(duplicate_unit_filter="Akali", min_size=2, max_size=4, max_score_below_clustersize=0)

    # with open(save_path, "w") as f:
    #     f.write('\n'.join('{},{},{}'.format(x.score,x.num_units,";".join(y.name for y in x.units)) for x in clusters))
    #     # TODO more outputs (traits, costs, etc)
    
    # perfect_clusters = get_perfect_clusters(clusters)

    perfect_clusters = calculator.calculate_clusters(duplicate_unit_filter="Akali", min_size=3, max_size=6, max_score_below_clustersize=2, require_perfect=True)

    with open(save_path_2, "w") as f:
        f.write('\n'.join('{},{},{}'.format(x.score,x.num_units,";".join(y.name for y in x.units)) for x in perfect_clusters))


if __name__ == "__main__":
    main()