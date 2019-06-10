import os

import matplotlib.pyplot as plt

from HPAPROX.dataIO import read_all, read, Data
from HPAPROX.interpolation import interpolate_splines, interpolate_lagrange


def process(dataset: [Data], filename):
	# plt.plot(
	# 	[point.x for point in dataset],
	# 	[point.y for point in dataset],
	# 	'b.',
	# 	label='raw dataset'
	# )
	# plt.show()

	nth = 11
	# nth = 22

	method = 'lagrange '
	interpolated_data = interpolate_lagrange(dataset[::nth], len(dataset) * 10)

	# method = 'splines '
	# interpolated_data = interpolate_splines(dataset[::nth])

	plt.figure()
	plt.plot(
		[point.x for point in dataset],
		[point.y for point in dataset],
		'b-',
		label='dane zrodlowe'
	)
	plt.plot(
		[point.x for point in dataset[::nth]],
		[point.y for point in dataset[::nth]],
		'g.',
		label='punkty wybrane do interpolacji'
	)
	plt.plot(
		[point.x for point in interpolated_data],
		[point.y for point in interpolated_data],
		'r-',
		label='wykres interpolowany'
	)
	plt.legend()
	plt.ylim(min([p.y for p in dataset]) - 10, max([p.y for p in dataset]) + 10)
	# plt.yscale("log")
	plt.title(method + filename + str(nth))
	plt.savefig(method + filename + str(nth) + '.png', dpi=600)
	# plt.show()


def all_data():
	data = read_all()
	folder = "./data"
	file_list = os.listdir(folder)
	for dataset, file in zip(data, file_list):
		process(dataset, file)


def single_file(filename='przyk3.txt'):
	data, _ = read('./data/' + filename)
	process(data, filename)


def main():
	all_data()
	# single_file('./data/SpacerniakGdansk.txt')


if __name__ == '__main__':
	main()
