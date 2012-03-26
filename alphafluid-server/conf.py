


def read(file, value):
	f = open(file, "r")

	for line in f.readlines():
		if line.startswith(value):
			res = line.split("=")
			return res.strip()
