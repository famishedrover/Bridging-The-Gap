import gym
import numpy as np
from matplotlib import pyplot as plt
import random
import pickle


class Sampler:
    def __init__(self, num_episodes=5, sampling_type="vanilla_random"):
        self.num_episodes = num_episodes
        self.sampling_type = sampling_type
        self.all_states = []
        self.all_screen_RGB = []

    def get_specific_states(self, no_pos, no_neg):
        # for ladder
        pos_states_indices = []
        for idx, state in enumerate(self.all_states):
            byte_val = state[30]
            if byte_val == 144 or byte_val == 123:
                # the player is on the rope.
                pos_states_indices.append(idx)

        neg_states_indices = list(set(range(len(self.all_states))) - set(pos_states_indices))

        pos_samples = self.get_samples(pos_states_indices, no_pos)
        neg_samples = self.get_samples(neg_states_indices, no_neg)

        pickle.dump([pos_samples, neg_samples], open('ladder.b', 'wb'))
        # t1 = pickle.load(open("ladder.b", "rb"))
        return pos_samples, neg_samples

    def get_samples(self, indices, no):
        sampled_indices = indices
        if no < len(indices):
            sampled_indices = random.sample(indices, no)
        samples = []
        for idx in sampled_indices:
            samples.append([self.all_states[idx], self.all_screen_RGB[idx]])
        return samples

    def set_starting_state(self, env, episode_number):
        if self.sampling_type == "vanilla_random":
            return env.reset()
        elif self.sampling_type == "random_start_state":
            if episode_number == 0:
                return env.reset()
            else:
                s_idx = np.random.choice(np.arange(len(self.all_states)))
                s_p = self.all_states[s_idx][:-1]
                s_p_a = self.all_states[s_idx][-1]
                env.unwrapped.restore_full_state(s_p)
                return env.step(s_p_a)[0]

    def run_episodes(self):
        env = gym.make('MontezumaRevenge-ram-v0')
        for i_episode in range(self.num_episodes):
            self.set_starting_state(env, i_episode)
            if env.unwrapped.ale.game_over():
                break
            while True:
                action = env.action_space.sample()
                done = env.step(action)[2]
                self.all_states.append(env.unwrapped._get_ram())
                self.all_screen_RGB.append(env.unwrapped.ale.getScreenRGB())
                if done:
                    print("Episode %d/%d finished" % (i_episode + 1, self.num_episodes))
                    break
        env.close()


if __name__ == "__main__":
    sampler = Sampler()
    sampler.run_episodes()
    sampler.get_specific_states()