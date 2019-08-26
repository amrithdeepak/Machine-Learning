import pandas as pd
from math import exp
from random import random
 
# This function creates a network given the length of 
# the input, output, and hidden layer. It also takes
# in the number of hidden layers.
def create_network(input_len, hidden_len, output_len,num_hidden):
	network = []
	hidden_layer = []
	hidden_layer_2 = []
	output_layer = []
	# adding hidden layers
	if num_hidden>0:
		for i in range(hidden_len):
			hidden_layer.append({'weights':[random() for j in range(input_len + 1)]})
		network.append(hidden_layer)
	if num_hidden == 2:
		for i in range(hidden_len):
			hidden_layer_2.append({'weights':[random() for j in range(input_len + 1)]})
		network.append(hidden_layer_2)
	for i in range(output_len):
		output_layer.append({'weights':[random() for j in range(hidden_len + 1)]})
	network.append(output_layer)
	return network

# Returns the output class
def sigmoid(inputs):
	return 1 / (1 + exp(-inputs))
 
# This calculates the weighted sum of the inputs
# multiplied by the weights.
def activation_fn(inputs, weights):
	weightlen = len(weights)-1
	ws = weights[weightlen]
	for i in range(weightlen):
		ws += weights[i] * inputs[i]
	return ws
 

 
# Does the backpropogation and stores
# error values in the nodes
def backpropogation(network, e_values):
	curr_layer = network[len(network)-1]
	errors = []
	for i in range(len(curr_layer)):
		curr_node = curr_layer[i]
		error = e_values[i] - curr_node['output']
		errors.append(error)
	# getting errors
	for j in range(len(curr_layer)):
		curr_node = curr_layer[j]
		curr_node['error'] = errors[j] * curr_node['output'] * (1.0 - curr_node['output']) 
	for i in range(len(network)-2,-1,-1):
		curr_layer = network[i]
		errors = []
		for j in range(len(curr_layer)):
			error = 0.0
			for curr_node in network[i + 1]:
				error += (curr_node['weights'][j] * curr_node['error'])
			errors.append(error)
		for j in range(len(curr_layer)):
			curr_node = curr_layer[j]
			curr_node['error'] = errors[j] * curr_node['output'] * (1.0 - curr_node['output']) 

 
# This function gets the outputs using
# forward propogation.
def get_outputs(network, data):
	output_data = data
	for layers in network:
		curr_data = []
		for layer in layers:
			layer['output'] = sigmoid(activation_fn(data, layer['weights']))
			curr_data.append(layer['output'])
		data = curr_data
	return data
 

# This function calculates the weights based on the 
# data. 
def calculate_weights(network, data, learning_rate):
	inputs = data[0:len(data)-1]
	for curr_node in network[0]:
		for j in range(len(inputs)):
			curr_node['weights'][j] += inputs[j] * learning_rate * curr_node['error'] 
		curr_node['weights'][len(curr_node['weights'])-1] += curr_node['error'] * learning_rate
	for i in range(1,len(network)):
		inputs = [curr_node['output'] for curr_node in network[i - 1]]
		for curr_node in network[i]:
			for j in range(len(inputs)):
				curr_node['weights'][j] += inputs[j] * learning_rate * curr_node['error']
			curr_node['weights'][len(curr_node['weights'])-1] +=  curr_node['error'] * learning_rate 
 
# This function calls backpropogation and calculate_weights
# and trains the data.
def train_function(network, dataset, learning_rate, n_outputs):
	for iter in range(20):
		sum_error = 0
		for data in dataset:
			predicted = get_outputs(network, data)
			expected = [0]* (n_outputs)
			expected[data[len(data)-1]] = 1
			# error is difference between predicted and actual
			for i in range (len(expected)):
				sum_error += (expected[i]-predicted[i])**2
			backpropogation(network, expected)
			calculate_weights(network, data, learning_rate)

# Calls the get outputs and returns the max class
def predict_class(network, data):
	outputs = get_outputs(network, data)
	maxidx = 0
	max_val = float("-inf")
	for i in range(len(outputs)):
		if outputs[i] > max_val:
			max_val = outputs[i]
			maxidx = i
	return maxidx


# This function given the data creates train and test data and
# then calculates the accuracy.
def start(dataloc):
	data = pd.DataFrame(pd.read_csv( dataloc, header=None))
	datalen = len(data)
	datasize = datalen//5
	average_accuracy = [0.0,0,0,0,0]
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

		dataset = data_train.values.tolist()
		dataset_len = len(dataset[0]) - 1
		unique_output_cnt = len(set([i[len(i)-1] for i in dataset]))
		for hidden_layers in range(3):
			network = create_network(dataset_len, hidden_layers, unique_output_cnt,1)
			train_function(network, dataset, 0.5, unique_output_cnt)
			dataset_test = data_test.values.tolist()
			correct = 0.0
			wrong = 0.0
			# going through each row in testing data
			for row in dataset_test:
				prediction = predict_class(network, row)
				actual = row[len(row)-1]
				if actual == prediction:
					correct +=1
					if i ==0:
						print("The predicted value is ", prediction, " and the actual value is ", actual, " which is correct.",sep="")
				else:
					wrong +=1
					if i ==0:
						print("The predicted value is ", prediction, " and the actual value is ", actual, " which is incorrect.",sep="")
			accuracy = correct/(correct+wrong)
			print("For the ", (i+1), "th iteration of the cross validation with ", hidden_layers, " hidden layers, the accuracy is ", accuracy,sep ="")
			average_accuracy[hidden_layers] += accuracy
	# average for the 5 iterations of cross validation
	for j in range(3):
		average_accuracy[j]/=5
		print("The average accuracy for ", j," hidden layers is ",average_accuracy[j], sep = "")




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

