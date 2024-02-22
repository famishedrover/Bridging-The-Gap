import numpy as np 
import matplotlib.pyplot as plt 

def getData(posram, negram, poscount, negcount , split=0.4, seed=456):
	"""
	spit : %of pos to include for train & test 
	"""
	np.random.seed(seed)

	pidx = np.random.choice(posram.shape[0], poscount)
	nidx = np.random.choice(negram.shape[0], negcount)

	pos = posram[pidx]
	neg = negram[nidx]


	trainexp = int(split*pos.shape[0])
	train_pos = pos[:trainexp]
	test_pos = pos[trainexp:]


	trainexn = int(split*neg.shape[0])
	train_neg = neg[:trainexn]
	test_neg = neg[trainexn:]

	
	x_train = np.vstack((train_pos,train_neg))
	x_test = np.vstack((test_pos,test_neg))

	y_train = np.zeros((trainexp + trainexn))
	y_train[:trainexp] = 1
	y_test = np.zeros((pos.shape[0]- trainexp + neg.shape[0]-trainexn))
	y_test[:pos.shape[0]-trainexp] = 1


	return x_train, y_train, x_test, y_test 
