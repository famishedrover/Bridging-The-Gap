from readConcepts import getEverything

from makeData import getData 
import pickle 
import numpy as np 


concepts = getEverything("./concepts_")


x = np.random.random((128,))
x = np.expand_dims(x, axis=0)

for ix in concepts.keys() :
	print (concepts[ix]["model"][0].predict(x))

