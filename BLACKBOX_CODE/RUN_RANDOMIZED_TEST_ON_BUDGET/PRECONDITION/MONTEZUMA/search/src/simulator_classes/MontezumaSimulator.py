import time
import gym
from matplotlib import pyplot as plt


class MontezumaSimulator():
    def __init__(self):
        self.env = gym.make('MontezumaRevenge-ramDeterministic-v0')
    
    def check_failure(self, old_x, old_y):
        # Failure constitute death or no change in X and Y position
        #time.sleep(2)
        # self.env.step(0)
        # self.env.step(0)
        # self.env.step(0)
        # self.env.step(0)
        # time.sleep(0.01)


        # First check if the agent is in air

        if self.env.unwrapped._get_ram()[86] != 255 or self.env.unwrapped._get_ram()[88] !=0:
        # The perform 10 noop actions
            for i in range(10):
                self.env.step(0)
                time.sleep(0.001)

        if self.env.unwrapped._get_ram()[86] != 255 or self.env.unwrapped._get_ram()[88] != 0:
            return True
        current_lives = self.env.unwrapped._get_ram()[58]



        x_pos = self.env.unwrapped._get_ram()[42]
        y_pos = self.env.unwrapped._get_ram()[43]



        #print ("Player lives",self.env.unwrapped._get_ram()[58])



        if current_lives < 5:
            return True



        x_diff = int(x_pos)- int(old_x)
        y_diff = int(y_pos) - int(old_y)
        if abs(x_diff) <= 2 and abs(y_diff) <= 2:
            return True
        # print ("Old_x", old_x)
        # print ("Old_y", old_y)
        # print ("new_x", x_pos)
        # print ("new_y", y_pos)
        # print (x_diff, y_diff)
        return False

    def test_action(self, state_act_seq, act):
        # Assume states are saved as action sequences
        self.env.seed(0)
        self.env.reset()

        for state_act in state_act_seq:
            self.env.step(state_act)
        rgb = self.env.unwrapped.ale.getScreenRGB()

        image_file = "/tmp/test_image_pre.png"
        plt.imsave(image_file, rgb)
        plt.clf()
        #print ("Player lives",self.env.unwrapped._get_ram()[58])

        x_pos = self.env.unwrapped._get_ram()[42]
        y_pos = self.env.unwrapped._get_ram()[43]

        # Just skip states that are already in air
        if self.env.unwrapped._get_ram()[86] != 255 or self.env.unwrapped._get_ram()[88] != 0:
            return False
        # Test action
        self.env.step(act)
        self.env.step(0)
        self.env.step(0)
        rgb = self.env.unwrapped.ale.getScreenRGB()
        image_file = "/tmp/test_image.png"
        plt.imsave(image_file, rgb)
        plt.clf()
        #time.sleep(1)
        return not self.check_failure(x_pos, y_pos)

    def get_states(self, state_act_seq):
        self.env.reset()
        for state_act in state_act_seq:
            self.env.step(state_act)
        return self.env.unwrapped._get_ram()
