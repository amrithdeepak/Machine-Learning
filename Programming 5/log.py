import numpy as np
import pandas as pd

# this is the sigmoid function which returns the output of running the sigmoid function
def sigmoid(inputs):
    return 1 / (1 + np.exp(-inputs))

# this function calcualtes the gradient
def gradient_fn(data, weights, classes):
	m = data.shape[0]
	return np.dot(data.T, classes-sigmoid(np.dot(data, weights)))

# this function returns the weights after training the 
# data using logistic regression
def logistic_regression_train(data,classes,learning_rate):
	n = data.shape[1]
	weights_same = False
	unique_classes = np.unique(classes)
	weights = []
	# for each class getting weight to predict that class or not that class
	for c in unique_classes:
		class_c = np.where(classes==c,1,0)
		weight = np.zeros(n)
		cnt = 0
		# stopping when weights don't change or after 10000 repetitions
		while not(weights_same or cnt >10000):
			cnt+=1
			gradient = gradient_fn(data,weight,class_c)
			for i in gradient:
				if abs(i) > 0.01:
					weights_same = False
			weight += learning_rate * gradient
		weights.append(weight)
	return weights,unique_classes

# given weights predict class
def predict_class(data, weights, classes):
	predictions = []
	for (rownum,row) in data.iterrows():
		maxidx = -1
		maxval = float("-inf")
		for i in range(len(weights)):
			weight = weights[i]
			currval = sigmoid(np.dot(row, weight))
			if currval>maxval:
				maxval = currval
				maxidx = i
		predictions.append(maxidx)
	return [classes[p] for p in predictions]


# This function given the data creates train and test data and
# then calculates the accuracy.
def start(dataloc):
	data = pd.DataFrame(pd.read_csv( dataloc, header=None))
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
		train_features = data_train.iloc[:, :-1]
		train_classes = data_train.iloc[:,-1]
		weights,unique_classes = logistic_regression_train(train_features, train_classes, 1e-3)

		test_features = data_test.iloc[:, :-1]
		test_labels = data_test.iloc[:,-1]
		test_data_predicted_classes = predict_class(test_features, weights,unique_classes)
		correct = sum(test_labels==test_data_predicted_classes)
		if i ==0:
			print("\nWeights: ")
			for j in range(len(weights)):
				print("For class ",  unique_classes[j], " the weights are\n ", weights[j], sep="")
			print()
			for j in range(len(test_labels)):
				print("Predicted Value: ",test_data_predicted_classes[j], " Actual Value: ", test_labels[j], sep ="" )
			print()
		accuracy = (float(correct))/(float)(len(test_data_predicted_classes))
		print("For the ", (i+1), "th iteration of the cross validation, the accuracy is ", accuracy,sep ="")
		average_accuracy += accuracy
	# average for the 5 iterations of cross validation
	average_accuracy/=5
	print("The average accuracy is ",average_accuracy, sep = "")



# call start function for each dataset
print("\nBreast Cancer:")
dataloc = "~/Downloads/breast-cancer-wisconsin.csv"
start(dataloc)

print("\nGlass:")
dataloc = "~/Downloads/breast-cancer-wisconsin.csv"
start(dataloc)

print("\nIris:")
dataloc = "~/Downloads/iris.csv"
start(dataloc)

print("\nSoybean:")
dataloc = "~/Downloads/soybean-small.csv"
start(dataloc)

print("\nVote:")
dataloc = "~/Downloads/house-votes-84.csv"
start(dataloc)

print()



