
import os 
import numpy as np
import pickle 


def getPaths(origin):
	concepts = {}

	for i,j,k in os.walk(origin) :
		if len(k) == 0 :
			continue 

		conceptname = i.split("/")[-1]
		# print ("Concept :", conceptname)
		# print ("RAM     :")
		negrams = []
		posrams = []
		modelpath = []
		for ik in k :
			if "RGB" in ik :
				continue

			if ".b" in ik  and "neg" in ik:
				negrams.append('/'.join((i,ik))) 
			if ".b" in ik  and "pos" in ik:
				posrams.append('/'.join((i,ik))) 
			if ".sav" in ik :
				getp = '/'.join((i,ik))
				modelpath.append (getp)

		# for r in rams : 
			# print (r)
		# print ("Model :", modelpath)

		concepts[conceptname] = {}
		concepts[conceptname]["path"] = i
		concepts[conceptname]["negrams"] = negrams
		concepts[conceptname]["posrams"] = posrams
		concepts[conceptname]["model"] = modelpath

	return concepts 


# print  (getPaths("./concepts_")["on_rope"]["path"])


def getEverything(origin = "./concepts_"):

	conceptpaths = getPaths(origin)
	concepts = {}

	
	for i in conceptpaths.keys() :
		print ("\n Reading Concept : ", i)
# 
		posctr = 0
		negctr = 0 

		neg = []
		pos = []

		t = None
		print("Negative ", len(conceptpaths[i]["negrams"]))

		if negctr < 1300 : 
			for rampaths in conceptpaths[i]["negrams"] :
				

				if negctr < 1300 : 
					negctr += 1	
					x = pickle.load(open(rampaths, "rb"))

					if t is None : 
						t = x 
					else :
						t = np.vstack((t,x))

				neg = t 	

		t = None		
		print("Positive ", len(conceptpaths[i]["posrams"]))

		if posctr < 1300 : 
			for rampaths in conceptpaths[i]["posrams"] :
				

				if posctr < 1300 : 
					posctr +=1 
					x = pickle.load(open(rampaths, "rb"))
					if t is None : 
						t = x 
					else :
						t = np.vstack((t,x))

			pos = t

		clf = []

		for modelpaths in conceptpaths[i]["model"]  :
			clfx = pickle.load(open(modelpaths, 'rb'))
			clf.append(clfx)
		

		concepts[i] = {}
		concepts[i]["path"] = conceptpaths[i]["path"]
		concepts[i]["neg"] = neg
		concepts[i]["pos"] = pos 
		concepts[i]["model"] = clf 

	return concepts 



# print (getEverything())