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

#    surfaces = [wall, floor, box_target, box_on_target, box, player, player_on_target, special_cell, on_special_cell, box_on_special_cell]
 
CELL_IS_WALL 		= 0
CELL_EMPTY_SPACE 	= 1
CELL_TARGET 		= 2
CELL_BOX_ON_TARGET 	= 3
CELL_IS_BOX 		= 4
CELL_PLAYER 		= 5
CELL_PLAYER_ON_TRGT = 6
CELL_SPECIAL_CELL 	= 7
CELL_PLAYER_ON_SPL 	= 8
CELL_BOX_ON_SPL     = 9




###-----
## "avoid bug", "avoid bug to score the best points"
##"box_not_in_pitfall", "the box is not in the pitfall"
##"No_pink_obstacle", "There is no pink obstacle while going up which adds extra points to the score\n" 
##---
def concept_on_pink_cell(state):
    try :
        if CELL_BOX_ON_SPL in state:
            return True
        else:
            return False
    except :
        print (state)
        exit(1)




## No_wall_on_the_top", "There is no wall on top of the box"
##"Wall_above", "There is wall above." 
##"No_wall_above.", "There is no wall above."
## "Wall_up", "The wall is on the front of the player."
##"Wall_on_top", "There is a wall on top side\n" 
##"No_wall_on_top_1", "There is no wall on the top for 1 space." 
##"No_wall_on_top", "There is no brick wall on top"
##---
def concept_wall_on_top(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 0 and state[py-1][px] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)


##"No_wall_on_top_m", "There is no wall on the top side for more than 1 space"
##---
def concept_no_wall_on_top_m(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 1 and state[py-1][px] != CELL_IS_WALL and state[py-2][px] != CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



##"No_pink_barrier_on_top", "There is no pink barrier on top of the box carried by the player" 
##"Pink_box_above", "There is a pink box above." 
##"No_pink_box_above", "There is no pink box above."
##No_wall_upwards", "There is no pink wall in the upward direction. "
##"Bug_on_top", "There is a bug on the top side"
## "No_bug_on_top_1", "There is no bug on top for 1 move"
##---

def concept_pink_cell_on_top(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 0 and state[py-1][px] == 7:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



##"No_bug_on_top_m", "There is no bug on top for more than 1 move" 
##---
def concept_no_pink_cell_on_top_m(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 1 and state[py-1][px] != 7 and state[py-2][px] != 7:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)


##"red_target_above", "There is red target above." 
##"Target_up", "The target is on the upwards direction of the player."
##"Red_target", "There is a red target on top which is the destination"
##----
def concept_target_on_top(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 0 and state[py-1][px] == CELL_TARGET:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)

##"Box_up", "The box is in the upward direction of the player. "
##"box_above", "the box is right above the green creature"
##---
def concept_box_on_top(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        if CELL_IS_BOX in state:
            box_idx = np.argwhere(state == CELL_IS_BOX)[0]
        elif CELL_BOX_ON_TARGET in state:    
            box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
        else:
            box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]

        py,px = player_idx
        by,bx = box_idx
 

        if by == (py-1) and bx == px:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)




##"No_wall_below", "There is no wall right below the box" 
## "Wall_below", "There is wall below the yellow box." 
##"No_wall_below", "There is no wall below the yellow box."
##"Wall_down", "There is a wall down"
## "No_wall_down_1", "There is no wall down for 1 move" 
##"No_wall_bottom", "There is no wall while going down"
##---
def concept_wall_below(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py < len(state)-1 and state[py+1][px] == 0:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)




##"No_wall_down_m", "There is no wall down for more than 1 move"
def concept_no_wall_below_m(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py < len(state)-2 and state[py+1][px] != 0 and state[py+2][px] != 0:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)
 
##---
## "No_pink_barrier_below", "There is no pink barrier right below the box" 
##"Pink_box_below", "There is a pink box below the yellow box." 
##"No_pink_box_below", "There is no pink box below the yellow box."
##"No_bug_down_1", "There is no bug down for 1 move" 
## "Bug_down", "There is a bug down" 
##---
def concept_pink_cell_below(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py < len(state)-1 and state[py+1][px] == 7:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)




##"No_bug_down_m", "There is no bug down for more than 1 move"
##---
def concept_no_pink_cell_below_m(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py < len(state)-2 and state[py+1][px] != 7 and state[py+2][px] != 7:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



## "black_space_below", "There is empty lack space below the box" 
##---
def concept_blank_cell_below(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py < len(state)-1 and state[py+1][px] == 1:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)

## "Red_target_below", "There is red target below the yellow box."
## "No_red_target_below", "There is no red target below the yellow box."
##---
def concept_target_below(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py < len(state)-1 and state[py+1][px] == CELL_TARGET:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)

## "box_below", "the box is right below the green creature"
##---
def concept_box_below(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        if CELL_IS_BOX in state:
            box_idx = np.argwhere(state == CELL_IS_BOX)[0]
        elif CELL_BOX_ON_TARGET in state:    
            box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
        else:
            box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]

        py,px = player_idx
        by,bx = box_idx
 

        if by == (py+1) and bx == px:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)


##"No_wall_on_the_left", "There is no wall on the left of the box" 
##"Wall_on_left", "There is wall left to the yellow box."
## "No_wall_on_left.", "There is no wall on left to the yellow box." 
##"Wall_left", "There is a wall on the left side" 
##"No_wall_left", "There is no wall on the left side"
## "No_wall_on_left", "There is no wall on the left for the box to go" 
##---
def concept_wall_on_left(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if px > 0 and state[py][px-1] == 0:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



##"Wall_left_m", "There is no wall on the left for more than 1 space" 
##---
def concept_no_wall_on_left_m(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if px > 1 and state[py][px-1] != 0 and state[py][px-2] != 0:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)


##"No_pink_barrier_on_the_left", "There is no pink barrier to the left of the box" 
##"Pink_box_on_left", "There is a pink box on left of the yellow box." 
##"No_pink_box_on_left", "There is no pink box on left of the yellow box." 
## "Bug_left", "There is a bug on the left"
##"No_bug_left", "There is no bug on the left"
##---
def concept_pink_cell_on_left(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if px > 0 and state[py][px-1] == 7:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)

##"Black_space_on_the_left", "There is a black space available to the left of the box"
##---
def concept_blank_cell_on_left(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if px > 0 and state[py][px-1] == 1:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



## "Red_marker_on_the_left", "There is a red marker on the left of the box" 
## "Red_target_on_left", "There is red target on the left of the yellow box." "No_red_target_on_left", "There is no red target on the left of the yellow box."
##---
def concept_target_on_left(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if px > 0 and state[py][px-1] == 2:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)

##"Box_on_left", "The box is on the left of the player." 
##"box_on_left", "the box is right on the left of the green creature"
##---
def concept_box_on_left(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        if CELL_IS_BOX in state:
            box_idx = np.argwhere(state == CELL_IS_BOX)[0]
        elif CELL_BOX_ON_TARGET in state:    
            box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
        else:
            box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]

        py,px = player_idx
        by,bx = box_idx
 

        if by == py and bx == (px - 1):
            return True
        else :
            return False
    except :
        print (state)
        exit(1)




##"No_pink_barrier_on_the_right", "There is no pink barrier on the right of the box" 
##"Pink_box_on_right", "There is a pink box on right of the yellow box." 
##"No_pink_box_on_right", "There is no pink box on right of the yellow box."
##"Bug_right", "There is a bug on the right side" 
##"No_bug_right", "There is no bug on the right side"
##---
def concept_pink_cell_on_right(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if px < len(state[py]) - 1 and state[py][px+1] == 7:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



##"Red_marker_on_the_right", "There is a red marker on the right of the box"
##"Target_on_right", "There is red target on the right of the yellow box." 
##"No_target_on_right", "There is no red target on the right of the yellow box."
##---

def concept_target_on_right(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if px < len(state[py]) - 1 and state[py][px+1] == CELL_TARGET:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



## "No_wall_on_the_right", "There is no wall on the right of the box"
##"no_wall_on_the_right_of_the_box", "There is no wall on the right of the box so that it can't be pushed right"
##---
def concept_wall_on_right_of_box(state):
    try :
        if CELL_IS_BOX in state:
            box_idx = np.argwhere(state == CELL_IS_BOX)[0]
        elif CELL_BOX_ON_TARGET in state:    
            box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
        else:
            box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]

        by,bx = box_idx
        if bx < len(state[by]) - 1 and state[by][bx+1] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



##"No_wall_on_right", "There is no wall on the right\n"
##---
def concept_wall_on_right(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if px < len(state[py]) - 1 and state[py][px+1] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)




##"No_wall_right_m", "There is no wall on the right for more than 1 space" 
##---
def concept_no_wall_on_right_m(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if px < len(state[py]) - 2 and state[py][px+1] != CELL_IS_WALL and state[py][px+2] != CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)




##"Box_on_right", "The box is on the right of the player."
## "box_on_right", "the box is on the immediate right of the green creature"
##---
def concept_box_on_right(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        if CELL_IS_BOX in state:
            box_idx = np.argwhere(state == CELL_IS_BOX)[0]
        elif CELL_BOX_ON_TARGET in state:    
            box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
        else:
            box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]

        py,px = player_idx
        by,bx = box_idx
 

        if by == py and bx == (px + 1):
            return True
        else :
            return False
    except :
        print (state)
        exit(1)






##"Wall_down_left_right", "There is a wall on the bottom, left and right sides\n"
##"Wall_on_bottom_left_right", "In this case, there will be a deadlock if box reaches to this position"
##--
def concept_wall_down_left_right(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py < len(state) - 1 and px > 0 and px < len(state[py]) - 1 and state[py+1][px] == CELL_IS_WALL and state[py][px-1] == CELL_IS_WALL and state[py][px+1] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



## "Wal_down_left", "There is a wall on the bottom and left sides" 
## "Wall_left_bottom", "There is a wall on the left and bottom sides"
##---
def concept_wall_down_left(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py < len(state) - 1 and px > 0 and state[py+1][px] == CELL_IS_WALL and state[py][px-1] == CELL_IS_WALL:
            return True
        else:
            return False
    except :
        print (state)
        exit(1)


##"Wall_down_right", "There is a wall on the bottom and right sides" 
## "Wall_right_bottom", "There is a wall on the bottom and right sides"
##---
def concept_wall_down_right(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py < len(state) - 1  and px < len(state[py]) - 1 and state[py+1][px] == CELL_IS_WALL and state[py][px+1] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)


## "Wall_left_top", "There is a wall on the left and top sides"
##"Wall_top_left", "There is a wall on the top and left sides"
##---
def concept_wall_top_left(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 0 and px > 0 and state[py-1][px] == CELL_IS_WALL and state[py][px-1] == CELL_IS_WALL:
            return True
        else:
            return False
    except :
        print (state)
        exit(1)



##"Wall_left_bottom_top", "There is a wall on the left, bottom and top sides" 
##---
def concept_wall_top_down_left(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 0 and py < len(state) - 1 and px > 0 and state[py-1][px] == CELL_IS_WALL and state[py+1][px] == CELL_IS_WALL and state[py][px-1] == CELL_IS_WALL:
            return True
        else:
            return False
    except :
        print (state)
        exit(1)


##"Wall_right_top", "There is a wall on the top and right sides"
##"Wall_top_right", "There is a wall on the top and right sides"
##----
def concept_wall_top_right(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 0  and px < len(state[py]) - 1 and state[py-1][px] == CELL_IS_WALL and state[py][px+1] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)


##"Wall_top_bottom_right", "There is a wall on the top, bottom, and right sides" 
##"Wall_on_right_top_bottom", "There will be a situation of deadlock in case box goes in this." 
##---
def concept_wall_up_down_right(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 0  and py < len(state) - 1  and px < len(state[py]) - 1 and state[py-1][px] == CELL_IS_WALL and state[py+1][px] == CELL_IS_WALL and state[py][px+1] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)


## "Wall_top_left_right", "There is a wall on the top, left, and right sides" 
##"Wall_top_left_right", "In this case there is no way to go back and continue the game. Its deadend" 
##---
def concept_wall_top_left_right(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 0  and px < len(state[py]) - 1 and px > 0 and state[py-1][px] == CELL_IS_WALL and state[py][px+1] == CELL_IS_WALL and state[py][px-1] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



##Wall_on_top_down_left", "There will be a situation of deadlock in case the box goes in this position"
##---
def concept_wall_up_down_left(state):
    try :
        if 5 in state:
            player_idx = np.argwhere(state == 5)[0]
        elif 6 in state:    
            player_idx = np.argwhere(state == 6)[0]
        else:
            player_idx = np.argwhere(state == 8)[0]

        py,px = player_idx
        if py > 0  and py < len(state) - 1  and px > 0 and state[py-1][px] == CELL_IS_WALL and state[py+1][px] == CELL_IS_WALL and state[py][px-1] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



##"no_wall_below_the_box", "there is no wall right below the box that blocks it from being pushed down"
##---
def concept_wall_below_box(state):
    try :
        if CELL_IS_BOX in state:
            box_idx = np.argwhere(state == CELL_IS_BOX)[0]
        elif CELL_BOX_ON_TARGET in state:    
            box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
        else:
            box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]

        by,bx = box_idx
        if by < len(state) - 1 and state[by+1][bx] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)


##"no_wall_on_the_left_of_the_box", "there is no wall on the left of the box blocking it from being pushed left"
##---
def concept_wall_on_left_of_box(state):
    try :
        if CELL_IS_BOX in state:
            box_idx = np.argwhere(state == CELL_IS_BOX)[0]
        elif CELL_BOX_ON_TARGET in state:    
            box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
        else:
            box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]

        by,bx = box_idx
        if bx > 0 and state[by][bx - 1] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)


##---
##No_wall_above_the_box", "there is no wall blocking the box from being pushed up"
##---
def concept_wall_above_box(state):
    try :
        if CELL_IS_BOX in state:
            box_idx = np.argwhere(state == CELL_IS_BOX)[0]
        elif CELL_BOX_ON_TARGET in state:    
            box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
        else:
            box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]

        by,bx = box_idx
        if by > 0 and state[by-1][bx] == CELL_IS_WALL:
            return True
        else :
            return False
    except :
        print (state)
        exit(1)



##















def getMask(state):
    if 5 in state:
        player_idx = np.argwhere(state == 5)[0]
    elif 6 in state:    
        player_idx = np.argwhere(state == 6)[0]
    else:
        player_idx = np.argwhere(state == 8)[0]

    if CELL_IS_BOX in state:
        box_idx = np.argwhere(state == CELL_IS_BOX)[0]
    elif CELL_BOX_ON_TARGET in state:    
        box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
    else:
        box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]


    pmask = np.zeros_like(state)
    pmask[player_idx[0], player_idx[1]] = 1 

    bmask = np.zeros_like(state)

    bmask[box_idx[0], box_idx[1]] = 1 

    return pmask, bmask 

def updateMask(state, pmask, bmask):
    if 5 in state:
        player_idx = np.argwhere(state == 5)[0]
    elif 6 in state:    
        player_idx = np.argwhere(state == 6)[0]
    else:
        player_idx = np.argwhere(state == 8)[0]

    if CELL_IS_BOX in state:
        box_idx = np.argwhere(state == CELL_IS_BOX)[0]
    elif CELL_BOX_ON_TARGET in state:    
        box_idx = np.argwhere(state == CELL_BOX_ON_TARGET)[0]
    else:
        box_idx = np.argwhere(state == CELL_BOX_ON_SPL)[0]


    pmask[player_idx[0], player_idx[1]] += 1
    bmask[box_idx[0], box_idx[1]] += 1 

    return pmask, bmask


