from HPAPROX.dataIO import read_all, read, Data
import matplotlib.pyplot as plt
from numpy import linspace
from multiprocessing import Pool
from functools import partial


def interpolate_point_lagrange(xi, data: [Data]):
    result: float = 0.0
    length = len(data)
    for i in range(length):
        term: float = data[i].y
        for j in range(length):
            if i != j:
                term *= (xi - data[j].x)/float(data[i].x - data[j].x)
        result += term

    print("Interpolated point", xi, "result", result)
    return result


def interpolate_lagrange(data: [Data], interpolation_density=None) -> [Data]:
    if interpolation_density is None:
        interpolation_density = len(data)

    lin_x = linspace(data[0].x, data[-1].x, interpolation_density)
    print("Max:", lin_x[-1])

    return [Data(lin_x[i], interpolate_point_lagrange(lin_x[i], data)) for i in range(interpolation_density)]
    #
    # pdata = partial(interpolate_point_lagrange, data=data)
    #
    # with Pool(5) as pool:
    #     print(pool)
    #     int_y = pool.imap(pdata, lin_x, chunksize=500)
    #
    # return [Data(x, y) for x, y in zip(lin_x, int_y)]

# def approx_polynomial(data: [Data], deg=3):
#     n = len(data)
#     arr = [[0.0 for _ in range(deg)] for _ in range(deg)]
#     r = [0.0 for _ in range(deg)]
#     # d = [0.0 for _ in range(deg)]
#
#     # Konstrukcja M
#     for i in range(deg):
#         for j in range(deg):
#             arr[i][j] = sum([p.x ** (i+j) for p in data])
#
#     # Konstrukcja d
#     d = [sum([(p.x ** i) * p.y for p in data]) for i in range(deg)]
#     # for i in range(deg):
#     #     d[i] = sum([(p.x ** i) * p.y for p in data])
#
#     # Rozwiązanie r
#     pass


def interpolate_splines(data: [Data], interpolation_density=None) -> [Data]:
    """http://facstaff.cbu.edu/wschrein/media/M329%20Notes/M329L67.pdf"""
    if interpolation_density is None:
        interpolation_density = len(data)

    n = len(data)
    # Step 1, len(h) = n - 1
    h = [data[i+1].x - data[i].x for i in range(n - 1)]
    # Step 2, len(alpha) = n - 2
    alpha = [(3/h[i] * (data[i+1].y - data[i].y)) - (3/h[i-1] * (data[i].y - data[i-1].y)) for i in range(1, n - 1)]
    # Step 3, len(l/u/z) = n
    l = [1.0 for _ in range(n)]
    u = [1.0 for _ in range(n)]
    z = [1.0 for _ in range(n)]
    # Step 4
    for i in range(1, n - 1):
        l[i] = 2 * (data[i+1].x - data[i-1].x) - h[i-1] * u[i-1]
        u[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i-1] * z[i-1]) / l[i]
    # Step 5
    l[-1] = 1.0
    z[-1] = 0.0
    c = [0.0 for _ in range(n)]
    # Step 6
    for


def process(dataset: [Data]):
    # plt.plot(
    #     [point.x for point in dataset],
    #     [point.y for point in dataset],
    #     'b.',
    #     label='raw dataset'
    # )
    # plt.show()

    # interpolated_data = interpolate_lagrange(dataset, 300)
    interpolated_data = interpolate_lagrange(dataset, len(dataset) * 10)

    plt.plot(
        [point.x for point in dataset],
        [point.y for point in dataset],
        'b.',
        label='raw dataset'
    )
    plt.plot(
        [point.x for point in interpolated_data],
        [point.y for point in interpolated_data],
        'r.',
        label='interpolated'
    )
    plt.legend()
    plt.ylim(min([p.y for p in dataset]) - 10, max([p.y for p in dataset]) + 10)
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
    single_file('./data/SpacerniakGdansk.txt')
    # single_file('./data/test.txt')


if __name__ == '__main__':
    main()
