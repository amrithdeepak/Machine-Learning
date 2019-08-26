import pandas as pd
import numpy as np

def naive_bayes(dataset,dataset_test_init,num_classes):
	# getting means of columns
	means = dataset.mean(axis=0)
	dataset2 = dataset.values.tolist()
	curr = 0
	#num_classes = 7
	counts = [0] * num_classes
	leng = len(dataset2[0])-1
	conditionals = []
	countzeros = []
	conditionals = [[0.0 for i in range(leng)] for j in range(num_classes)]

	for i in range(len(conditionals)):
		for j in range(len(conditionals[0])):
			conditionals[i][j] = 0.0
	# going through each row of data
	for sentence in dataset2:
		datasetdata = a = [None] * len(sentence)
		cnt=0
		for i in range(len(sentence)-1,-1,-1):
			cnt+=1
			# for the response variable, getting total count for each value
			if (i==len(sentence)-1):
				curr = int(sentence[i])
				counts[curr-1] +=1
				datasetdata[i] = curr
			# getting the counts for the contitional probabilities
			elif (float(sentence[i])>means[i]): 
				datasetdata[i]= 1;
				conditionals[curr-1][i] = (conditionals[curr-1][i])+1.0;
			else:
				datasetdata[i]= 0;
	# getting the conditional probailities by dividing by the number of 
	# values for the class
	for i in range (len(conditionals[0])):
		for j in range (num_classes):
			if counts[j]==0:
				countzeros.append(j)
				conditionals[j][i] = 0.0
			else:
				conditionals[j][i] = conditionals[j][i]/(float(counts[j]))
	# classifying test data
	dataset_test = dataset_test_init.values.tolist()
	wrong = 0
	correct = 0
	for sentence2 in dataset_test:
		#filling in values for the array of values and
		# the conditional counts
		datasetdata = [0] * len(sentence2);
		for i in range(len(sentence2)):
			if (i == len(sentence2) -1):
				curr = int(sentence2[i])
				counts[curr-1] += 1
				datasetdata[i] = curr
			else:
				if (float(sentence2[i])>means[i]):
					datasetdata[i]= 1
				else:
					datasetdata[i]= 0
		probs = [1.0] * num_classes
		# Calculating Conditional Probability of classes
		for i in range (len(datasetdata)-1):
			for j in range(num_classes):
				probs[j] *= (1-conditionals[j][i])
				if counts[j]==0:
					probs[j]=0
			max_class = np.argmax(probs) + 1
			actual_class = int (datasetdata[len(datasetdata)-1])
			if (max_class == actual_class):
				correct +=1
			else:
				wrong+=1
	return ((float(correct))/(float(correct+wrong)))


def SFS(F_init,dataset,dataset_test_init,predict_var,num_classes):
	F0 = []
	basePerf = float("-inf")
	F = F_init

	currPerf = float("-inf")

	while len(F)>0:
		bestPerf = float("-inf")
		# checking for best feature to add
		for f in F:
			F0.append(f)
			D_train = dataset[F0].join(dataset[predict_var])
			D_valid = dataset_test_init[F0].join(dataset_test_init[predict_var])
			currPerf = naive_bayes(D_train,D_valid,num_classes)
			if currPerf > bestPerf:
				bestPerf = currPerf
				bestF = f

			F0 = F0[:-1]
		# if adding feature improves performance
		if bestPerf > basePerf:
			basePerf = bestPerf

			F.remove(bestF)
			F0.append(bestF)
		# adding more features doesnt improve model
		else:
			break;
	return [F0,basePerf]

def glass_data(dataloc_train,dataloc_test):
	# getting data frame to supply
	colnames = ["0","1","2","3","4","5","6","7","8","9","10"]
	glass = pd.DataFrame(pd.read_csv( dataloc_train, header=None,names=colnames))
	glass_test = pd.DataFrame(pd.read_csv( dataloc_test, header=None,names=colnames))

	# all features
	predict_var = "10"
	F_init = ["1","2","3","4","5","6","7","8","9"]
	result = SFS(F_init,glass,glass_test,predict_var,7)
	print("\nThe features chosen are ", result[0], " for SFS on the glass data.")
	print("The best performance is ", result[1],".")

	# excluding feature 4 to show new result
	F_init = ["1","2","3","5","6","7","8","9"]
	result=SFS(F_init,glass,glass_test,predict_var,7)
	print("\nThe features chosen are ", result[0], " for SFS on the glass data with one feature (#4) removed.")
	print("The best performance is ", result[1],".")


def iris_data(dataloc_train,dataloc_test):
	# getting data frame to supply
	colnames = ["0","1","2","3","4"]
	iris = pd.DataFrame(pd.read_csv( dataloc_train, header=None,names=colnames))
	iris_test = pd.DataFrame(pd.read_csv( dataloc_test, header=None,names=colnames))
	predict_var = "4"

	# converting response variables to numeric values to supply naive bayes
	iris = iris.values.tolist()
	leng = len(iris)
	width = len(iris[0])
	iris_numeric = [[0 for i in range(width)] for j in range(leng)]
	for i in range (len(iris)):
		for j in range (len(iris[i])):
			if j == 4:
				if iris[i][j] == "Iris-setosa":
					iris_numeric[i][j] = 1
				elif (iris[i][j] == "Iris-versicolor"): 
					iris_numeric[i][j] = 2
				else:
					iris_numeric[i][j] = 3
			else:
				iris_numeric[i][j] = iris[i][j]

	iris_test = iris_test.values.tolist()
	leng = len(iris_test)
	width = len(iris_test[0])
	iris_test_numeric = [[0 for i in range(width)] for j in range(leng)]
	for i in range (len(iris_test)):
		for j in range (len(iris_test[i])):
			if j == 4:
				if iris_test[i][j] == "Iris-setosa":
					iris_test_numeric[i][j] = 1
				elif (iris_test[i][j] == "Iris-versicolor"): 
					iris_test_numeric[i][j] = 2
				else:
					iris_test_numeric[i][j] = 3
			else:
				iris_test_numeric[i][j] = iris[i][j]

	iris_numeric = pd.DataFrame(iris_numeric)
	iris_test_numeric = pd.DataFrame(iris_test_numeric)
	# running SFS algorithm
	F_init = ["0","1","2","3"]
	iris_numeric.columns = colnames
	iris_test_numeric.columns = colnames
	result = SFS(F_init,iris_numeric,iris_test_numeric,predict_var,3)
	print("\nThe features chosen are ",result[0], " for SFS on the iris data.")
	print("The best performance is ", result[1],".")


def spambase_data(dataloc_train,dataloc_test):
	colnames = [None]*58
	for i in range(58):
		colnames[i] = str(i)

	# getting data frame to supply
	spambase = pd.DataFrame(pd.read_csv( dataloc_train, header=None,names=colnames))
	spambase_test = pd.DataFrame(pd.read_csv( dataloc_test, header=None,names=colnames))
	spambase = spambase.values.tolist()
	leng = len(spambase)
	width = len(spambase[0])
	# making the predicted variable values 1 and 2 instead of 0 and 1
	spambase_numeric = [[0 for i in range(width)] for j in range(leng)]
	for i in range (len(spambase)):
		for j in range (len(spambase[i])):
			if j == (len(spambase[i])-1):
				spambase_numeric[i][j] = int(spambase[i][j])+1
			else:
				spambase_numeric[i][j] = spambase[i][j]

	spambase_test = spambase_test.values.tolist()
	leng = len(spambase_test)
	width = len(spambase_test[0])
	spambase_test_numeric = [[0 for i in range(width)] for j in range(leng)]
	for i in range (len(spambase_test)):
		for j in range (len(spambase_test[i])):	
			if j == (len(spambase_test[i])-1):
				spambase_test_numeric[i][j] = int(spambase_test[i][j])+1
			else:
				spambase_test_numeric[i][j] = spambase_test[i][j]

	spambase_numeric = pd.DataFrame(spambase_numeric)
	spambase_test_numeric = pd.DataFrame(spambase_test_numeric)


	spambase_numeric.columns = colnames
	spambase_test_numeric.columns = colnames
	F_init = colnames[0:57]	

	# print results
	predict_var = "57"
	result = SFS(F_init,spambase_numeric,spambase_test_numeric,predict_var,2)
	print("\nThe features chosen are ",result[0], " for SFS on the spambase data.")
	print("The best performance is ", result[1],".")


glass_data("~/Downloads/glass.csv","~/Downloads/glass_test.csv")
iris_data("~/Downloads/iris.csv","~/Downloads/iris_test.csv")
spambase_data("~/Downloads/spambase.csv","~/Downloads/spambase_test.csv")
print("\n")
