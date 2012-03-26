


def read(file, value):
	f = open(file, "r")

	for line in f.readlines():
		if line.startswith(value):
			res = line.split("=")[-1]
			return res.strip()
