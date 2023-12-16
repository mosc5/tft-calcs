from clusters.calculator import Calculator, SetBasics

import pathlib


def main():
    json_path = pathlib.Path("data", "set_10", "components.json")
    save_path = pathlib.Path("data", "set_10", "clusters.csv")

    set_basics = SetBasics(json_path)
    calculator = Calculator(set_basics)
    clusters = calculator.calculate_clusters(duplicate_unit_filter="Akali")

    with open(save_path, "w") as f:
        f.write('\n'.join('{},{},{}'.format(x[0],x[1],x[2]) for x in clusters))


if __name__ == "__main__":
    main()