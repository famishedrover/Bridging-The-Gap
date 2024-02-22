from readConcepts import getEverything
from sklearn.tree import DecisionTreeClassifier

from makeData import getData 
import pickle 



concepts = getEverything("./concepts_")





# filename = "./concepts/"+'final_model.sav'
# pickle.dump(finalClf, open(filename, 'wb'))

poscount = 10 
negcount = 20 
split = 0.5

for i in concepts.keys() :
	print ("Concept :", i)
	clf = DecisionTreeClassifier(max_depth=10)


	x,y,x_test, y_test = getData(concepts[i]["pos"], concepts[i]["neg"], poscount =10, negcount =10, split=0.5)
	clf.fit(x, y)
	score = clf.score(x, y)
	testscore = clf.score(x_test, y_test)

	print ("Train : ", score, " Test : ", testscore)
	savepath = concepts[i]["path"]+"/model_"+str(poscount)+"_"+str(negcount)+"_"+str(split).replace(".", "_")+".sav"
	print (savepath)
	pickle.dump(clf, open(savepath, 'wb'))

