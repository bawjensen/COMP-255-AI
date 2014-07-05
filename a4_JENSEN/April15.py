def main():
	with open("preprocessedFeatureSet.csv", "r") as fin:
		
		i = 0
		for line in fin:
			line = line.strip()

			if i == 0:
				lineList = line.split(",")
				for i in xrange(len(lineList)):
					if i != 0:
						locationOfDot = lineList[i].find(".")
						lineList[i] = lineList[i][locationOfDot-1:locationOfDot]

				i += 1

			else:
				line = line.split(",")
				j = 0
				for value in line:
					lineList[j] += ("," + value)
					j += 1


	buffStr = "\n".join(lineList)

	print buffStr

	with open("ppCARTFeatureSet.csv", "w") as fout:
		fout.write(buffStr)
main()