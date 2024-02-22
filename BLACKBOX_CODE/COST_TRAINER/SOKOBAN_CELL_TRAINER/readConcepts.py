import os 
import utils

import random


from constt import *

random.seed(SEED)


def getPaths(path):
	paths = []
	for i,j,k in os.walk(path):
		for im in k : 
			paths.append("/".join([path,im]))

			# if "15796" in paths[-1] :
			# 	print (paths[-1])
	return paths


import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import numpy as np
# from skimage import io, transform


from scipy.misc import imresize
# prepro = lambda img: imresize(img[:].mean(2), (80,80)).astype(np.float32).reshape(1,80,80)/255.
prepro = lambda img: imresize(img, (80,80,3)).astype(np.float32).reshape(3,80,80)




class ConceptData(Dataset):

	def __init__(self, ROOT, CONCEPT_NAME, transform=None, pos_limit=100, neg_limit=100, seed=1, selectPossible=False):
		# selectPossible is to select min(available, limit) number of examples for both pos and negative...

		random.seed(seed)
		
		pospath = ROOT+"/"+CONCEPT_NAME+"/pos"
		negpath = ROOT+"/"+CONCEPT_NAME+"/neg"

		self.pospaths_full = getPaths(pospath)
		self.negpaths_full = getPaths(negpath)

		if selectPossible : 
			#neg_limit = min(neg_limit, len(self.negpaths_full))
			neg_limit = len(self.negpaths_full)

			print (neg_limit)
			self.negpaths = random.sample(self.negpaths_full, neg_limit)

			#pos_limit = min(pos_limit, len(self.pospaths_full))
			pos_limit = len(self.pospaths_full)
			print (pos_limit)
			self.pospaths = random.sample(self.pospaths_full, pos_limit)

		else :
			self.negpaths = random.sample(self.negpaths_full, neg_limit)
			self.pospaths = random.sample(self.pospaths_full, pos_limit)			


		print ("CONCEPT SAMPLE COUNT", CONCEPT_NAME, pos_limit, neg_limit)
		self.labels = np.hstack((   np.ones(len(self.pospaths)),  np.zeros(len(self.negpaths))  ))
		
		self.allpaths = self.pospaths + self.negpaths

		


		self.transform = transform

	def __len__(self):
		return len(self.allpaths)

	def __getitem__(self, idx):
		if torch.is_tensor(idx):
			idx = idx.tolist()

		img_name = self.allpaths[idx]
		image = utils.read_img(img_name)

		# image = utils.readPILImage(img_name)

		if self.transform:
			image = self.transform(image)

		# print (image.shape)
		# image = prepro(image)
		# print (image.shape)
		label = self.labels[idx]

		return  (image, label)




# data = ConceptData("box_above", None)


# for ix in data :
	# print (ix[1])
