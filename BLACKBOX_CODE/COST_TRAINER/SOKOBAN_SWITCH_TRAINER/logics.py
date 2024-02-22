import numpy as np

import os

# you can define a new concept function -- just remember to name is as concept_*



# we could have created a class - that would have been slightly faster/ better way -- will go with this style for now

# x increases to right 
# y increases to down 


# special cases to handle is when agent / box is over target or switch -- so the thing on the top has the value...
# since switch etc is static we can store them in the init state as well ... and later use those ! 

# 1 is empty space 
# 0 is wall 
# 5 is player 
# 8 switch on 
# 7 switch off 
# 2 target 
# 3 box on target 


CELL_IS_WALL 		= 0
CELL_EMPTY_SPACE 	= 1
CELL_TARGET 		= 2
CELL_BOX_ON_TARGET 	= 3
CELL_IS_BOX 		= 4
CELL_PLAYER 		= 5
CELL_SWITCH_OFF 	= 7
CELL_SWITCH_ON 		= 8



# for flip - box cannot be on switch 
# player can be on target and switch -- 5 is shown in that case 
# box can be on target - game ends 
# 

def concept_box_above(state):
	# assumes room state

	# returns true if box is above...


	try : 

		player_idx = np.argwhere(state == 5)[0]

		try : 
			box_idx = np.argwhere(state == 4)[0]
		except : 
			box_idx = np.argwhere(state == 3)[0]

		py,px = player_idx
		by,bx = box_idx

		if (bx == px) and (by+1 == py) :
			return True
		else :
			return False
	except : 
		print (state)

def concept_box_below(state):
	# assumes room state

	player_idx = np.argwhere(state == 5)[0]
	try : 
		box_idx = np.argwhere(state == 4)[0]
	except : 
		box_idx = np.argwhere(state == 3)[0]

	py,px = player_idx
	by,bx = box_idx

	if (bx == px) and (by-1 == py) :
		return True
	else :
		return False

def concept_box_left(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if( (state[py][px-1] == CELL_BOX_ON_TARGET) or (state[py][px-1] == CELL_IS_BOX) ) :
			return True 
	except : 
		pass 

	return False 

def concept_box_right(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if((state[py][px+1] == CELL_BOX_ON_TARGET) or (state[py][px+1] == CELL_IS_BOX)) :
			return True 
	except : 
		pass 

	return False 




def concept_switch_on(state):
	# 7 when off, 8 on
	# not present when box on it.

	# assume : when box on switch -- 'its on!'

	status = True 
	switch_state = np.argwhere(state == 8)
	if len(switch_state) == 0 :
		status = False

	return status




def concept_empty_below(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py+1][px] == CELL_EMPTY_SPACE) :
			return True 
	except : 
		pass 

	return False 

def concept_empty_above(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py-1][px] == CELL_EMPTY_SPACE) :
			return True 
	except : 
		pass 

	return False 

def concept_empty_left(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py][px-1] == CELL_EMPTY_SPACE) :
			return True 
	except : 
		pass 

	return False 

def concept_empty_right(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py][px+1] == CELL_EMPTY_SPACE) :
			return True 
	except : 
		pass 

	return False 





# wall is below player, above player so on...

def concept_wall_below(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py+1][px] == CELL_IS_WALL) :
			return True 
	except : 
		pass 

	return False 

def concept_wall_above(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py-1][px] == CELL_IS_WALL) :
			return True 
	except : 
		pass 

	return False 

def concept_wall_left(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py][px-1] == CELL_IS_WALL) :
			return True 
	except : 
		pass 

	return False 

def concept_wall_right(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py][px+1] == CELL_IS_WALL) :
			return True 
	except : 
		pass 

	return False 




# player is above switch, below switch so on...

def concept_above_switch(state):
	py,px  = np.argwhere(state == CELL_PLAYER)[0] 
	try : 
		if((state[py+1][px] == CELL_SWITCH_ON) or ((state[py+1][px] == CELL_SWITCH_OFF)) ) :
			return True 
	except : 
		pass 

	return False 

def concept_below_switch(state):
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	try : 
		if((state[py-1][px] == CELL_SWITCH_ON) or ((state[py-1][px] == CELL_SWITCH_OFF)) ) :
			return True 
	except : 
		pass 

	return False 

def concept_left_switch(state):
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	try : 
		if((state[py][px+1] == CELL_SWITCH_ON) or ((state[py][px+1] == CELL_SWITCH_OFF)) ) :
			return True 
	except : 
		pass 

	return False 

def concept_right_switch(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if((state[py][px-1] == CELL_SWITCH_ON) or ((state[py][px-1] == CELL_SWITCH_OFF)) ) :
			return True 
	except : 
		pass 

	return False 




# target below / left / right / above player ....

def concept_target_below(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py+1][px] == CELL_TARGET) :
			return True 
	except : 
		pass 

	return False 

def concept_target_above(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py-1][px] == CELL_TARGET) :
			return True 
	except : 
		pass 

	return False 

def concept_target_left(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py][px-1] == CELL_TARGET) :
			return True 
	except : 
		pass 

	return False 

def concept_target_right(state):
	# empty below player -- 
	py,px  = np.argwhere(state == CELL_PLAYER)[0]
	# if something is below -- 
	try : 
		if(state[py][px+1] == CELL_TARGET) :
			return True 
	except : 
		pass 

	return False 





# wall_left_below_ofbox

def concept_wall_left_below_ofbox(state) :

	try : 
		box_idx = np.argwhere(state == 4)[0]
	except : 
		box_idx = np.argwhere(state == 3)[0]

	# should be one of the two...
	by,bx = box_idx
	try : 
		if((state[by][bx-1] == CELL_IS_WALL) and ((state[by+1][bx] == CELL_IS_WALL))) :
		# left   									below
			return True 
	except : 
		pass 

	return False 


#  orderL2R_player_box_target

def concept_orderL2R_player_box_target(state):
	try : 
		box_idx = np.argwhere(state == 4)[0]
	except : 
		box_idx = np.argwhere(state == 3)[0]

	# should be one of the two...
	by,bx = box_idx
	# now player is to left and target is to right
	try : 
		if((state[by][bx-1] == CELL_PLAYER) and ((state[by][bx+1] == CELL_TARGET))) :
		# left   									right
			return True 
	except : 
		pass 

	return False 

def concept_orderL2R_target_box_player(state):
	try : 
		box_idx = np.argwhere(state == 4)[0]
	except : 
		box_idx = np.argwhere(state == 3)[0]

	# should be one of the two...
	by,bx = box_idx
	# now player is to right and target is to left
	try : 
		if((state[by][bx-1] == CELL_TARGET) and ((state[by][bx+1] == CELL_PLAYER))) :
		# left   									right
			return True 
	except : 
		pass 
		
	return False 


# order_T2D_target_box_player

def concept_order_T2D_target_box_player(state):
	try : 
		box_idx = np.argwhere(state == 4)[0]
	except : 
		box_idx = np.argwhere(state == 3)[0]

	# should be one of the two...
	by,bx = box_idx
	# now player is to below and target is to above
	try : 
		if((state[by-1][bx] == CELL_TARGET) and ((state[by+1][bx] == CELL_PLAYER))) :
		# above   									below
			return True 
	except : 
		pass 
		
	return False 



# empty_below -- space below 			done
# empty_left -- space left  			done 
# empty_right 							done 
# wall_below   							done 
# wall_left 							done
# wall_right 							done
# wall_above  							done 
# box_onleft 							done
# box_onright  							done
# aboveof_switch 						done 
# leftof_switch							done 
# rightof_switch   (by the name of green pellete)		done
# belowof_switch						done
# orderL2R_target_box_player			done
# orderL2R_player_box_target 			done
# order_T2D_target_box_player			done
# wall_left_below_ofbox 				done
# target_onleft_player					done
# target_onright_player					done  - above/below also done.
# # concept_switch_on 					done
# # concept_box_above 					done 
# # concept_box_below  					done
















def getMask(state):
	player_idx = np.argwhere(state == 5)[0]
	pmask = np.zeros_like(state)
	pmask[player_idx[0], player_idx[1]] = 1 

	bmask = np.zeros_like(state)

	try : 
		box_idx = np.argwhere(state == 4)[0]
	except : 
		box_idx = np.argwhere(state == 3)[0]

	bmask[box_idx[0], box_idx[1]] = 1 

	return pmask, bmask 

def updateMask(state, pmask, bmask):
	player_idx = np.argwhere(state == 5)[0]

	try : 
		box_idx = np.argwhere(state == 4)[0]
	except : 
		box_idx = np.argwhere(state == 3)[0]


	pmask[player_idx[0], player_idx[1]] += 1
	bmask[box_idx[0], box_idx[1]] += 1 

	return pmask, bmask

# def concept_box_left(state):
# 	print ("working")
# 	return True

# def concept_box_right(state):
# 	print ("working")
# 	return True


# we can do class stuff - but is it worth it? since like 3 concepts --- 


# class Logic:
# 	def __init__(self, name="box_above"):
# 		self.name = name

# 	def run(self, state):
# 		pass





# class Box_Above(Logic):
# 	def run(self, state):

	



# def sample(a):
# 	print (a*2)

# eval("sample")(2)