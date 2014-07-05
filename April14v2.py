def main():
	MIN_FREQ = .0005

	with open("rawFeatureSet.csv", "r") as fin:
		buffStr = ""
		wordCountList = []
		lineList = []
		totalCount = 0

		i = 0
		for line in fin:
			if i == 0:
				buffStr += line
				i += 1

			else:
				line = line.strip()
				lineList.append(line)

				line = line.split(",")
				word = line.pop(0)
				line = [int(x) for x in line]
				count = sum(line)

				wordCountList.append([count, word])

				totalCount += count

		i = 0
		for count, word in wordCountList:
			freq = float(count) / totalCount
			if freq > MIN_FREQ:
				buffStr += (lineList[i] + "\n")

			i += 1

		with open("preprocessedFeatureSet.csv", "w") as fout:
			fout.write(buffStr)



if __name__ == "__main__":
	main()