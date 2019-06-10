from numpy import linspace

from HPAPROX.dataIO import Data
import HPAPROX.matrix_calc as mcalc


def interpolate_point_lagrange(xi, data: [Data]):
	result: float = 0.0
	length = len(data)
	for i in range(length):
		term: float = data[i].y
		for j in range(length):
			if i != j:
				term *= (xi - data[j].x) / float(data[i].x - data[j].x)
		result += term

	print("Interpolated point", xi, "result", result)
	return result


def interpolate_lagrange(data: [Data], interpolation_density=None) -> [Data]:
	if interpolation_density is None:
		interpolation_density = len(data)

	lin_x = linspace(data[0].x, data[-1].x, interpolation_density)
	print("Max:", lin_x[-1])

	return [Data(lin_x[i], interpolate_point_lagrange(lin_x[i], data)) for i in range(interpolation_density)]

	# pdata = partial(interpolate_point_lagrange, data=data)
	#
	# with Pool(5) as pool:
	#     print(pool)
	#     int_y = pool.imap(pdata, lin_x, chunksize=500)
	#
	# return [Data(x, y) for x, y in zip(lin_x, int_y)]


def find_point(x: float, source: [float]) -> int:
	for i in range(len(source) - 1):
		if x < source[i+1]:
			return i

	return len(source) - 2


def interpolate_splines(data: [Data], interpolation_density=None) -> [Data]:
	if interpolation_density is None:
		interpolation_density = len(data) * 100

	lin_x = linspace(data[0].x, data[-1].x, interpolation_density)
	x = [p.x for p in data]
	y = [p.y for p in data]
	a, b, c, d = spline(x, y)

	ret = []
	for i in range(interpolation_density):
		p = find_point(lin_x[i], x)
		xval = lin_x[i] - x[p]
		value = a[p] + b[p] * xval + c[p] * xval ** 2 + d[p] * xval ** 3
		ret.append(Data(lin_x[i], value))

	return ret


def spline(x: [float], y: [float]) -> ([float], [float], [float], [float]):
	n = len(x)

	tmp_1 = x[1:]
	tmp_2 = x[:-1]
	h = [xl - xe for xl, xe in zip(tmp_1, tmp_2)]
	tmp_1 = y[1:]
	tmp_2 = y[:-1]
	df = [(yl - ye) / hv for yl, ye, hv in zip(tmp_1, tmp_2, h)]
	tmp_1 = df[1:]
	tmp_2 = df[:-1]
	b = [(dl - de) * 6 for dl, de in zip(tmp_1, tmp_2)]

	L = h[:-1]
	U = h[1:]
	D = [(hl + he) * 2 for hl, he in zip(L, U)]

	matrix = [[0.0 for _ in range(n - 2)] for _ in range(n - 2)]
	for i in range(n - 2):
		for j in range(n - 2):
			if i == j:
				matrix[i][j] = D[i]
			elif i == j - 1:
				matrix[i][j] = U[i]
			elif i == j + 1:
				matrix[i][j] = L[i]

	# rozwiązanie matrix * ret = b
	ret, _ = mcalc.gauss_seidel(matrix, b, len(matrix), 10 ** -15)
	if ret is None:
		print("Metoda iteracyjna zawiodła, przerzucam się na metodę Gaussa")
		ret, _ = mcalc.gauss(matrix, b)

	ret.insert(0, 0.0)
	ret.append(0.0)

	a = y[:-1]
	tmp_1 = ret[1:]
	tmp_2 = ret[:-1]
	b = [di - hi * (2 * re + rl) / 6 for di, hi, rl, re in zip(df, h, tmp_1, tmp_2)]
	c = [ri / 2 for ri in ret[:-1]]
	d = [(rl - re) / (6 * hi) for rl, re, hi in zip(tmp_1, tmp_2, h)]

	# len(abcd) = len(x) - 1
	return a, b, c, d
