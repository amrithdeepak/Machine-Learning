
import pandas as pd
import numpy as np
import math
from collections import defaultdict

# Node has labels which is the variable we are looking at
# children which are the values, next_node which is a dictionary
# mapping each child to its subtrees, and predicted_class used for 
# pruning
class Node(object):
	def __init__(self, label, children, next_node, predicted_class):
		self.label = label
		self.children = children
		self.next_node = next_node
		self.predicted_class = predicted_class

# Decision tree contains the node as its root
class DecisionTree(object):
	def __init__(self):
		self.root=None

# This function calculates the informationGain given the data predictor variable	
def informationGain(data):
	counts = {}
	total_count = len(data)
	ig = 0.0
	for i in data:
		if i in counts:
			counts[i] +=1
		else:
			counts[i] = 1
	for i in counts:
		fraction_i = counts[i]/total_count
		ig += -fraction_i*math.log(fraction_i,2)
	return ig

# This function calculates the list of entropies given a dataset for each of the 
# variables.
def getEntropy(data):
	total_count = len(data)
	ent = []
	for by_col in data.columns[0:len(data.columns)-1]:
		entropy = 0.0
		counts = {}
		# get counts
		for i in data[by_col]:
			if i in counts:
				counts[i] +=1
			else:
				counts[i] = 1
		for i in counts:
			fraction_i = counts[i]/total_count
			# formula for entropy using information gain
			entropy += fraction_i * informationGain((data[data[by_col]==i]).iloc[:,-1])
		ent.append(entropy)
	return ent

# This function prints the decision tree. While this isn't necessary,
# it is incredibly useful for debugging.
def print_dt(root, seen = None):
    if seen == None:
      seen = set()
    seen.add(root)
    if not(root.next_node):
    	print('leaf', root.label)
    	return
    print (root.label,"with children", root.children)
    for i in root.next_node.keys():
    	print(i, "->", root.next_node[i].label)
    for i in root.next_node.keys():
    	if root.next_node[i] in seen:
    		print("DUPLICATED NODE", root.next_node[i].label, root.label)
    	else:
    		print_dt(root.next_node[i])
		
# This function prunes the data by calling do_prune and also calls the evaluation function 
def pruning(root, testing_data):
	correct = 0.0
	cnt =0
	pruning = defaultdict(lambda:0)
	for i, row in testing_data.iterrows():
		cnt +=1
		correct += evaluate_helper(root,row,pruning)
	do_prune(root,pruning)

# The function that does the actual pruning work
def do_prune(root, pruning_counts):
	if not root.next_node: #if it's a leaf
		return
	# recursively prune each child
	for i in root.children:
		do_prune(root.next_node[i],pruning_counts)
	# if pruning improves accuracy
	if root.next_node is not None and pruning_counts[root] > 0 and pruning_counts[root] >= sum([pruning_counts[root.next_node[i]] for i in root.children]):
		root.children = None
		root.next_node = None
		root.label = root.predicted_class
	elif root.children:
		pruning_counts[root] = sum([pruning_counts[root.next_node[i]] for i in root.children])

# Calls evaluate_helper and returns the accuracy
def evaluate(root, testing_data):
	correct = 0.0
	cnt =0
	for i, row in testing_data.iterrows():
		cnt +=1
		correct += evaluate_helper(root,row)
	return correct/(len(testing_data))

# Does the evaluation work
def evaluate_helper(root,row,pruning=None):
	real_ans = row[len(row)-1]
	if pruning is not None and root.predicted_class == real_ans:
		pruning[root]+=1
	# if we are at a leaf
	if not(root.next_node):
		# correct
		if root.label == real_ans:
			return 1
		# incorrect
		else:
			return 0
	curr_label = root.label
	branch = row[curr_label]
	# recursively follow next_node based on value of testing data
	if branch not in root.next_node:
		return evaluate_helper(root.next_node[root.children[0]], row)
	return evaluate_helper(root.next_node[branch],row,pruning)

# This function creates training and testing data using 5 fold cross validation
# and calculates the accuracies for both pruned and unpruned.
def start(dataloc):
	data = pd.DataFrame(pd.read_csv( dataloc))
	datalen = len(data)
	datasize = datalen//5
	average_pruned = 0.0
	average_noprune = 0.0
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
		# call test function which will do the 
		# the classification was correct
		accuracy_pruned = test(data_train, data_test, True)
		accuracy_noprune = test(data_train, data_test, False)
		print("For the ", (i+1), "th iteration of the cross validation, the pruned accuracy is ", accuracy_pruned,sep ="")
		print("For the ", (i+1), "th iteration of the cross validation, the non-pruned accuracy is ", accuracy_noprune,sep ="")
		average_pruned += accuracy_pruned
		average_noprune += accuracy_noprune
	# average for the 5 iterations of cross validation
	average_pruned/=5
	average_noprune/=5
	print("The average pruned accuracy is ",average_pruned, sep = "")
	print("The average non-pruned accuracy is ",average_noprune, sep = "")

# This funvtion calls the recursive function to create the decision tree
# and then calls evaluate.
def test(data_train, data_test, do_pruning):
	highest_var,data_values_highest = do_work(data_train)
	data4  = [i for i in data_train.iloc[:,-1] if i] 
	most_dominant_class = max(set(data4) , key=(data4).count)
	prev_node = Node(highest_var,data_values_highest, {},most_dominant_class)
	# initialize decision tree
	dt = DecisionTree()
	dt.root = prev_node
	# call recursive function for each child
	for value in data_values_highest:
		recursion(data_train, prev_node,data_values_highest,highest_var)
	# non pruned
	if not(do_pruning):
		return evaluate(dt.root, data_test)
	# pruned
	pruning(dt.root,data_test)
	return evaluate(dt.root, data_test)

# This function calls information gain, entropy and calculates gains to 
# get the most important feature and the values it takes
def do_work(data):
	colmeans = data.mean(axis=0)
	ig = informationGain(data[data.columns[len(data.columns)-1]])
	ent = getEntropy(data)
	gains= [ig - x for x in ent]
	maxidx = gains.index(max(gains))
	highest_var = data.columns[maxidx]
	data_values_highest = list(set(data[highest_var]))
	return highest_var,data_values_highest

# This recursive function examines each node and recursively calculates
# next_node
def recursion(data, prev_node, data_values_highest, highest_var):
	# only 1 value left, base case
	if len(data_values_highest) == 1:
		data4  = [i for i in data.iloc[:,-1] if i] 
		most_dominant_class = max(set(data4) , key=(data4).count)
		a = Node(most_dominant_class,None, None,most_dominant_class)
		return a
	# only 1 column left or no data, base case
	if data.shape[1]==1 or len(data)==0:
		data4  = [i for i in data.iloc[:,-1] if i] 
		most_dominant_class = max(set(data4) , key=(data4).count)
		a = Node(most_dominant_class,None, None,most_dominant_class)
		return a
	else:
		for value in data_values_highest:
			data2 = data.drop(highest_var, axis=1)
			data3 = data2[data[highest_var]==value]
			# no data, base case
			if(len(data3)==0):
				data4  = [i for i in data.iloc[:,-1] if i] 
				most_dominant_class = max(set(data4) , key=(data4).count)
				a = Node(most_dominant_class,None, None,most_dominant_class)
				return a
			# only 1 value of variable, base case
			if len(data_values_highest) == 1:
				data4  = [i for i in data3.iloc[:,-1] if i] 
				most_dominant_class = max(set(data4) , key=(data4).count)
				a = Node(most_dominant_class,None, None,most_dominant_class)
				return a
			# only 1 column left or no data, base case
			if data3.shape[1]==1 or len(data)==0:
				data4  = [i for i in data3.iloc[:,-1] if i] 
				most_dominant_class = max(set(data4) , key=(data4).count)
				a = Node(most_dominant_class, None,None,most_dominant_class)
				return a
			# recursive step, calculates next node's label, children, and creates the dictionary
			# for next node
			highest_var_2,data_values_highest_2 = do_work(data3)
			data4  = [i for i in data3.iloc[:,-1] if i] 
			most_dominant_class = max(set(data4) , key=(data4).count)
			next_node = Node(highest_var_2,data_values_highest_2,{},most_dominant_class)
			assert(prev_node.label != highest_var_2)
			# recursively calculate next node
			prev_node.next_node[value] = recursion(data3,next_node,data_values_highest_2,highest_var_2) 
		return prev_node
# call start function for each dataset
print("\nAbalone: ")
dataloc = "~/Downloads/abalone.csv"
start(dataloc)
print("\nSegmentation:")
dataloc = "~/Downloads/segmentation.csv"
start(dataloc)
print("\nCar:")
dataloc = "~/Downloads/car.csv"
start(dataloc)
