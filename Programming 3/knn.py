import pandas as pd
import numpy as np
import statistics 

# calling function for ecoli
def ecoli(dataloc):
	print("\nEcoli Data: ")
	data = pd.DataFrame(pd.read_csv( dataloc, header=None))
	find_best_k(data,10)

# calling function for segmentation
def segmentation(dataloc):
	print("\nSegmentation Data: ")
	data = pd.DataFrame(pd.read_csv( dataloc, skiprows=1, header=None))
	data = data.drop([0], axis = 1)
	data.columns = (range(len(data.iloc[0])))
	find_best_k(data,10)

# calling function for machine
def machine(dataloc):
	print("\nMachine Data: ")
	data = pd.DataFrame(pd.read_csv( dataloc, skiprows=1, header=None))
	data = data.drop([0,1,9], axis = 1)
	data.columns = (range(len(data.iloc[0])))
	find_best_k_regression(data,10)

# calling function for forest fire
def forest_fire(dataloc):
	print("\nForest Fire Data: ")
	data = pd.DataFrame(pd.read_csv( dataloc, skiprows=1, header=None))
	find_best_k_regression(data,10)

# This function finds the best k value for classification knn
def find_best_k(data,number_k):
	datalen = len(data)
	datasize = datalen//5
	best_avg = 0.0
	best_k = 0
	# examining all k values
	for k in range (1,number_k):	
		average = 0.0
		# 5 fold cross validation
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
			for j in range(len(data_test)):
				# call knn function which will return boolean value on whether
				# the classification was correct
				correct += knn(data_train,data_test.iloc[j],k)
			print("For the ", (i+1), "th iteration of the cross validation for k = ", k, ", the accuracy is ", correct/len(data_test),sep ="")
			average += correct/len(data_test)
		# average for the 5 iterations of cross validation
		average/=5
		# choose best value of k
		if average > best_avg:
			best_avg = average
			best_k = k
		print("The average accuracy for k = ", k, " is ",average, sep = "")
		print()
	print("The best k value is ", best_k, " with accuracy ", best_avg, sep ="")
	print()


# This function finds the best k value for regression knn
def find_best_k_regression(data,number_k):
	datalen = len(data)
	datasize = datalen//5
	best_avg = float('inf')
	best_k = 0
	# examining all k values
	for k in range (1,number_k):	
		average = 0.0
		# 5 fold cross validation
		for i in range(5):
			# create train and test data
			data_test = data[datasize*i:datasize*(i+1)]
			if i ==0:
				data_train= data[datasize*(i+1):datalen]
			elif i==4:
				data_train = data[0:datasize*i]
			else:
				data_train = data[0:datasize*i].append(data[datasize*(i+1):datalen])
			error_sq =0
			for j in range(len(data_test)):
				# call knn function which will return error
				error_sq += (knn_regression(data_train,data_test.iloc[j],k))**2
			# mean square error for the 5 iterations
			mse = error_sq/len(data_test)
			print("For the ", (i+1), "th iteration of the cross validation for k= ", k, ", the mean square error is ", mse,sep ="")
			average += mse
		# average for the 5 iterations of cross validation
		average/=5
		# choose best value of k
		if average < best_avg:
			best_avg = average
			best_k = k
		print("The average mean square error for k = ", k, " is ",average, sep = "")
		print()
	print("The best k value is ", best_k, " with average mean square error ", best_avg, sep ="")
	print()

# calculates the euclidean distance between 2 points
def euclidean_distance(pt1,pt2):
	size = len(pt1)
	dist = 0
	for i in range(size):
		if not(type(pt1.iloc[i]) is str):
			dist += (pt1.iloc[i]-pt2.iloc[i])**2
	return dist **(0.5)

# classifies the test point based on the most frequent of the k nearest neighbors
# of the training data and returns whether it was accurate or not.
def knn(dataset_train, test_point, k):
	numcols = (len(dataset_train.iloc[0]))
	dist = {}
	class_count = {}
	# calculating euclidean distance
	for i in range(len(dataset_train)):
		dist[i] = euclidean_distance(dataset_train.iloc[i],test_point)
	# sorting distance
	sorted_dist = sorted(dist.items(), key=lambda kv: kv[1])
	k_near = []
	for i in range(k):
		# getting the k closest based on the sort
		k_near.append(sorted_dist[i][0])
	# iterating through k nearest neighbors and getting class
	for i in range(k):
		class_val = dataset_train.iloc[k_near[i]][numcols-1]
		# getting counts of each class
		if class_val in class_count:
			class_count[class_val] +=1
		# class not shown up yet
		else:
			class_count[class_val] = 1

	sorted_class = sorted(class_count.items(), key=lambda kv: kv[1])[0][0]
	# returns if the class predicted and actual class are the same
	return (sorted_class == test_point[numcols-1])

# classifies the test point based on the most frequent of the k nearest neighbors
# of the training data and returns the error(predicted-actual)
def knn_regression(dataset_train, test_point, k):
	numcols = (len(test_point))
	dist = {}
	class_count = {}
	# calculating euclidean distance
	for i in range(len(dataset_train)):
		dist[i] = euclidean_distance(dataset_train.iloc[i],test_point)
	# sorting distance
	sorted_dist = sorted(dist.items(), key=lambda kv: kv[1])
	k_near_sum = 0
	for i in range(k):
		k_near_sum += (sorted_dist[i][0])
	# average value of k nearest neighbors
	regression_val = k_near_sum/k
	# difference between predicted and actual
	return (regression_val - test_point[numcols-1])

ecoli("~/Downloads/ecoli.csv")

segmentation("~/Downloads/segmentation.csv")

machine("~/Downloads/machine.csv")

forest_fire("~/Downloads/forestfires.csv")
