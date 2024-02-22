import gym
import gym_sokoban_mod
from .AbstractSimulator import AbstractSimulator
import copy

class SokobanFlipSimulator():
    def __init__(self):
        self.env = gym.make('Sokoban-mod-v0')


    def test_action(self, state_seq, act):
        self.env.reset()

        for state_act in state_seq:
            self.env.step(state_act)

        agent_pos_x, agent_pos_y = self.env.player_position
        res_state, reward, done, _ = self.env.step(act)
        new_agent_pos_x, new_agent_pos_y = self.env.player_position
        if agent_pos_x != new_agent_pos_x or agent_pos_y != new_agent_pos_y:
            return True

        return False

    def get_action_cost(self, state_seq, act):
        self.env.reset()

        for state_act in state_seq:
            self.env.step(state_act)


        res_state, reward, done, _ = self.env.step(act)

        return -1*reward