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
        print("Reading file:", file)
        yield read(file)


def read(filename: str) -> [Data]:
    with open(filename, 'r') as inputFile:
        lines = inputFile.readlines()
    raw_data: [[str, str]] = [line.strip().split(',') for line in lines]
    return [Data(float(x), float(y)) for x, y in raw_data]
