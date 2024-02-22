from PIL import Image
import numpy as np
import os 

from constt import *

#from matplotlib import pyplot as plt 


def save_img(img, path):
	im = Image.fromarray(img)
	im.save(path)


def readPILImage(path):
	im = Image.open(path)
	return im

def convertImageToNumpy(PIL_Image):
	return np.array(PIL_Image)

def read_img(path):
	im = np.array(Image.open(path))
	return im 


def createDirs(allConceptsFuncs, ROOT="runs"):

	if not os.path.exists(ROOT):
		os.mkdir(ROOT)
		print("Directory " , ROOT ,  " Created ")

	if not os.path.exists(ROOT+"/plots"):
		os.mkdir(ROOT+"/plots")
		print("Directory " , ROOT+"/plots" ,  " Created ")

	if not os.path.exists(ROOT+"/models"):
		os.mkdir(ROOT+"/models")
		print("Directory " , ROOT+"/models" ,  " Created ")


	for concept in allConceptsFuncs: 

		dirsCreate = [ROOT, ROOT+"/"+concept, ROOT+"/"+concept+"/pos", ROOT+"/"+concept+"/neg"]
		for dirName in dirsCreate :
			if not os.path.exists(dirName):
				os.mkdir(dirName)
				print("Directory " , dirName ,  " Created ")


def findAllConcepts():
	import logics 
	allConceptsFuncs = []
	for x in dir(logics) :
		if "concept" in x :
			allConceptsFuncs.append(x)
	print ("All Concepts Found :", allConceptsFuncs)

	return allConceptsFuncs



def saveMasks(pmask, bmask, path, ep):
	savepath = path +"/plots/"+str(ep)+".png"

	#fig, (ax1, ax2) = plt.subplots(1, 2)
	#fig.suptitle('Left Player, Right Box')
	#ax1.matshow(pmask)
	#ax2.matshow(bmask)

	#plt.savefig(savepath)
	#plt.close()
