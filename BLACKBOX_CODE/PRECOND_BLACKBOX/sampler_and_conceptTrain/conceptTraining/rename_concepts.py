import os 
  
# Function to rename multiple files 

i = 0

path = "../cases/myconcepts/die_on_left/"
for filename in os.listdir(path): 
	print (filename)
	name = filename.split(".")
	# pos_sample52068_RGB.b
	# pos_sample52319_image.png
	# pos_sample112370_RAM.b
	newname =  "pos_"+"sample"+name[0].split("sample")[1]+"."+name[1]
	# print (filename, newname)
	# if newname != filename :
	# 	print (filename, newname)
	  
	print (path+filename,path + newname)
	os.rename(path+filename,path + newname) 

	# break
	i += 1