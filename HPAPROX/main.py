from HPAPROX.dataIO import read_all, read, Data
import matplotlib.pyplot as plt
from numpy import linspace


def interpolate_point_lagrange(xi, data: [Data]):
    result: float = 0.0
    length = len(data)
    for i in range(length):
        term: float = data[i].y
        for j in range(length):
            if i != j:
                term *= (xi - data[j].x)/float(data[i].x - data[j].x)
        result += term

    print("Interpolated point", xi)
    return result


def interpolate_lagrange(data: [Data], interpolation_range=None) -> [Data]:
    if interpolation_range is None:
        interpolation_range = len(data)

    lin_x = linspace(data[0].x, data[-1].x, interpolation_range)

    return [Data(lin_x[i], interpolate_point_lagrange(lin_x[i], data)) for i in range(interpolation_range)]


def process(dataset: [Data]):
    # plt.plot(
    #     [point.x for point in dataset],
    #     [point.y for point in dataset],
    #     'b.',
    #     label='raw dataset'
    # )
    # plt.show()

    interpolated_data = interpolate_lagrange(dataset, len(dataset)*2)

    plt.plot(
        [point.x for point in dataset],
        [point.y for point in dataset],
        'b.',
        label='raw dataset'
    )
    plt.plot(
        [point.x for point in interpolated_data],
        [point.y for point in interpolated_data],
        'r-',
        label='interpolated'
    )
    plt.legend()
    # plt.yscale("log")
    plt.show()


def all_data():
    data: [[Data]] = read_all()
    for dataset in data:
        process(dataset)
    # for dataset in data:
    #     for line in dataset:
    #         print(line)


def single_file(filename='./data/100.txt'):
    data: [Data] = read(filename)
    process(data)


def main():
    # all_data()
    single_file('./data/Redlujjj.txt')  # largest file


if __name__ == '__main__':
    main()
