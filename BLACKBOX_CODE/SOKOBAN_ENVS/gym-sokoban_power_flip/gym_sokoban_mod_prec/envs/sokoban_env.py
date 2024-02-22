import gym
from gym.utils import seeding
from gym.spaces.discrete import Discrete
from gym.spaces import Box
from .room_utils import generate_room
from .render_utils import room_to_rgb, room_to_tiny_world_rgb
import numpy as np
import copy


class SokobanEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array', 'tiny_human', 'tiny_rgb_array', 'raw']
    }

    def __init__(self,
                 dim_room=(10, 10),
                 max_steps=120,
                 num_boxes=4,
                 num_gen_steps=None,
                 reset=True):

        # General Configuration
        self.dim_room = dim_room
        if num_gen_steps == None:
            self.num_gen_steps = int(1.7 * (dim_room[0] + dim_room[1]))
        else:
            self.num_gen_steps = num_gen_steps

        self.num_boxes = num_boxes
        self.boxes_on_target = 0

        self.box_x = 7
        self.box_y = 3


        self.max_reward = 500


        # Penalties and Rewards
        self.penalty_for_step = -1
        self.penalty_box_off_target = -1
        self.reward_box_on_target = 1#000
        self.reward_finished = 100#000
        self.reward_last = 0

        self.switch_state = False
        # Other Settings
        self.viewer = None
        self.max_steps = 200 #max_steps
        self.action_space = Discrete(len(ACTION_LOOKUP))
        screen_height, screen_width = (dim_room[0] * 16, dim_room[1] * 16)
        self.observation_space = Box(low=0, high=255, shape=(screen_height, screen_width, 3), dtype=np.uint8)
        
        if reset:
            # Initialize Room
            _ = self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action, observation_mode='rgb_array'):
        assert action in ACTION_LOOKUP
        assert observation_mode in ['rgb_array', 'tiny_rgb_array', 'raw']
        #print("Executing actions",action)
        self.num_env_steps += 1

        old_player_pos = self.player_position.copy()

        self.new_box_position = None
        self.old_box_position = None

        moved_box = False

        if action == 0:
            moved_player = False


        # All push actions are in the range of [0, 3]
        elif action < 5:
            moved_player, moved_box = self._push(action)

        else:
            moved_player = self._move(action)

        if moved_player and old_player_pos[0] == 8 and old_player_pos[1] == 6:
               self.switch_state = not self.switch_state
               if not self.switch_state:
                    self.room_state[8][6] = 7
       
        #print ("new box positions",self.box_x, self.box_y)
        self._calc_reward(action)

        if moved_box:
            dist = abs(3 - self.box_x) + abs(3 - self.box_y)
            #if dist != 0:
            #    self.reward_last += (self.max_reward/dist)
            #else:
            #    self.reward_last += self.max_reward
            self.reward_last += 1 -1*(dist/10)
       
        if not self.switch_state:
           self.reward_last += -1* (abs(8-self.player_position[0])+abs(6-self.player_position[1]))

        
        done = self._check_if_done(action, moved_box)

        # Convert the observation to RGB frame
        observation = self.render(mode=observation_mode)

        info = {
            "action.name": ACTION_LOOKUP[action],
            "action.moved_player": moved_player,
            "action.moved_box": moved_box,
        }
        if done:
            info["maxsteps_used"] = self._check_if_maxsteps()
            info["all_boxes_on_target"] = self._check_if_all_boxes_on_target()

        #print ("room state", self.room_state)
        return observation, self.reward_last, done, info

    def _push(self, action):
        """
        Perform a push, if a box is adjacent in the right direction.
        If no box, can be pushed, try to move.
        :param action:
        :return: Boolean, indicating a change of the room's state
        """
        change = CHANGE_COORDINATES[(action - 1) % 4]
        new_position = self.player_position + change
        current_position = self.player_position.copy()

        # No push, if the push would get the box out of the room's grid
        new_box_position = new_position + change
        if new_box_position[0] >= self.room_state.shape[0] \
                or new_box_position[1] >= self.room_state.shape[1]:
            return False, False


        can_push_box = self.room_state[new_position[0], new_position[1]] in [3, 4]
        can_push_box &= self.room_state[new_box_position[0], new_box_position[1]] in [1, 2]
        #can_push_box &= (7 not in self.room_state)
        can_push_box &= self.switch_state
        if can_push_box:

            self.new_box_position = tuple(new_box_position)
            self.old_box_position = tuple(new_position)
            
            # Move Player
            self.player_position = new_position
            self.room_state[(new_position[0], new_position[1])] = 5
            self.room_state[current_position[0], current_position[1]] = \
                self.room_fixed[current_position[0], current_position[1]]

            # Move Box
            box_type = 4
            if self.room_fixed[new_box_position[0], new_box_position[1]] == 2:
                box_type = 3
            self.room_state[new_box_position[0], new_box_position[1]] = box_type
            self.box_x = new_box_position[0]
            self.box_y = new_box_position[1]
            return True, True

        # Try to move if no box to push, available
        else:
            #return self._move(action), False
            return False, False

    def _move(self, action):
        """
        Moves the player to the next field, if it is not occupied.
        :param action:
        :return: Boolean, indicating a change of the room's state
        """
        change = CHANGE_COORDINATES[(action - 1) % 4]
        new_position = self.player_position + change
        current_position = self.player_position.copy()

        # Move player if the field in the moving direction is either
        # an empty field or an empty box target.
        if self.room_state[new_position[0], new_position[1]] in [1, 2, 7, 8]:
            self.player_position = new_position
            self.room_state[(new_position[0], new_position[1])] = 5
            self.room_state[current_position[0], current_position[1]] = \
                self.room_fixed[current_position[0], current_position[1]]
            return True

        return False

    def _calc_reward(self, action):
        """
        Calculate Reward Based on
        :return:
        """
        # Every step a small penalty is given, This ensures
        # that short solutions have a higher reward.
        self.reward_last = self.penalty_for_step
        #print ("self switch state", self.switch_state, action)
        if not self.switch_state and action in [1,2,3,4]:
        #if action in [1,2,3,4]:
        #    change = CHANGE_COORDINATES[(action - 1) % 4]
        #    new_position = self.player_position + change
        #    current_position = self.player_position.copy()

        #    # No push, if the push would get the box out of the room's grid
        #    new_box_position = new_position + change
        #    if not (new_box_position[0] >= self.room_state.shape[0] \
        #        or new_box_position[1] >= self.room_state.shape[1]):
        #        can_push_box = self.room_state[new_position[0], new_position[1]] in [3, 4]
        #        can_push_box &= self.room_state[new_box_position[0], new_box_position[1]] in [1, 2]
        #        can_push_box &= self.switch_state
        #        if not can_push_box:
            self.reward_last += -100 


        # count boxes off or on the target
        empty_targets = self.room_state == 2
        player_on_target = (self.room_fixed == 2) & (self.room_state == 5)
        total_targets = empty_targets | player_on_target

        current_boxes_on_target = self.num_boxes - \
                                  np.where(total_targets)[0].shape[0]

        # Add the reward if a box is pushed on the target and give a
        # penalty if a box is pushed off the target.
        #if current_boxes_on_target > self.boxes_on_target:
        #    self.reward_last += self.reward_box_on_target
        #elif current_boxes_on_target < self.boxes_on_target:
        #    self.reward_last += self.penalty_box_off_target
        
        game_won = self._check_if_all_boxes_on_target()        
        if game_won:
            self.reward_last += self.reward_finished
            print ("Goal reached....") 
        self.boxes_on_target = current_boxes_on_target

        #print ("box_x",self.box_x)
        #print ("box_y",self.box_y)


    def _check_if_done(self, action, moved_box):
        # Check if the game is over either through reaching the maximum number
        # of available steps or by pushing all boxes on the targets.
        if action in [1,2,3,4]:
#            change = CHANGE_COORDINATES[(action - 1) % 4]
#            new_position = self.player_position + change
#            current_position = self.player_position.copy()
#
#            # No push, if the push would get the box out of the room's grid
#            new_box_position = new_position + change
#            if not (new_box_position[0] >= self.room_state.shape[0] \
#                or new_box_position[1] >= self.room_state.shape[1]):
#            #if not self.switch_state:
#                    can_push_box = self.room_state[new_position[0], new_position[1]] in [3, 4]
#                    can_push_box &= self.room_state[new_box_position[0], new_box_position[1]] in [1, 2]
#                    can_push_box &= self.switch_state
#                    if not can_push_box:
            if not self.switch_state or list(self.player_position) == [8,6]:
                print ("Done...", self.player_position)
                return True        
        return self._check_if_all_boxes_on_target() or self._check_if_maxsteps()

    def _check_if_all_boxes_on_target(self):
        empty_targets = self.room_state == 2
        player_hiding_target = (self.room_fixed == 2) & (self.room_state == 5)
        are_all_boxes_on_targets = np.where(empty_targets | player_hiding_target)[0].shape[0] == 0
        return are_all_boxes_on_targets

    def _check_if_maxsteps(self):
        return (self.max_steps == self.num_env_steps)

    def reset(self, second_player=False, render_mode='rgb_array'):
        try:
            self.room_fixed, self.room_state, self.box_mapping = generate_room(
                dim=self.dim_room,
                num_steps=self.num_gen_steps,
                num_boxes=self.num_boxes,
                second_player=second_player
            )
        except (RuntimeError, RuntimeWarning) as e:
            print("[SOKOBAN] Runtime Error/Warning: {}".format(e))
            print("[SOKOBAN] Retry . . .")
            return self.reset(second_player=second_player)

        self.player_position = np.argwhere(self.room_state == 5)[0]
        self.num_env_steps = 0
        self.reward_last = 0
        self.boxes_on_target = 0
        self.box_x = 7
        self.box_y = 3


        self.switch_state = False
        starting_observation = self.render(render_mode)
        return starting_observation

    def render(self, mode='human', close=None, scale=1):
        assert mode in RENDERING_MODES

        img = self.get_image(mode, scale)

        if 'rgb_array' in mode:
            return img

        elif 'human' in mode:
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
            return self.viewer.isopen

        elif 'raw' in mode:
            arr_walls = (self.room_fixed == 0).view(np.int8)
            arr_goals = (self.room_fixed == 2).view(np.int8)
            arr_boxes = ((self.room_state == 4) + (self.room_state == 3)).view(np.int8)
            arr_player = (self.room_state == 5).view(np.int8)

            return arr_walls, arr_goals, arr_boxes, arr_player

        else:
            super(SokobanEnv, self).render(mode=mode)  # just raise an exception

    def get_image(self, mode, scale=1):
        
        if mode.startswith('tiny_'):
            img = room_to_tiny_world_rgb(self.room_state, self.room_fixed, scale=scale)
        else:
            img = room_to_rgb(self.room_state, self.room_fixed)

        return img

    def close(self):
        if self.viewer is not None:
            self.viewer.close()

    def set_maxsteps(self, num_steps):
        self.max_steps = num_steps

    def get_action_lookup(self):
        return ACTION_LOOKUP

    def get_action_meanings(self):
        return ACTION_LOOKUP


ACTION_LOOKUP = {
    0: 'no operation',
    1: 'push up',
    2: 'push down',
    3: 'push left',
    4: 'push right',
    5: 'move up',
    6: 'move down',
    7: 'move left',
    8: 'move right',
}

# Moves are mapped to coordinate changes as follows
# 0: Move up
# 1: Move down
# 2: Move left
# 3: Move right
CHANGE_COORDINATES = {
    0: (-1, 0),
    1: (1, 0),
    2: (0, -1),
    3: (0, 1)
}

RENDERING_MODES = ['rgb_array', 'human', 'tiny_rgb_array', 'tiny_human', 'raw']
