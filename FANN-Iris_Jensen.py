import libfann
from random import randrange

FILENAME = "iris"

def grabData():

	outputData = []

	with open(FILENAME + ".csv", "r") as fin:
		if FILENAME == "iris":
			for line in fin:
				line = line.strip()

				line = line.split(",")

				Type = line.pop(0)
				line[0] = line[0].strip()

				if Type == "Iris-setosa":
					line.append(["1", "-1", "-1"])
				elif Type == "Iris-versicolor":
					line.append(["-1", "1", "-1"])
				elif Type == "Iris-virginica":
					line.append(["-1", "-1", "1"])

				outputData.append(line)

	return outputData


def makeANN(training, hidden, error):
	with open(FILENAME + ".data", "w") as fout:
		numInOutPairs = str(len(training))
		numIns = str(len(training[0][:-1]))
		numOuts = str(len(training[0][0]))

		header = " ".join((numInOutPairs, numIns, numOuts))

		fout.write(header + "\n")
		for line in training:
			secLine = line.pop()

			line = " ".join(line)
			secLine = " ".join(secLine)

			fout.write(line + "\n" + secLine + "\n")

#==================================================================================

	connection_rate = 1
	num_input = 4
	num_hidden = hidden
	num_output = 3

	desired_error = error
	max_iterations = 100000
	iterations_between_reports = 1000

	print "\n\nMaking ANN\n\n"
	ann = libfann.neural_net()

	ann.create_sparse_array(connection_rate, (num_input, num_hidden, num_output))
	ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
	ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC_STEPWISE)

	ann.train_on_file(FILENAME + ".data", max_iterations, iterations_between_reports, desired_error)

	ann.save(FILENAME + ".net")


def runANN(L):
	ann = libfann.neural_net()

	ann.create_from_file(FILENAME + ".net")

	return ann.run(L)

def main():
	outputData = grabData()

	testSize = 145
	totalSize = len(outputData)

	training = outputData[:]
	test = []
	# Grab test values out of training
	for i in xrange(testSize):
		test.append(  training.pop( randrange(len(training)) )  )


	makeANN(training, hidden = 4, error = 0.01)


	numFalse = 0
	for featureSet in test:
		inputFeatures = featureSet[:-1]
		expectedOutputFeatures = featureSet[-1]

		for i in xrange(len(inputFeatures)):
			inputFeatures[i] = float(inputFeatures[i])

		actualOutputFeatures = runANN(inputFeatures)

		maxExpected = max(expectedOutputFeatures)
		maxActual = max(actualOutputFeatures)

		expectedIndex = expectedOutputFeatures.index(maxExpected)
		actualIndex = actualOutputFeatures.index(maxActual)
		
		if expectedIndex != actualIndex and actualOutputFeatures.count(maxActual) == 1:
			print "Super whoops."
			print expectedOutputFeatures
			print actualOutputFeatures

			numFalse += 1

	print "Number of elements withheld for test size: %i (out of a total %i elements)." % (testSize, totalSize)
	print "Got", numFalse, "out of", testSize, "wrong."

	with open("fail_outputs" + str(testSize) + ".txt", "a") as fout:
		fout.write(str(numFalse) + "\n")



main()