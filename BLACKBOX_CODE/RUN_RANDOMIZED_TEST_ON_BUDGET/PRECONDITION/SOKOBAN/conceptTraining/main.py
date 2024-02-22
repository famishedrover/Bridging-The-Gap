import pickle 
import numpy as np
import random 


import matplotlib.pyplot as plt

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

__RAM__ = 0 
__RGB__ = 1



# posSamples = 20 
# negSamples = 40


all_samples = pickle.load(open("./concepts/ladder.b", "rb"))

def getNumpy(pos_ram, neg_ram):
	x_p = np.array(pos_ram)
	x_n = np.array(neg_ram)

	# print (x_p.shape, x_n.shape )
	x = np.vstack((x_p, x_n))

	y = np.zeros((x.shape[0]))
	y[:x_p.shape[0]] = 1
	
	return x ,y 



def traintestConcept(posSamples, negSamples, all_samples):

	pos_samples = all_samples[0]
	neg_samples = all_samples[1]
	# single_pos_sample_RAM = pos_samples[0][0]
	# single_pos_sample_RGB = pos_samples[0][1]



	pos_ram = [x[0] for x in pos_samples]
	neg_ram = [x[0] for x in neg_samples]


	pos_ram = random.sample(pos_ram, posSamples)
	pos_ram_test = pos_ram[:int(posSamples/2)]
	pos_ram = pos_ram[int(posSamples/2):]

	# print (len(pos_ram),len(pos_ram_test))



	neg_ram = random.sample(neg_ram, negSamples)
	neg_ram_test = neg_ram[:int(negSamples/2)]
	neg_ram = neg_ram[int(negSamples/2):]

	# print (len(neg_ram),len(neg_ram_test))

	# print (len(pos_ram), len(neg_samples))


	x ,y = getNumpy(pos_ram,neg_ram)
	x_test, y_test = getNumpy(pos_ram_test, neg_ram_test)


	print ('Total Dataset :', x.shape[0] , ' \nNeg Sample    :', negSamples , ' \nPos Sample    :', posSamples )
	print ('Test/Train = 50/50')




	names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
	         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
	         "Naive Bayes", "QDA"]

	classifiers = [
	    KNeighborsClassifier(3),
	    SVC(kernel="linear", C=0.025),
	    SVC(gamma=2, C=1),
	    GaussianProcessClassifier(1.0 * RBF(1.0)),
	    DecisionTreeClassifier(max_depth=5),
	    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
	    MLPClassifier(alpha=1, max_iter=1000),
	    AdaBoostClassifier(),
	    GaussianNB(),
	    QuadraticDiscriminantAnalysis()]



	X_train = x 
	y_train = y


	acc = {}

	for name, clf in zip(names, classifiers):
	    
	    clf.fit(X_train, y_train)
	    score = clf.score(X_train, y_train)
	    scoretest = clf.score(x_test, y_test)
	    acc[name] = (score,scoretest)
	    print (' %s   Train Score : %f Test Score : %f'%( name, score , scoretest) )

	return acc 


# Plot and stuff 

tryposcounts = [5, 10, 20 ,30,40,50, 60, 70, 80, 90 , 100]

allAcc = []

for i in tryposcounts : 
	acc = traintestConcept(i,2*i,all_samples)
	allAcc.append(acc)

