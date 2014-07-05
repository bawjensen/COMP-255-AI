def main():
	with open("rawByAuthorFeatureSet.csv", "r") as fin:
		textString = ""

		i = 0
		for line in fin:
			print "LOOPING AGAIN"
			if i == 0:
				i += 1
			else:
				line = line.strip()
				line = line.split(",")
				word = line.pop(0)

				line = [int(x) for x in line]
				count = sum(line)
				textString += str((word + " ")*count)


	with open("fedTextString.txt", "w") as fout:
		fout.write(textString)

if __name__ == "__main__":
	main()