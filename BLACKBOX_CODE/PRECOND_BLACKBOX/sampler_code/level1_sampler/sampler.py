import gym
import numpy as np
from matplotlib import pyplot as plt
import random
import pickle
from shutil import copy2
from HumanAgent import *
import time
import shutil
import os
import yaml

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
        return False

    def condition_based_sampling(self):
        for condition in self.conditions:
            pos_states_indices = []
            for state_idx, state in enumerate(self.all_states):
                if self.game_state_condition_check(condition, state, state_idx):
                    pos_states_indices.append(state_idx)
                    self.condition_to_sample_map[condition].add(state_idx)
            assert len(self.all_states) == self.sample_count
            #neg_states_indices = list(set(range(self.sample_count)) - set(pos_states_indices))
            print("for condition: %s, no of pos samples found: %d" %(condition, len(pos_states_indices)))
            #self.save_samples(condition, "pos", pos_states_indices, self.no_pos)
            #self.save_samples(condition, "neg", neg_states_indices, self.no_neg)

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
            file_prefix = "../config/humanAgentSamples/"
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
        else:
            self.env.reset()
            return []

    def run_episodes(self):
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
                    if self.game_state_condition_check("has_key", ram):
                        self.save_state()
                        self.sample_count += 1
                        self.save_plan(plan)
                        self.execute_plan(plan)
                        break
                else:
                    action = self.env.action_space.sample()
                    self.all_actions.append(action)
                    plan.append(action)
                    next_state_info = self.env.step(action)
                self.save_state(plan)
                self.sample_count += 1
                if next_state_info[3]['ale.lives'] < 6:
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
    def save_plan(plan):
        file_prefix = "../config/humanAgentSamples/"
        state_by_sequence = file_prefix + "action_sequence.b"
        with open(state_by_sequence, 'wb') as fp:
            pickle.dump(plan, fp)

    def save_state(self, plan=None):
        sample_idx = self.sample_count
        ram = self.env.unwrapped._get_ram()
        rgb = self.env.unwrapped.ale.getScreenRGB()
        self.all_states.append(ram)
        self.all_states_RGB.append(rgb)


        # Make the directory for the sample_count

        sample_dir = "%s/samples/" % self.data_folder + "%d/" % sample_idx
        os.mkdir(sample_dir)

        if self.agent == "human":
            file_prefix = "../config/humanAgentSamples/"

        image_rgb_file =  sample_dir + "sample_RGB.b"
        with open(image_rgb_file, 'wb') as fp:
            pickle.dump(rgb, fp)

        image_file = sample_dir + "sample_image.png" 
        plt.imsave(image_file, rgb)
        plt.clf()
        
        ram_file = sample_dir + "sample_RAM.b"
        with open(ram_file, 'wb') as fp:
            pickle.dump(ram, fp)
        
        if self.agent != "human":
            self.all_states_action_seq.append(plan)
            action_seq_file = sample_dir + "sample_action_seq.b"
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


if __name__ == "__main__":
    conditions = ["on_rope", "on_ground_and_alive", "on_ladder1", "on_ladder2", "on_ladder3",
                  "skull_on_left", "skull_on_right", "has_key", "on_highest_platform", "on_middle_platform",
                  "door_on_right_position", "door_on_left_position", "wall_on_left", "wall_on_right", "key_on_right"
                  , "key_above", "key_on_left", "holding_on_to_the_rope_top", "holding_on_to_the_rope_bottom"]
    data_folder = "/tmp/ProjectsData/blackBoxExp"
    sampler = Sampler(num_episodes=1000
                      , _data_folder=data_folder
                      , sampling_type="random_restart_from_plan"
                      , conditions=conditions
                      , no_pos=100
                      , no_neg=200
                      , agent="random")
    sampler.create_directory_structure()
    sampler.run_episodes()
    # sampler.check_restore(no_of_samples=1511)
