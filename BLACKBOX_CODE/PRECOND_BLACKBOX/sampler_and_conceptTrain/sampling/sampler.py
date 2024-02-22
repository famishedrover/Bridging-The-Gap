import gym
import numpy as np
from matplotlib import pyplot as plt
import random
import pickle
from shutil import copy2
from agents.HumanAgent import *
import time
import shutil
import os
import yaml

import time

import random 



# All actions ------------------------------------------------------------------------------------------------------------

ACTION_NOOP = 0
ACTION_FIRE = 1
ACTION_UP = 2
ACTION_RIGHT = 3
ACTION_LEFT = 4
ACTION_DOWN = 5
ACTION_UPRIGHT = 6
ACTION_UPLEFT = 7
ACTION_DOWNRIGHT = 8
ACTION_DOWNLEFT = 9
ACTION_UPFIRE = 10
ACTION_RIGHTFIRE = 11
ACTION_LEFTFIRE = 12
ACTION_DOWNFIRE = 13
ACTION_UPRIGHTFIRE = 14
ACTION_UPLEFTFIRE = 15
ACTION_DOWNRIGHTFIRE = 16
ACTION_DOWNLEFTFIRE = 17



#  ========================================================================================================================
#  ========================================================================================================================
#  ================================================== LEVEL 1 =============================================================
#  ========================================================================================================================
#  ========================================================================================================================


class Sampler:
	def __init__(self, _data_folder, num_episodes=2,
				 sampling_type="vanilla_random",
				 agent="random",
				 conditions=None,
				 no_pos=5,
				 no_neg=10,
				 ):
		if conditions is None:
			conditions = []
		self.num_episodes = num_episodes
		self.sampling_type = sampling_type
		self.data_folder = _data_folder
		self.env = None
		self.ale = None
		self.agent = agent
		self.sample_count = 0
		self.conditions = conditions

		self.condition_to_sample_map = {}
		for cond in self.conditions:
			self.condition_to_sample_map[cond] = set()
		self.no_pos = no_pos
		self.no_neg = no_neg
		self.all_states = []
		self.all_states_RGB = []
		self.all_actions = []
		self.all_states_action_seq = []

	def create_directory_structure(self):
		if os.path.exists("%s/samples" % self.data_folder):
			shutil.rmtree("%s/samples" % self.data_folder)
		if os.path.exists("%s/concepts" % self.data_folder):
			shutil.rmtree("%s/concepts" % self.data_folder)
		os.makedirs("%s/samples" % self.data_folder)
		os.makedirs("%s/concepts" % self.data_folder)
		for condition in self.conditions:
			os.makedirs("%s/concepts/%s" % (self.data_folder, condition))
		print("directory structure created")

	def game_state_condition_check(self, condition, ram, idx=None):
		if ram[58] < 5:
			# ignore cases where Joe has died
			return False
		if condition == "on_rope":
			byte_val = ram[30]
			if byte_val == 144 or byte_val == 123:
				return True
		elif condition == "on_ground_and_alive":
			y_pos = ram[43]
			lives = ram[58]
			midair = ram[30]
			if y_pos == 148 and lives == 5 and midair != 165:
				return True
		elif condition == "on_ladder1":
			ladder = ram[30]
			x_pos = ram[42]
			if (ladder == 62 or ladder == 82) and x_pos == 21:
				return True
		elif condition == "on_ladder2":
			ladder = ram[30]
			x_pos = ram[42]
			if (ladder == 62 or ladder == 82) and x_pos == 77:
				return True
		elif condition == "on_ladder3":
			ladder = ram[30]
			x_pos = ram[42]
			if (ladder == 62 or ladder == 82) and x_pos == 133:
				return True
		elif condition == "skull_on_left":
			rgb = self.all_states_RGB[idx]
			joe_pos = np.array(np.where(rgb == [228, 111, 111]))[0:2, 0]
			skull_pos = np.array(np.where(rgb[100:] == [236, 236, 236]))[0:2, 0] \
						+ np.array([100, 0])
			if idx < len(self.all_states) - 1:
				y_pos = ram[43]
				midair = ram[30]
				next_state_lives = self.all_states[idx+1][58]
				if y_pos == 148 \
						and midair != 165 \
						and next_state_lives == 4\
						and joe_pos[1] > skull_pos[1]:
					return True
		elif condition == "skull_on_right":
			rgb = self.all_states_RGB[idx]
			joe_pos = np.array(np.where(rgb == [228, 111, 111]))[0:2, 0]
			skull_pos = np.array(np.where(rgb[100:] == [236, 236, 236]))[0:2, 0] \
						+ np.array([100, 0])
			if idx < len(self.all_states) - 1:
				y_pos = ram[43]
				midair = ram[30]
				next_state_lives = self.all_states[idx + 1][58]
				if y_pos == 148 \
						and midair != 165 \
						and next_state_lives == 4\
						and joe_pos[1] < skull_pos[1]:
					return True
		elif condition == "has_key":
			inventory = ram[66]
			if inventory == 14:
				return True
		elif condition == "on_highest_platform":
			y_pos = ram[43]
			if y_pos == 235:
				return True
		elif condition == "on_middle_platform":
			y_pos = ram[43]
			if y_pos == 192:
				return True
		elif condition == "door_on_right_position":
			y_pos = ram[43]
			x_pos = ram[42]
			if x_pos == 129 and y_pos == 235:
				return True
		elif condition == "door_on_left_position":
			y_pos = ram[43]
			x_pos = ram[42]
			if x_pos == 24 and y_pos == 235:
				return True
		elif condition == "wall_on_left":
			y_pos = ram[43]
			x_pos = ram[42]
			if x_pos == 9 and y_pos == 192:
				return True
		elif condition == "wall_on_right":
			y_pos = ram[43]
			x_pos = ram[42]
			if x_pos == 145 and y_pos == 192:
				return True
		elif condition == "key_on_right":
			y_pos = ram[43]
			x_pos = ram[42]
			inventory = ram[66]
			if inventory == 14:
				return False
			if y_pos == 192:
				if 9 <= x_pos <= 11:
					return True
		elif condition == "key_above":
			y_pos = ram[43]
			x_pos = ram[42]
			inventory = ram[66]
			if inventory == 14:
				return False
			if y_pos == 192:
				if 12 <= x_pos <= 15:
					return True
		elif condition == "key_on_left":
			y_pos = ram[43]
			x_pos = ram[42]
			inventory = ram[66]
			if inventory == 14:
				return False
			if y_pos == 192:
				if 16 <= x_pos <= 20:
					return True
		elif condition == "holding_on_to_the_rope_top":
			y_pos = ram[43]
			byte_val = ram[30]
			if byte_val == 144 or byte_val == 123:
				if 208 <= y_pos <= 212:
					return True
		elif condition == "holding_on_to_the_rope_bottom":
			y_pos = ram[43]
			byte_val = ram[30]
			if byte_val == 144 or byte_val == 123:
				if 181 <= y_pos <= 185:
					return True
		

		elif condition == "on_edge_left":
			# print ("Sdf")
			cond = self.checkOnEdgeLeft(ram)
			# print ("condition :",cond)
			return cond
		
		elif condition == "on_edge_right":
			cond = self.checkOnEdgeRight(ram)
			return cond 

		return False


		 





	def condition_based_sampling(self):
		for condition in self.conditions:
			pos_states_indices = []
			for state_idx, state in enumerate(self.all_states):
				if self.game_state_condition_check(condition, state, state_idx):
					pos_states_indices.append(state_idx)
			assert len(self.all_states) == self.sample_count
			neg_states_indices = list(set(range(self.sample_count)) - set(pos_states_indices))
			print("for condition: %s, no of pos samples found: %d" %(condition, len(pos_states_indices)))
			self.save_samples(condition, "pos", pos_states_indices, self.no_pos)
			self.save_samples(condition, "neg", neg_states_indices, self.no_neg)

	def save_samples(self, condition, prefix, indices, no):
		sampled_indices = indices
		if no < len(indices):
			sampled_indices = random.sample(indices, no)
		for idx in sampled_indices:
			copy2("%s/samples/sample%d_image.png" % (self.data_folder, idx),
				  "%s/concepts/%s/%s_sample%d_image.png" % (self.data_folder, condition, prefix, idx))
			copy2("%s/samples/sample%d_RAM.b" % (self.data_folder, idx),
				  "%s/concepts/%s/%s_sample%d_RAM.b" % (self.data_folder, condition, prefix, idx))
			copy2("%s/samples/sample%d_RGB.b" % (self.data_folder, idx),
				  "%s/concepts/%s/%s_sample%d_RGB.b" % (self.data_folder, condition, prefix, idx))

	def create_visit_map(self):
		total_samples = self.sample_count
		all_face_pixels = []
		file = "%s/samples/sample%d_image.png" % self.data_folder
		for i in range(total_samples):
			rgb = plt.imread(file % i)
			for j in range(rgb.shape[0]):
				for k in range(rgb.shape[1]):
					print(rgb[j][k])
					if np.array_equal(rgb[j][k], [0.78431374, 0.28235295, 0.28235295, 1.0]):
						face_pixels = [j, k]
						all_face_pixels.append(tuple(face_pixels))
		screen_1 = plt.imread(file % 0)
		all_face_pixels = set(all_face_pixels)
		for pixel in all_face_pixels:
			screen_1[pixel[0]][pixel[1]] = [0, 0, 255, 1]
		# print(all_face_pixels)
		plt.imshow(screen_1)
		plt.show()

	def set_starting_state(self):
		self.env.seed(0)
		if self.sampling_type == "vanilla_random":
			self.env.reset()
			return []
		elif self.sampling_type == "random_restart_from_plan":
			file_prefix = "./config/humanAgentSamples/"
			# print (os.getcwd())
			file = file_prefix + "action_sequence.b"

			
			with open(file, 'rb') as fp:
				action_sequence = pickle.load(fp)
			random_state_idx = random.choice(range(len(action_sequence)))
			self.env.reset()
			for action in action_sequence[:random_state_idx+1]:
				_ = self.env.step(action)
				assert _[3]['ale.lives'] == 6
			print("Starting from state-%d" % random_state_idx)
			return action_sequence[:random_state_idx+1]

		elif self.sampling_type == "fixStart" :
			self.env = gym.make('MontezumaRevenge-ramDeterministic-v0')
			self.env.seed(0)
			self.env.reset()

			with open("./full_plans/plantoLevel3Start.b","rb") as f :
				plan = pickle.load(f)

			for action in plan:
				self.env.step(action)
				time.sleep(0.01)
				self.env.render()

			# self.env = env 
			return plan 

		else:
			self.env.reset()
			return []


	def dieAndCheckEdge(self,plan, direction="left", rendering=False) :
		env = gym.make('MontezumaRevenge-ramDeterministic-v0')
		env.seed(0)
		env.reset()

		for action in plan:
			env.step(action)
			if rendering:
				env.render()

		if direction == "left" :
			env.step(ACTION_LEFT)
		else : 
			env.step(ACTION_RIGHT)

		ram = env.unwrapped._get_ram()
		x_prev = ram[42]

		i = 0 
		Set = False 
		Dead = False 

		if direction == "left" :
			observation, reward, done, info = env.step(ACTION_RIGHT)
			ram = env.unwrapped._get_ram()
			x = ram[42]
			if x <= x_prev : 
				Set = True 
		else : 
			observation, reward, done, info = env.step(ACTION_LEFT)
			ram = env.unwrapped._get_ram()
			x = ram[42]
			if x >= x_prev : 
				Set = True 


		for i in range(25) :
			next_state_info= env.step(ACTION_LEFT)
			if rendering :
				env.render()
			# print (i,done)
			if next_state_info[3]['ale.lives'] < 6:
				Dead = True 
				break

		if Dead and Set :
			print ("Save")
		else :
			print ("Dont Save")

		env.close()

		return (Dead and Set)


	def checkOnEdgeLeft(self,ram):
		def inrange(pt,val,sign=">"):
			if sign == ">" :
				if val<=pt+4 and val >=pt :
					return True
			else : 
				if val>=pt-4 and val <=pt :
					return True

			return False
		y = ram[43]
		x = ram[42]
		if y==235 : 
			# top platform
			if inrange(66,x,"<") or inrange(104,x,"<") :
				return True

		elif y == 192:
			# mid platform
			if  inrange(60,x,"<") or inrange(124,x,"<"):
				return True

		return False

	def checkOnEdgeRight(self,ram):
		def inrange(pt,val,sign=">"):
			if sign == ">" :
				if val<=pt+4 and val >=pt :
					return True
			else : 
				if val>=pt-4 and val <=pt :
					return True

			return False
		y = ram[43]
		x = ram[42]
		if y==235 : 
			# top platform
			if inrange(50,x,">") or inrange(82,x,">") :
				return True

		elif y == 192:
			# mid platform
			if inrange(30,x,">") or inrange(94,x,">"):
				return True
			 
		return False


	def run_episodes(self):
		# model = pickle.load(open("./conceptTraining/concepts_/die_on_left/model_600_1200_0_5.sav", 'rb'))
		t = 0

		self.env = gym.make('MontezumaRevenge-ramDeterministic-v0')
		self.ale = self.env.unwrapped.ale
		if self.agent == "human":
			self.env.render()
			self.env.unwrapped.viewer.window.on_key_press = HumanAgent.handle_key_press_event
			self.env.unwrapped.viewer.window.on_key_release = HumanAgent.handle_key_release_event
		for i_episode in range(self.num_episodes):
			plan = self.set_starting_state()
			while True:


				if self.agent == "human":
					plan.append(HumanAgent.human_agent_action)
					next_state_info = self.env.step(HumanAgent.human_agent_action)
					self.env.render()
					time.sleep(0.1)
					ram = self.env.unwrapped._get_ram()
					# print (ram[42],ram[43])


					# edge = self.checkOnEdgeLeft(ram)
					# shouldBeSaved = False
					# if edge : 
					# 	shouldBeSaved = self.dieAndCheckEdge(plan,direction="left")

					# print ("Save:",shouldBeSaved)

					# x = np.expand_dims(ram, axis=0)
					# print (model.predict(x))
					# try :
					# 	print (model.predict_proba(x))
					# except : 
					# 	pass
					
					



					# print (ram[30] == 165)
					# print (plan)




					# edge = self.checkOnEdgeLeft(ram)
					# # print (edge )
					# shouldBeSaved = False
					# if edge : 
					# 	shouldBeSaved = self.dieAndCheckEdge(plan,direction="left")

					
					# if not shouldBeSaved :

					# 	redge = self.checkOnEdgeRight(ram)
					# 	# print (redge )
					# 	# shouldBeSaved = False
					# 	if redge : 
					# 		shouldBeSaved = self.dieAndCheckEdge(plan,direction="right")


					# print (shouldBeSaved)
					# if shouldBeSaved:
					# 	takeaction = ACTION_LEFT
					# 	if redge : 
					# 		takeaction = ACTION_RIGHT
						
					# 	print ("Taking Action", takeaction)
					# 	plan.append(takeaction)	
					# 	self.env.step(takeaction)
					# 	self.env.render()	




					# plan.append(ACTION_LEFT)
					# self.env.step(ACTION_LEFT)
					# self.env.render()

					# if self.game_state_condition_check("has_key", ram):
					# 	self.save_state()
					# 	self.sample_count += 1
					# 	self.save_plan(plan)
					# 	self.execute_plan(plan)
					# 	break
				

				elif self.agent == "robocop" :
					t = input()
					if t == 'w':
						action = 2
					elif t == 'a':
						action = 4
					elif t=='d':
						action = 3
					elif t == 's':
						action = 5
					# action = 4
					# self.all_actions.append()
					ram = self.env.unwrapped._get_ram()
					print ("Prev",ram[42],ram[43])

					next_state_info = self.env.step(action)
					self.env.render()
					ram = self.env.unwrapped._get_ram()
					print ("New",ram[42],ram[43])



				else:
					t +=1 
					action = self.env.action_space.sample()
					# print (ram[42],ram[43])
					self.all_actions.append(action)
					plan.append(action)
					ram = self.env.unwrapped._get_ram()



					# edge = self.checkOnEdgeLeft(ram)
					# shouldBeSaved = False
					# if edge : 
					# 	shouldBeSaved = self.dieAndCheckEdge(plan,direction="left")

					## Sample way of stroring --------------------------------------------------------------------------------

					# if shouldBeSaved :
					# 	sample_idx = self.sample_count
						
					# 	rgb = self.env.unwrapped.ale.getScreenRGB()
					# 	self.all_states.append(ram)
					# 	self.all_states_RGB.append(rgb)

					# 	print (os.getcwd())
					# 	path = "./cases/myconcepts/die_on_left/pos_"

					# 	image_rgb_file = path + "sample%d_RGB.b" % sample_idx
					# 	with open(image_rgb_file, 'wb') as fp:
					# 		pickle.dump(rgb, fp)
					# 	image_file = path + "sample%d_image.png" % sample_idx
					# 	plt.imsave(image_file, rgb)
					# 	plt.clf()
					# 	ram_file = path + "sample%d_RAM.b" % sample_idx
					# 	with open(ram_file, 'wb') as fp:
					# 		pickle.dump(ram, fp)

					# else : 

					# 	if t%3 == 0 :

					# 		sample_idx = self.sample_count
							
					# 		rgb = self.env.unwrapped.ale.getScreenRGB()
					# 		self.all_states.append(ram)
					# 		self.all_states_RGB.append(rgb)
					# 		path = "./cases/myconcepts/die_on_left/neg_"

					# 		image_rgb_file = path + "sample%d_RGB.b" % sample_idx
					# 		with open(image_rgb_file, 'wb') as fp:
					# 			pickle.dump(rgb, fp)
					# 		image_file = path + "sample%d_image.png" % sample_idx
					# 		plt.imsave(image_file, rgb)
					# 		plt.clf()
					# 		ram_file = path + "sample%d_RAM.b" % sample_idx
					# 		with open(ram_file, 'wb') as fp:
					# 			pickle.dump(ram, fp)





					next_state_info = self.env.step(action)
					self.env.render()

				
				self.save_state(plan)
				self.sample_count += 1
				if next_state_info[3]['ale.lives'] < 6:
					self.save_plan(plan,"./full_plans/")
					print ("Saved")
					print("Episode %d/%d finished" % (i_episode + 1, self.num_episodes))
					print("Lives left: %d" % next_state_info[3]['ale.lives'])
					break
		self.env.close()
		print("Total samples collected: %d" % self.sample_count)
		if self.agent != "human":
			self.condition_based_sampling()
			# Save the ground truth map
			with open('/tmp/ground_truth.yaml','w') as y_fd:
				yaml.dump(self.condition_to_sample_map, y_fd)
			# self.check_skull_logic2()

	def execute_plan(self, plan):
		print("executing plan")
		if self.agent == "human":
			self.env.reset()
			for action in plan:
				self.env.step(action)
				self.env.render()
				time.sleep(0.1)
		print("plan complete")

	@staticmethod
	def save_plan(plan,path="../config/humanAgentSamples/"):
		file_prefix = path
		state_by_sequence = file_prefix + "action_sequence.b"
		with open(state_by_sequence, 'wb') as fp:
			pickle.dump(plan, fp)

	def save_state(self, plan=None):
		sample_idx = self.sample_count
		ram = self.env.unwrapped._get_ram()
		rgb = self.env.unwrapped.ale.getScreenRGB()
		self.all_states.append(ram)
		self.all_states_RGB.append(rgb)
		file_prefix = "%s/samples/" % self.data_folder
		if self.agent == "human":
			file_prefix = "./config/humanAgentSamples/"
		image_rgb_file = file_prefix + "sample%d_RGB.b" % sample_idx
		with open(image_rgb_file, 'wb') as fp:
			pickle.dump(rgb, fp)
		image_file = file_prefix + "sample%d_image.png" % sample_idx
		plt.imsave(image_file, rgb)
		plt.clf()
		ram_file = file_prefix + "sample%d_RAM.b" % sample_idx
		with open(ram_file, 'wb') as fp:
			pickle.dump(ram, fp)
		if self.agent != "human":
			self.all_states_action_seq.append(plan)
			action_seq_file = file_prefix + "sample%d_action_seq.b" % sample_idx
			with open(action_seq_file, 'wb') as fp:
				pickle.dump(plan, fp)

	def check_skull_logic2(self):
		file_prefix = "/Users/anon/ProjectsData/blackBoxExp" \
					  "/samples/"
		for state_idx, state in enumerate(self.all_states):
			for condition in ["skull_on_left", "skull_on_right"]:
				if self.game_state_condition_check(condition, state, state_idx):
					self.env = gym.make('MontezumaRevenge-ramDeterministic-v0')
					self.env.seed(0)
					self.env.reset()
					action_sequence_file = file_prefix + "sample%d_action_seq.b" % state_idx
					with open(action_sequence_file, 'rb') as fp:
						action_sequence = pickle.load(fp)
					for action in action_sequence:
						self.env.step(action)
					if condition == "skull_on_left":
						self.env.step(4)
					else:
						self.env.step(3)
					lives = self.env.unwrapped._get_ram()[58]
					if lives == 4:
						print("agent dies in state %d" % state_idx)

	def check_restore(self, no_of_samples):
		for sample_idx in range(no_of_samples):
			file_prefix = "/Users/anon/ProjectsData/blackBoxExp" \
						  "/samples/"
			self.env = gym.make('MontezumaRevenge-ramDeterministic-v0')
			self.env.seed(0)
			self.env.reset()
			action_sequence_file = file_prefix + "sample%d_action_seq.b" % sample_idx
			with open(action_sequence_file, 'rb') as fp:
				action_sequence = pickle.load(fp)
			for action in action_sequence:
				self.env.step(action)
			restored_ram = self.env.unwrapped._get_ram()
			ram_file = file_prefix + "sample%d_RAM.b" % sample_idx
			with open(ram_file, "rb") as fp:
				stored_ram = pickle.load(fp)
			print("sample_idx checked: %d" % sample_idx)
			assert np.array_equal(stored_ram, restored_ram)






#  ========================================================================================================================
#  ========================================================================================================================
#  ================================================== LEVEL 3 =============================================================
#  ========================================================================================================================
#  ========================================================================================================================

GLOBAL_START_PLAN = []
with open("./full_plans/level3init.b","rb") as f :
	GLOBAL_START_PLAN = pickle.load(f)
# GLOBAL_START_PLAN.append(ACTION_DOWN)

GOAL_PLAN = []
with open("./full_plans/goalPlan.b","rb") as f :
	GOAL_PLAN = pickle.load(f)

# Create another env and run it till the start point for level 3 ----------------------------------------------------------------
def runTillEP3( render = False, random_starts = False, toIdx = None):
	global GLOBAL_START_PLAN
	plan = GLOBAL_START_PLAN
	env = gym.make('MontezumaRevenge-ramDeterministic-v0')
	env.seed(0)
	env.reset()

	# if not plan : 
	# 	with open("./full_plans/plantoLevel3Start.b","rb") as f :
	# 		plan = pickle.load(f)

	# print (plan)
	# souce :  plantoLevel3.b
	# splan = plan[:-150]
	# eplan = plan[:-50]

	# with open("./full_plans/plantoLevel3Start.b","wb") as f : 
	# 	pickle.dump(splan, f)  
	# till -160

	# with open("./full_plans/plantoLevel3End.b","wb") as f : 
	# 	pickle.dump(eplan, f)
	# till -120 

	for action in plan:
		env.step(action)
		if render : 
			time.sleep(0.0001)
			env.render()



	if random_starts :
		# print (len(GOAL_PLAN))
		toIdx = random.choice(range(len(GOAL_PLAN)))
		# print (toIdx)

		for i in range(toIdx) :
			env.step(GOAL_PLAN[i])

			if render : 
				env.render()
				time.sleep(0.0001)

	else : 
		# print (toIdx)
		for i in range(toIdx) :
			env.step(GOAL_PLAN[i])

			if render : 
				env.render()
				time.sleep(0.0001)


	if render : 
		env.close()
		# time.sleep(2)

	return env, toIdx

# misc condition : if Joe and Crab in certain range --------------------------------------------------------------------------------
def checkIsClear(env):

	rgb = env.unwrapped.ale.getScreenRGB()

	for sx in range(25):
		rgb[sx,:] = [0,0,0]

	# find crab .................................................... 
	wh = np.where(rgb == [92,186,92] )

	xc = int(np.mean(wh[0]))
	yc = int(np.mean(wh[1]))
	for i in range(len(wh[0])) :
		rgb[wh[0][i], wh[1][i]] = [	227,	38,	54]


	# find joe on rgb ..............................................

	wh = np.where(rgb == [200,72,72] )
	xj = int(np.mean(wh[0]))
	yj = int(np.mean(wh[1]))
	for i in range(len(wh[0])) :
		rgb[wh[0][i], wh[1][i]] = [	227,	38,	54]


	# print ("Joe", xj, yj)
	rgb[xj,yj] = [72, 200, 72]

	# print ("Crab", xc, yc)
	rgb[xc,yc] = [72, 200, 72]
	# print (rgb[xc,yc], rgb[xj,yj])
	# plt.imshow(rgb)
	# plt.show()


	# plt.clf()


	norm = np.sqrt((xj-xc)**2 + (yj-yc)**2)

	# print (norm)
	if norm > 23.5 : 
		return True 
	else :
		return False 

# Get XY positoin of crab and Joe from RGB hacks --------------------------------------------------------------------------------
def getCrabJoeXYonRGB(env):

	rgb = env.unwrapped.ale.getScreenRGB()

	for sx in range(25):
		rgb[sx,:] = [0,0,0]

	# find crab .................................................... 
	wh = np.where(rgb == [92,186,92] )

	xc = int(np.mean(wh[0]))
	yc = int(np.mean(wh[1]))

	# find joe on rgb ..............................................

	wh = np.where(rgb == [200,72,72] )
	xj = int(np.mean(wh[0]))
	yj = int(np.mean(wh[1]))

	return ((xc,yc),(xj,yj))

def isGoal(env):
	ram = env.unwrapped._get_ram()
	x,y = ram[42],ram[43]

	if x == 77 and y <= 180 :
		return True 
	return False 

def isDead(next_state_info) :
	return next_state_info[3]['ale.lives'] < 6

def level3Bounds(action, env):
	ram = env.unwrapped._get_ram()
	x,y = ram[42],ram[43]
	# print (x,y)
	if y < 150 and (action in (ACTION_UPLEFTFIRE, ACTION_UPRIGHTFIRE, ACTION_UPFIRE, ACTION_UP, ACTION_UPLEFT, ACTION_UPRIGHT)) :
		action = ACTION_NOOP 
	# print (x,y)

	return action 


import numpy as np 

# import copy 

# --------------------------------------------------------------------------------------------------------------------------------------
# Run the agent uptil the current point and then take "action" from this point, kind of like in mind to check what happens
# returns next state information from which we can see whether dead or not.
def nextStepResult(plan, action, toIdx):
	env, idx = runTillEP3(render=False, random_starts = False, toIdx = toIdx)

	for a in plan : 
		env.step(a)


	next_state_info = env.step(action)

	env.close()
	del env 

	return next_state_info



#  All conditions below ----------------------------------------------------------------------------------------------------------------
def isClearDownCrab(plan, oenv, toIdx):

	next_state_info = nextStepResult(plan, ACTION_DOWN, toIdx)

	ans = (not isDead(next_state_info))

	ram = oenv.unwrapped._get_ram()
	if (ram[42] == 77):  #to make sure that joe is on the ladder 

		if ans : 
			return "pos"
		else : 
			return "neg" 
	else :
		return False 



def onLadder(plan, oenv, toIdx):
	ram = oenv.unwrapped._get_ram()
	if ram[42] == 77 : # joe is on the ladder 
		return "pos" 
	return "neg"  

def onLadderTop(plan, oenv, toIdx):
	ram = oenv.unwrapped._get_ram()
	if onLadder(plan, oenv, toIdx) == "pos" : 
		if ram[43] >  240 : 
			return "pos"
	return "neg"

def onLadderBottom(plan, oenv, toIdx):
	ram = oenv.unwrapped._get_ram()
	if onLadder(plan, oenv, toIdx) == "pos" : 
		if ram[43] <  240 : 
			return "pos"
	return "neg"
	

def isLevelBottom(plan, oenv, toIdx):
	# >=130
	ram = oenv.unwrapped._get_ram()
	if onLadder(plan, oenv, toIdx) == "pos" : 
		if ram[43] <= 130 : 
			return "pos"
	return "neg"

def inAir(plan, oenv, toIdx):
	ram = oenv.unwrapped._get_ram()
	midair = (ram[30] == 165)

	if midair :
		return "pos"
	return "neg"

def onLeftPassage(plan, oenv, toIdx):
	ram = oenv.unwrapped._get_ram()
	if not (onLadder(plan, oenv,toIdx) == "pos") : 
		if ram[42] <  73 : 
			return "pos"
	return "neg"

def onRightPassage(plan, oenv, toIdx):
	ram = oenv.unwrapped._get_ram()
	if not (onLadder(plan, oenv, toIdx) == "pos") : 
		if ram[42] >  79 : 
			return "pos"
	return "neg"


def crabOnLeft(plan, oenv, toIdx):
	ram = oenv.unwrapped._get_ram()
	if ram[43] == 235 : 
		next_state_info = nextStepResult(plan, ACTION_LEFT, toIdx) 

		if isDead(next_state_info) :
			return "pos"

		return "neg"

	return False 

def crabOnRight(plan, oenv, toIdx):
	ram = oenv.unwrapped._get_ram()
	if ram[43] == 235 : 
		next_state_info = nextStepResult(plan, ACTION_RIGHT, toIdx) 

		if isDead(next_state_info) :
			return "pos"

		return "neg"

	return False 


def isClearUpCrab(plan, oenv, toIdx):
	next_state_info = nextStepResult(plan, ACTION_UP, toIdx)

	ans = (not isDead(next_state_info))

	ram = oenv.unwrapped._get_ram()
	if (ram[42] == 77):
		if ans : 
			return "pos"
		else : 
			return "neg" 
	else :
		return False 

def crabOnRelativeRight(plan, oenv, toIdx) :
	try :
		c,j = getCrabJoeXYonRGB(oenv)
		if c[1] > j[1] :
			return "pos"
	except : 
		pass

	return "neg" 

def crabOnRelativeLeft(plan, oenv, toIdx) :
	try : 
		c,j = getCrabJoeXYonRGB(oenv)
		if c[1] < j[1] :
			return "pos"
	except :
		pass

	return "neg" 
	 

def ladderBottomThreshold(plan, oenv, toIdx) :
	ram = oenv.unwrapped._get_ram()
	if isGoal(oenv) :
		return "pos"
	elif ram[42] == 77 :
		return "neg"

	return False  




GLOBAL_DUMP = []
def dump():
	global GLOBAL_DUMP 

	for tx in GLOBAL_DUMP : 
		if ".png" in tx[1] :
			plt.imsave(tx[1],tx[0])
			plt.clf()
		else : 
			with open(tx[1], 'wb') as fp : 
				pickle.dump(tx[0], fp)

	del GLOBAL_DUMP[:]

def speedDumping(x,path):
	global GLOBAL_DUMP

	if len(GLOBAL_DUMP) == 3000 : 
		dump()
		# empty contents from mem
		del GLOBAL_DUMP[:]

	else : 
		GLOBAL_DUMP.append((x,path))


def addToDump(x,path):
	global GLOBAL_DUMP

	GLOBAL_DUMP.append((x,path))


# Run each condition and save ------------------------------------------------------------------------------------------------
def runConditionAndSave(path, fnCondition, condition, episode_plan, env , toIdx,  posctr, negctr, ctr):
	
	path = path+condition+"/"

	cond = fnCondition(episode_plan, env, toIdx)

	ram = env.unwrapped._get_ram()
	rgb = env.unwrapped.ale.getScreenRGB()

	THRESH = 0.95
	if  cond:	
		if cond == "pos":
			ram_file = path + "pos_sample%d_RAM.b" % ctr
			image_file = path + "pos_sample%d_image.png" % ctr

			# if epRatio > THRESH : 	
			# 	with open(ram_file, 'wb') as fp:
			# 		pickle.dump(ram, fp)
			# 	plt.imsave(image_file, rgb)
			# 	plt.clf()
			# else : 
			addToDump(ram, ram_file)
			addToDump(rgb, image_file)

			posctr += 1

		if cond == "neg" :
			ram_file = path + "neg_sample%d_RAM.b" % ctr
			image_file = path + "neg_sample%d_image.png" % ctr
			# if epRatio > THRESH : 

				
			# 	with open(ram_file, 'wb') as fp:
			# 		pickle.dump(ram, fp)
				
				
			# 	plt.imsave(image_file, rgb)
			# 	plt.clf()
			
			# else : 
			addToDump(ram, ram_file)
			addToDump(rgb, image_file)

			negctr += 1

		ctr+=1
	else : 
		pass 

	return posctr, negctr, ctr

# Main code : ----------------------------------------------------------------------------------------------------------------
def randomAgentLevel3(path, conditions, episodes=4000, steps_per_episode= 60, render = False ):

	beginTime = time.time()
	
	for ep in range(episodes) :

		startTime = time.time()
		env, idx = runTillEP3(render=False, random_starts=True)
		if render : 
			env.render()

		episode_plan = []
		for i in range(steps_per_episode) :

			for condition in conditions.keys() :
				
				fnCondition = conditions[condition][0]


				conditions[condition][1], conditions[condition][2], conditions[condition][3] = runConditionAndSave( path, fnCondition, condition,episode_plan, env, idx,  conditions[condition][1], conditions[condition][2], conditions[condition][3])



			ram = env.unwrapped._get_ram()
			
			action = env.action_space.sample()

			# EXAMPLE PLAN .................

			# print("ep",ep," step",i," ", ram[42],ram[43])
			# for i in range(20) :
			# 	env.step(ACTION_NOOP)
			# 	env.render()
			# 	time.sleep(0.01)
			# for i in range(3) :
			# 	env.step(ACTION_DOWN)
			# 	env.render()
			# 	time.sleep(1)

			# for i in range(40) : 
			# 	env.step(ACTION_DOWN)
			# 	ram = env.unwrapped._get_ram()
			# 	print(ram[42],ram[43])
			# 	env.render()
			# 	time.sleep(1)



			if ram[43] > 249 : 
				action = ACTION_DOWN


			if isGoal(env) :
				break


			episode_plan.append(action)
			nextinfo = env.step(action)			


			if render : 
				env.render()
				time.sleep(0.1)

		
			if (isDead(nextinfo)) :
				break

			
				
		env.close()
		del env


		dump()

		print("Running Ep {:05d} / {:05d} | Time = {:05d} | Total Time = {:09d} | Avg. Time /ep = {:5.2f}".format(ep,episodes, int(time.time()-startTime), int(time.time() - beginTime), int((time.time() - beginTime) / (ep+1) ))) 
		for condition in conditions.keys() :
			print ("Condition = {} | Posctr = {:06d} | Negctr = {:06d}".format(condition.ljust(20), conditions[condition][1], conditions[condition][2]))
		print ("-"*30)
			
			

	print ("Finished in Time :", time.time()-beginTime)

	if render : 
		time.sleep(3)



def createDirs(path, conditions) :
	# "./cases/myconcepts/level3/"

	for condition in conditions : 
		os.mkdir(path+"/"+condition)
	print ("Concept Dirs created.")

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--level", type=int,
                    help="Choose Montezuma Level")
	args = parser.parse_args()


	if (args.level != 1) and (args.level !=4) : 
		print ("MUST PROVIDE argument LEVEL use --help")
		exit()


	# LEVEL 1 STUFF : ------------------------------------------------------------------------------------------------

	if args.level == 1 :

		conditions = ["on_rope", "on_ground_and_alive", "on_ladder1", "on_ladder2", "on_ladder3",
		              "skull_on_left", "skull_on_right", "has_key", "on_highest_platform", "on_middle_platform",
		              "door_on_right_position", "door_on_left_position", "wall_on_left", "wall_on_right", "key_on_right"
		              , "key_above", "key_on_left", "holding_on_to_the_rope_top", "holding_on_to_the_rope_bottom"]
		conditions += ["on_edge_left","on_edge_right"]
		data_folder = "./cases"
		print("Starting LEVEL 1")
		print ("CONCEPTS IN DIRECTORY : ", data_folder + "/concepts")
		sampler = Sampler(num_episodes=4000
		                  , _data_folder=data_folder
		                  , sampling_type="vanilla_random"
		                  , conditions=conditions
		                  , no_pos=100
		                  , no_neg=200
		                  , agent="random")

		sampler.create_directory_structure()
		print("Dir created")
		sampler.run_episodes()
		print("End")

		# sampler.check_restore(no_of_samples=1511)

	#  LEVEL 3 STUFF : ------------------------------------------------------------------------------------------------ 

	if args.level == 4 :
		print ("STARTING LEVEL 4") 
		path = "./cases/myconcepts/level4/"

		if os.path.exists (path):
			print ("PLEASE REMOVE THE PATH {} AFTER CHECKING".format(path))
			exit()

		os.mkdir(path)

		random.seed(path)

		print ("CONCEPTS IN DIRECTORY : ", path)

		conditions = {}
		# [fn, pos, neg, ctr] 

		# already done with random_travel

		conditions["isClearDownCrab"] 	= [isClearDownCrab,		 	0, 0, 0]
		conditions["onLadder"] 			= [onLadder,	 			0, 0, 0]
		conditions["onLadderTop"] 		= [onLadderTop, 			0, 0, 0]
		conditions["onLadderBottom"] 		= [onLadderBottom, 			0, 0, 0]
		# conditions["isLevelBottom"] 		= [isLevelBottom, 			0, 0, 0]
		conditions["inAir"] 				= [inAir, 					0, 0, 0]
		conditions["onLeftPassage"]		= [onLeftPassage, 			0, 0, 0]
		conditions["onRightPassage"] 		= [onRightPassage, 			0, 0, 0]
		conditions["crabOnLeft"] 			= [crabOnLeft,			    0, 0, 0]
		conditions["crabOnRight"] 		= [crabOnRight, 			0, 0, 0]



		conditions["isClearUpCrab"] 		= [isClearUpCrab, 			0, 0, 0]
		conditions["crabOnRelativeRight"] 	= [crabOnRelativeRight, 	0, 0, 0]
		conditions["crabOnRelativeLeft"] 	= [crabOnRelativeLeft, 		0, 0, 0]
		conditions["ladderBottomThreshold"] = [ladderBottomThreshold, 	0, 0, 0]



		createDirs(path, conditions.keys())
		randomAgentLevel3(path, conditions, episodes=4000, steps_per_episode=60, render=False)
























	# with open("./cases/myconcepts/level3RandomStarts/allModels/onLadder_600_1200_0_5.sav", "rb") as f :
	# 	model = pickle.load(f)



	# # GOALPLAN AND INIT PLAN GEN. 


	# env,_ = runTillEP3(render = False, toIdx=0)
	

	# for i in range(10) :
	# 	env.step(ACTION_NOOP)

	# 	ram = env.unwrapped._get_ram()
	# 	x = np.expand_dims(ram, axis=0)
	# 	print (model.predict(x), model.predict_proba(x))

	# 	env.render()
	# 	time.sleep(0.5)

	# for i in range(20) :
	# 	env.step(ACTION_DOWN)

	# 	ram = env.unwrapped._get_ram()
	# 	x = np.expand_dims(ram, axis=0)
	# 	print (model.predict(x), model.predict_proba(x))
		
	# 	env.render()
	# 	time.sleep(0.5)

	# with open("./full_plans/level3init.b", "wb") as fp : 
	# 	pickle.dump(GLOBAL_START_PLAN, fp)
	# with open("./full_plans/goalPlan.b", "wb") as fp : 
	# 	pickle.dump(nplan,fp)



	# time.sleep(2)
	# print ("Starting actual plan...")
	# for ix,action in enumerate(nplan) : 
	# 	env.step(action)
	# 	env.render()
	# 	time.sleep(0.1)
	# 	ram = env.unwrapped._get_ram()
	# 	print (ix, "     ", ram[42], ram[43])
