from readConcepts import getEverything
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier


from makeData import getData 
import pickle 
import os

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--level", type=int,
                help="Choose Montezuma Level")
parser.add_argument("-r", "--root", type=str,
                help="Give Concept directory path")
args = parser.parse_args()


rootpath = None 
rootpath = args.root 

if args.level == 4 : 
	rootpath = "../cases/myconcepts/level4"

if args.level == 1 :
	rootpath = "../cases/concepts"



print ("ROOT PATH : ",rootpath)

if rootpath is None : 
	print ("choose correct level with --level argument")
	exit()



# folder = "./Level1/concepts_"
# folder = rootpath+"/concepts_"

print ("Begin Reading...")
concepts = getEverything(rootpath)
print ("End Reading...")
# print (concepts)


if not os.path.exists(rootpath + "/plots") :
	os.mkdir(rootpath + "/plots")

if not os.path.exists(rootpath + "/allModels") :
	os.mkdir(rootpath + "/allModels")



import matplotlib.pyplot as plt




# filename = "./concepts/"+'final_model.sav'
# pickle.dump(finalClf, open(filename, 'wb'))



def runTrain(poscount,negcount,split,final=False):
	poscount = poscount
	negcount = negcount
	split = split
	FINAL = final

	names = []
	scores = []
	testscores = []


	for i in concepts.keys() :
		print ("Concept :", i)

		if i == "concepts" :
			continue

		try :

			# clf = DecisionTreeClassifier(max_depth=10)
			# clf = GaussianNB()
			# clf = SVC()
			clf = AdaBoostClassifier()


			# print("Examples found: Pos", len(concepts[i]["pos"]), len(concepts[i]["neg"]))
			# print (concepts[i])
			x,y,x_test, y_test = getData(concepts[i]["pos"], concepts[i]["neg"], poscount = poscount, negcount =negcount, split=split)
			clf.fit(x, y)
			score = clf.score(x, y)
			testscore = clf.score(x_test, y_test)

			print ("Train : ", score, " Test : ", testscore)
			
			names.append(i)
			scores.append(score)
			testscores.append(testscore)

			if not FINAL :
				savepath = concepts[i]["path"]+"/model_"+str(poscount)+"_"+str(negcount)+"_"+str(split).replace(".", "_")+".sav"
			else : 
				savepath = concepts[i]["path"] + "/final_model.sav"
			print ("SAVED MODEL AT ", savepath)
			pickle.dump(clf, open(savepath, 'wb'))

			modelsavepath = rootpath+"/allModels/"+i+"_"+str(poscount)+"_"+str(negcount)+"_"+str(split).replace(".", "_")+".sav"
			pickle.dump(clf, open(modelsavepath, 'wb'))

			print ("SAVED AT COMMON :", modelsavepath)
		except : 
			print ("FAILED")
			print ("Check number of pos/neg samples for this concept.")






	fig, axs = plt.subplots(1, 1, figsize=(18, 10), sharey=True)
	axs.bar(names, scores, alpha=0.5, label="train")
	axs.bar(names, testscores, alpha=0.5, label="test")

	axs.set_xticklabels( names, rotation=20, fontsize=7)
	plt.legend(loc='upper right')
	plt.title('Plot for Setting, pos={},neg={},split={}'.format(poscount,negcount,split))


	if not FINAL : 
		pathimg = rootpath+"/plots/"+str(poscount)+"_"+str(negcount)+"_"+str(split).replace(".", "_")+".svg"
	else : 
		pathimg = rootpath+"/plots/final.svg"

	plt.savefig(pathimg)
	# fig.savefig('temp.png', dpi=fig.dpi)
	# plt.show()
	



# conditions=[(10,20,0.5),(20,40,0.5),(40,60,0.5),(40,80,0.5),(60,100,0.5),(60,120,0.5),(60,120,0.7),(80,100,0.5),(80,100,0.7),(100,120,0.5),(100,120,0.7),(120,200,0.5),(120,200,0.7),(150,200,0.5),(150,200,0.7),(120,240,0.5),(120,240,0.5),(150,300,0.5),(150,300,0.7),(200,200,0.7),(100,100,0.7)]

# conditions = conditions + [(300,300,0.5), (500,500,0.7), (200,400,0.5), (300,600,0.5)]

# conditions = conditions + [(600,1200,0.5)]

# for x in conditions :
# 	p,n,s = x 
# 	runTrain(poscount=p,negcount=n,split=s,final=False)


runTrain(600,1200,0.5,True)	


