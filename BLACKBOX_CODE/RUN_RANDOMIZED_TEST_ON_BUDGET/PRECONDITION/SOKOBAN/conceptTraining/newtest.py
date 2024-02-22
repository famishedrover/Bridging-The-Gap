#!/usr/bin/env python
# python_example.py
# Author: Ben Goodrich
#
# This is a direct port to python of the shared library example from
# ALE provided in doc/examples/sharedLibraryInterfaceExample.cpp
import sys
from random import randrange
from ale_python_interface import ALEInterface

import numpy as np
from matplotlib import pyplot as plt 

if len(sys.argv) < 2:
  print('Usage: %s rom_file' % sys.argv[0])
  sys.exit()

ale = ALEInterface()

# Get & Set the desired settings
ale.setInt(b'random_seed', 123)



def setKthBit(n,k): 
  
    # kth bit of n is being 
    # set by this operation 
    return ((1 << k) && n) 






# Set USE_SDL to true to display the screen. ALE must be compiliedinbxfgdrgbfvcvx
# with SDL enabled for this to work. On OSX, pygame init is used to
# proxy-call SDL_main.
USE_SDL = False
if USE_SDL:
  if sys.platform == 'darwin':
    import pygame
    pygame.init()
    ale.setBool('sound', False) # Sound doesn't work on OSX
  elif sys.platform.startswith('linux'):
    ale.setBool('sound', True)
  ale.setBool('display_screen', True)

# Load the ROM file
rom_file = str.encode(sys.argv[1])
ale.loadROM(rom_file)

# Get the list of legal actions
legal_actions = ale.getLegalActionSet()

print ('Legal Actions :', legal_actions)



def printKthBit(n, k): 
    print(n & (1 << (k-1))) 

def isSame(ram1, ram2, text="") :
  if text == "" :
    pass 
  else : 
    print('-'*20)
    print (text)
  if( np.array_equal(ram1, ram2) ):
    if text != "" :
      print ("SAME!!")
    return True 
  else : 
    if text != "" :
      print ("DIFFERENT!")
    return False




orginalram = ale.getRAM()
originalScreenshot = ale.getScreenRGB()



# Play 10 episodes

changeRAM  = np.zeros_like(orginalram)
changeScreenshot = np.zeros_like(originalScreenshot)

changea = None
runIter = 0

while not ale.game_over():
  a = legal_actions[randrange(len(legal_actions))]
  # Apply an action and get the resulting reward
  
  currRAM = ale.getRAM()
  printKthBit( currRAM[53], 3)


  reward = ale.act(a)



  plt.imshow(ale.getScreenRGB())
  plt.pause(1)
  plt.clf()

ale.reset_game()



# ale.reset_game()

# currentRAM = ale.getRAM()
# currentScreenshot = ale.getScreenRGB()

# ale.setRAM(changeRAM)
# newChangeRAM = ale.getRAM()
# newChangeScreenshot = ale.getScreenRGB()

# ale.act(changea)
# print("Action Taken : ", changea)

# newChangeRAM2 = ale.getRAM()
# newChangeScreenshot2 = ale.getScreenRGB()



# fig = plt.figure(figsize=(8,8))

# ax = fig.add_subplot(3,2,1)
# ax.title.set_text('Original Screenshot')
# plt.imshow(originalScreenshot)


# ax = fig.add_subplot(3,2,2)
# ax.title.set_text('Some State after the original')
# plt.imshow(changeScreenshot)

# ax = fig.add_subplot(3,2,3)
# ax.title.set_text('Reset')
# plt.imshow(currentScreenshot)

# ax = fig.add_subplot(3,2,4)
# ax.title.set_text('After SetRAM')
# plt.imshow(newChangeScreenshot)


# ax = fig.add_subplot(3,2,5)
# ax.title.set_text('Take and action after "SetRAM" ')
# plt.imshow(newChangeScreenshot2)


# plt.show()


# isSame(newChangeScreenshot, currentScreenshot, "screenshot comparison, newCHANGED/current")
# isSame(newChangeRAM, currentRAM  , "RAM comparison, newchange/current")
# # isSame(newChangeRAM, currentRAM  , "RAM comparison, old/new")






# ALL ACTIONS 
        # case PLAYER_A_NOOP:
        # case PLAYER_A_FIRE:
        # case PLAYER_A_UP:
        # case PLAYER_A_RIGHT:
        # case PLAYER_A_LEFT:
        # case PLAYER_A_DOWN:
        # case PLAYER_A_UPRIGHT:
        # case PLAYER_A_UPLEFT:
        # case PLAYER_A_DOWNRIGHT:
        # case PLAYER_A_DOWNLEFT:
        # case PLAYER_A_UPFIRE:
        # case PLAYER_A_RIGHTFIRE:
        # case PLAYER_A_LEFTFIRE:
        # case PLAYER_A_DOWNFIRE:
        # case PLAYER_A_UPRIGHTFIRE:
        # case PLAYER_A_UPLEFTFIRE:
        # case PLAYER_A_DOWNRIGHTFIRE:
        # case PLAYER_A_DOWNLEFTFIRE: