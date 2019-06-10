import matplotlib.pyplot as plt

from HPAPROX.dataIO import read_all, read, Data
from HPAPROX.interpolation import interpolate_splines, interpolate_lagrange


def process(dataset: [Data]):
	# plt.plot(
	# 	[point.x for point in dataset],
	# 	[point.y for point in dataset],
	# 	'b.',
	# 	label='raw dataset'
	# )
	# plt.show()

	# interpolated_data = interpolate_lagrange(dataset)
	# interpolated_data = interpolate_lagrange(dataset, len(dataset) * 10)
	interpolated_data = interpolate_splines(dataset[::10])

	plt.plot(
		[point.x for point in dataset],
		[point.y for point in dataset],
		'b-',
		label='raw dataset'
	)
	plt.plot(
		[point.x for point in interpolated_data],
		[point.y for point in interpolated_data],
		'r-',
		label='interpolated'
	)
	plt.legend()
	plt.show()


def all_data():
	data: [[Data]] = read_all()
	for dataset in data:
		process(dataset)


def single_file(filename='./data/100.txt'):
	data: [Data] = read(filename)
	process(data)


def main():
	all_data()
	# single_file('./data/SpacerniakGdansk.txt')


if __name__ == '__main__':
	main()
