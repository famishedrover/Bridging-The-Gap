import gym
import gym_sokoban_mod_prec
#from .AbstractSimulator import AbstractSimulator
import copy

class SokobanFlipSimulator():
    def __init__(self):
        self.env = gym.make('Sokoban-mod-prec-v0')


    def test_action(self, state_seq, act):
        self.env.reset()
        done_flag = False
        for state_act in state_seq:
            #if not done_flag:
            s,_,done_flag,_ = self.env.step(state_act)
        #if done_flag is True:
        #    return False

        agent_pos_x, agent_pos_y = self.env.player_position
        res_state, reward, done, _ = self.env.step(act)
        if done is True and not reward > 0:
            return False
        return True

    def get_action_cost(self, state_seq, act):
        self.env.reset()

        for state_act in state_seq:
            self.env.step(state_act)


        res_state, reward, done, _ = self.env.step(act)

        return -1*reward
