import pandas as pd
import numpy as np

def naive_bayes(dataset,dataset_test_init,num_classes,print_data):
	# getting means of columns
	means = dataset.mean(axis=0)
	dataset2 = dataset.values.tolist()
	curr = 0
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
			if print_data:
				print("The predicted class is ",max_class, " and the actual class is ", actual_class, ".", sep="")
			if (max_class == actual_class):
				correct +=1
			else:
				wrong+=1
	return ((float(correct))/(float(correct+wrong)))

# This function given the data creates train and test data and
# then calculates the accuracy.
def start(data):
	datalen = len(data)
	datasize = datalen//5
	average_accuracy = 0.0

	# shuffle data
	data = data.sample(frac=1).reset_index(drop=True)
	for i in range(5):
		# create train and test data
		data_test = data[datasize*i:datasize*(i+1)]
		if i ==0:
			data_train= data[datasize*(i+1):datalen]
		elif i==4:
			data_train = data[0:datasize*i]
		else:
			data_train = data[0:datasize*i].append(data[datasize*(i+1):datalen])
		correct =0

		classes = data_train.iloc[:,-1]
		if i==0:
			accuracy = naive_bayes(data_train, data_test, len(classes.unique()),True)
		else:
			accuracy = naive_bayes(data_train, data_test, len(classes.unique()),False)
		
		print("For the ", (i+1), "th iteration of the cross validation, the accuracy is ", accuracy,sep ="")
		average_accuracy += accuracy
	# average for the 5 iterations of cross validation
	average_accuracy/=5
	print("The average accuracy is ",average_accuracy, sep = "")


def iris_data(dataloc):
	# getting data frame to supply
	colnames = ["0","1","2","3","4"]
	iris = pd.DataFrame(pd.read_csv( dataloc, header=None,names=colnames))
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
	start(pd.DataFrame(iris_numeric))


def breast_cancer_data(dataloc):
	# getting data frame to supply
	colnames = ["0","1","2","3","4","5","6","7","8","9"]
	breast_cancer = pd.DataFrame(pd.read_csv( dataloc, header=None,names=colnames))
	for i in range (len(breast_cancer)):
		for j in range (len(breast_cancer.iloc[i])):
			if j == 9:
				breast_cancer.iloc[i][j] +=1
	start(pd.DataFrame(breast_cancer))


def glass_data(dataloc):
	# getting data frame to supply
	colnames = ["0","1","2","3","4","5","6","7","8","9"]
	glass = pd.DataFrame(pd.read_csv( dataloc, header=None,names=colnames))
	for i in range (len(glass)):
		for j in range (len(glass.iloc[i])):
			if j == 9 and glass.iloc[i][j]>4:
				glass.iloc[i][j] -=1
	start(pd.DataFrame(glass))


def soybean_data(dataloc):
	colnames = [None]*36
	for i in range(36):
		colnames[i] = str(i)
	# getting data frame to supply
	soybean = pd.DataFrame(pd.read_csv( dataloc, header=None,names=colnames))
	start(pd.DataFrame(soybean))


def vote_data(dataloc):
	colnames = [None]*17
	for i in range(17):
		colnames[i] = str(i)
	vote = pd.DataFrame(pd.read_csv( dataloc, header=None,names=colnames))
	# converting response variables to numeric values to supply naive bayes
	vote = vote.values.tolist()
	leng = len(vote)
	width = len(vote[0])
	vote_numeric = [[0 for i in range(width)] for j in range(leng)]
	for i in range (len(vote)):
		for j in range (len(vote[i])):
			if j == 16:
				if vote[i][j] == "Republican":
					vote_numeric[i][j] = 1
				else:
					vote_numeric[i][j] = 2
			else:
				vote_numeric[i][j] = vote[i][j]
	start(pd.DataFrame(vote_numeric))

# call start function for each dataset
print("\nBreast Cancer:")
dataloc = "~/Downloads/breast-cancer-wisconsin.csv"
breast_cancer_data(dataloc)


print("\nGlass:")
dataloc = "~/Downloads/glass.csv"
glass_data(dataloc)


print("\nIris:")
dataloc = "~/Downloads/iris.csv"
iris_data(dataloc)

print("\nSoybean:")
dataloc = "~/Downloads/soybean-small.csv"
soybean_data(dataloc)

print("\nVote:")
dataloc = "~/Downloads/house-votes-84.csv"
vote_data(dataloc)

print()
