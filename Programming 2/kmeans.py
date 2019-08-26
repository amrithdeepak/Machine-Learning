import pandas as pd
import numpy as np
import statistics 

def k_means(dataset_init,dataset_test_init,k):

	dataset = dataset_init[0]
	cl = dataset_init[1]

	leng = len(dataset)
	cluster = [[None for i in range(leng)] for j in range(k)]
	mu = [None]*k
	dataset_min = min(dataset)
	dataset_max = max(dataset)

	delta = (dataset_max - dataset_min)/k
	# setting initaial mu
	for i in range(k):
		mu[i] = dataset_min + (0.5+i)*delta
	mussame = False
	# looping while the clusters are changing
	while not(mussame):
		# setting clusters 
		min_idx_cnt= [0]*k
		cluster = [[] for i in range(k)]
		actual_val_list = [[] for i in range(k)]
		cnt = 0
		# setting cluster for the iteration
		for j in range (len(dataset)):
			x = dataset[j]
			actual = cl[j]
			dist = [None]*k
			min_dist = float("inf")
			min_idx = -1
			for i in range(k):
				dist[i] = abs(mu[i]-x)
				if dist[i]<min_dist:
					min_dist = dist[i]
					min_idx = i
			cluster[min_idx].append (x)
			actual_val_list[min_idx].append(actual)
		mussame = True
		# setting mu
		for i in range(k):
			if mu[i] != statistics.mean(cluster[i]):
				mussame = False
				mu[i] = statistics.mean(cluster[i])
		

	# calculating silhoutte coefficient
	s_i = []
	for x in dataset:
		sum_a = 0
		cluster_no = -1
		for i in range (k):
			if x in cluster[i]:
				cluster_no=i
		for x2 in cluster[cluster_no]:
			sum_a += abs(x2-x)
		# calculating average distance
		mean_a = sum_a/len(cluster[cluster_no])
		sum_b = 0
		for x2 in dataset:
			sum_b += abs(x2-x)
		sum_b -= sum_a
		# calculating b_i
		mean_b = sum_b/(len(dataset)-len(cluster[cluster_no]))
		# adding each silhoutte coefficient to a list
		s_i.append( (mean_b-mean_a)/(max(mean_a,mean_b)))
	print("The average silhoutte coefficient is ", statistics.mean(s_i))
	mu_mapping=[]
	# finding the cluster each mu value maps to
	for x in actual_val_list:
		if(max(set(x), key=x.count) in mu_mapping):
			counter=0
			stop_no = True
			while (stop_no):
				l=sorted(x,key=x.count,reverse=True)
				if l[counter] not in mu_mapping:
					mu_mapping.append(l[counter])
					stop_no = False
				counter +=1
				if counter == len(l):
					for i in range(1,k+1):
						if i not in mu_mapping:
							mu_mapping.append(i)
							stop_no = False
							break
		else:
			mu_mapping.append(max(set(x), key=x.count))
	for i in range(k):
		print("Cluster mean ", mu[i], "Classified Class ", mu_mapping[i])


	# testing with testing data
	dataset = dataset_test_init[0]
	cl = dataset_test_init[1]

	correct=0
	wrong = 0
	
	# for each element in dataset, classify it using the cluster and cluster mapping
	for j in range (len(dataset)):
		x = dataset[j]
		actual = cl[j]
		dist = [None]*k
		min_dist = float("inf")
		min_idx = -1
		for i in range(k):
			dist[i] = abs(mu[i]-x)
			if dist[i]<min_dist:
				min_dist = dist[i]
				min_idx = i
		classified = mu_mapping[min_idx]
		# check if the classified class equals the actual class
		if classified == actual:
			correct+=1
		else:
			wrong+=1
	print("There are ", correct," correct classifications and ", wrong, " incorrect classifications giving an accuracy of ", correct/(correct+wrong))

	return mu	


def glass_data(dataloc_train,dataloc_test,colnames):
	# getting data frame to supply
	glass = pd.DataFrame(pd.read_csv( dataloc_train, header=None,names=colnames))
	glass_test = pd.DataFrame(pd.read_csv( dataloc_test, header=None,names=colnames))
	predict_var = "10"
	features = "4"
	num_classes = 7
	# calling and printing k_means results
	print("\nGlass Data:\n")
	print ("The cluster means are ",k_means([glass[features],glass[predict_var]],[glass_test[features],glass_test[predict_var]],num_classes))


def iris_data(dataloc_train,dataloc_test,colnames):

	# getting data frame to supply 
	iris = pd.DataFrame(pd.read_csv( dataloc_train, header=None,names=colnames))
	iris_test = pd.DataFrame(pd.read_csv( dataloc_test, header=None,names=colnames))
	predict_var = "4"
	features = "1"

	# converting response variables to numeric values to supply k-means
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

	iris_numeric.columns = colnames
	iris_test_numeric.columns = colnames
	num_classes = 3
	# calling and printing k_means results
	print("\nIris Data:\n")
	print("The cluster means are ", k_means([iris_numeric[features],iris_numeric[predict_var]],[iris_test_numeric[features],iris_test_numeric[predict_var]],num_classes))


def spambase_data(dataloc_train,dataloc_test, colnames):

	# getting data frame to supply
	spambase = pd.DataFrame(pd.read_csv( dataloc_train, header=None,names=colnames))
	spambase_test = pd.DataFrame(pd.read_csv( dataloc_test, header=None,names=colnames))
	spambase = spambase.values.tolist()
	leng = len(spambase)
	width = len(spambase[0])

	features = "0"

	predict_var = "57"
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
	# calling and printing k_means results
	num_classes = 2
	print("\nSpambase Data:\n")
	print("The cluster means are ", k_means([spambase_numeric[features],spambase_numeric[predict_var]],[spambase_test_numeric[features],spambase_test_numeric[predict_var]],num_classes))


dataloc_train ="~/Downloads/glass.csv"
dataloc_test = "~/Downloads/glass_test.csv"
colnames = ["0","1","2","3","4","5","6","7","8","9","10"]
glass_data(dataloc_train,dataloc_test,colnames)


dataloc_train = "~/Downloads/iris.csv"
dataloc_test = "~/Downloads/iris_test.csv"
colnames = ["0","1","2","3","4"]
iris_data(dataloc_train,dataloc_test,colnames)

colnames = [None]*58
for i in range(58):
	colnames[i] = str(i)

dataloc_train = "~/Downloads/spambase.csv"
dataloc_test = "~/Downloads/spambase_test.csv"

spambase_data(dataloc_train,dataloc_test,colnames)

print("\n")
