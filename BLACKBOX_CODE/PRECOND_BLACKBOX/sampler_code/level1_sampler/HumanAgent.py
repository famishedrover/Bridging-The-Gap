"""
control Montezuma with a human agent.
"""

KEY_SPACE = ord(' ')  # 32
KEY_A = ord('a')  # 97
KEY_W = ord('w')  # 119
KEY_D = ord('d')  # 100
KEY_S = ord('s')  # 115
KEY_P = ord('p')  # 112
KEY_LEFT = 65361
KEY_UP = 65362
KEY_RIGHT = 65363
KEY_DOWN = 65364
KEY_ESC = 65307
KEY_CAPTURE = 99

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

key_printscreen_triggered = False

key_space_pressed = False
key_left_pressed = False
key_up_pressed = False
key_right_pressed = False
key_down_pressed = False

capture_all_transitions = True


class HumanAgent:
    human_agent_action = ACTION_NOOP
    human_sets_pause = False
    exec_next_action = False

    @staticmethod
    def update_human_agent_action():
        """
        Update the human agent action according to the pressed keys.
        """

        if key_up_pressed and key_left_pressed and key_space_pressed:
            HumanAgent.human_agent_action = ACTION_UPLEFTFIRE
            return

        if key_up_pressed and key_right_pressed and key_space_pressed:
            HumanAgent.human_agent_action = ACTION_UPRIGHTFIRE
            return

        if key_down_pressed and key_left_pressed and key_space_pressed:
            HumanAgent.human_agent_action = ACTION_DOWNLEFTFIRE
            return

        if key_down_pressed and key_right_pressed and key_space_pressed:
            HumanAgent.human_agent_action = ACTION_DOWNRIGHTFIRE
            return

        if key_up_pressed and key_left_pressed:
            HumanAgent.human_agent_action = ACTION_UPLEFT
            return

        if key_up_pressed and key_right_pressed:
            HumanAgent.human_agent_action = ACTION_UPRIGHT
            return

        if key_down_pressed and key_left_pressed:
            HumanAgent.human_agent_action = ACTION_DOWNLEFT
            return

        if key_down_pressed and key_right_pressed:
            HumanAgent.human_agent_action = ACTION_DOWNRIGHT
            return

        if key_up_pressed and key_space_pressed:
            HumanAgent.human_agent_action = ACTION_UPFIRE
            return

        if key_down_pressed and key_space_pressed:
            HumanAgent.human_agent_action = ACTION_DOWNFIRE
            return

        if key_left_pressed and key_space_pressed:
            HumanAgent.human_agent_action = ACTION_LEFTFIRE
            return

        if key_right_pressed and key_space_pressed:
            HumanAgent.human_agent_action = ACTION_RIGHTFIRE
            return

        if key_up_pressed:
            HumanAgent.human_agent_action = ACTION_UP
            return

        if key_down_pressed:
            HumanAgent.human_agent_action = ACTION_DOWN
            return

        if key_left_pressed:
            HumanAgent.human_agent_action = ACTION_LEFT
            return

        if key_right_pressed:
            HumanAgent.human_agent_action = ACTION_RIGHT
            return

        if key_space_pressed:
            HumanAgent.human_agent_action = ACTION_FIRE
            return

        HumanAgent.human_agent_action = ACTION_NOOP

    @staticmethod
    def handle_key_press_event(key, mod):
        """
        Key press event handler.
        """

        global key_space_pressed
        global key_left_pressed
        global key_up_pressed
        global key_right_pressed
        global key_down_pressed

        # game environment control
        if key == KEY_ESC:
            HumanAgent.human_sets_pause = not HumanAgent.human_sets_pause
            return

        # agent control
        if key == KEY_SPACE:
            key_space_pressed = True

        if key == KEY_W or key == KEY_UP:
            key_up_pressed = True

        if key == KEY_S or key == KEY_DOWN:
            key_down_pressed = True

        if key == KEY_A or key == KEY_LEFT:
            key_left_pressed = True

        if key == KEY_D or key == KEY_RIGHT:
            key_right_pressed = True

        HumanAgent.exec_next_action = True
        HumanAgent.update_human_agent_action()

    @staticmethod
    def handle_key_release_event(key, mod):
        """
        Key release event handler.
        """

        global key_space_pressed
        global key_left_pressed
        global key_up_pressed
        global key_right_pressed
        global key_down_pressed

        # agent control
        if key == KEY_SPACE:
            key_space_pressed = False

        if key == KEY_W or key == KEY_UP:
            key_up_pressed = False

        if key == KEY_S or key == KEY_DOWN:
            key_down_pressed = False

        if key == KEY_A or key == KEY_LEFT:
            key_left_pressed = False

        if key == KEY_D or key == KEY_RIGHT:
            key_right_pressed = False

        HumanAgent.update_human_agent_action()

