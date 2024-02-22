import os 
from shutil import copyfile





# Running Ep 00629 / 04000 | Time = 00129 | Total Time = 000083736 | Avg. Time /ep = 132.00
# Condition = isClearDownCrab      | Posctr = 023999 | Negctr = 000215
# Condition = onLadder             | Posctr = 024214 | Negctr = 006789
# Condition = onLadderTop          | Posctr = 010838 | Negctr = 020165
# Condition = onLadderBottom       | Posctr = 012849 | Negctr = 018154
# Condition = inAir                | Posctr = 004315 | Negctr = 026688
# Condition = onLeftPassage        | Posctr = 002235 | Negctr = 028768
# Condition = onRightPassage       | Posctr = 003822 | Negctr = 027181
# Condition = crabOnLeft           | Posctr = 000020 | Negctr = 002593
# Condition = crabOnRight          | Posctr = 000001 | Negctr = 002612
# Condition = isClearUpCrab        | Posctr = 024204 | Negctr = 000010
# Condition = crabOnRelativeRight  | Posctr = 000049 | Negctr = 030954
# Condition = crabOnRelativeLeft   | Posctr = 030806 | Negctr = 000197
# Condition = ladderBottomThreshold | Posctr = 000064 | Negctr = 024150


# call as 
# python -m sampling.mergeConcepts 
# from root.

rootpath = "./cases/myconcepts"
path = rootpath + "/level3_all"
savepath = rootpath+"/merged"
try : 
	os.mkdir(savepath)
except : 
	pass 




posex = 0 
negex = 0 

for run in os.listdir(path) :
	print ("In Folder : ", run)
	for concept in os.listdir(path+"/"+run) :
		
		try : 
			os.mkdir(savepath + "/" + concept)
		except : 
			pass 



		for k in os.listdir(path+"/"+run+"/"+concept) :
			src = path+"/"+run+"/"+concept+"/"+k
			# print (src)

			extn = k.split("_")[2]

			currex  = 0
			if "neg" in k : 
				ty = "neg"
				negex += 1
				currex = negex
			else : 
				ty = "pos"
				posex += 1
				currex = posex

			dst = savepath+"/"+concept+"/"+ ty + "_sample"+str(currex)+"_" + extn
			# print (dst)
			copyfile(src, dst)
	
		