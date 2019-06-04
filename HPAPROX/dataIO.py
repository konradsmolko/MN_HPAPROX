import os


class Data:
    def __init__(self, a: float, b: float):
        self.x = a
        self.y = b

    def print(self):
        print('x:', self.x, 'y:', self.y)


def read_all() -> [[Data]]:
    folder = "./data"
    file_list = os.listdir(folder)

    for file in file_list:
        file = "./data/" + file
        yield read(file)


def read(filename: str) -> [Data]:
    with open(filename, 'r') as inputFile:
        lines = inputFile.readlines()
    raw_data: [[str, str]] = [line.strip().split(',') for line in lines]

    # for i in range(len(raw_data)):
    #     for j in range(2):
    #         raw_data[i][j] = float(raw_data[i][j])

    # data = [Data(float(x), float(y)) for x, y in raw_data]
    # return data

    return [Data(float(x), float(y)) for x, y in raw_data]
