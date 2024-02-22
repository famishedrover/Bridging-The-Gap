import pickle
from matplotlib import pyplot as plt
import numpy as np
if __name__ == "__main__":
    rgb = pickle.load(open("/Users/anon/ProjectsData/blackBoxExp/concepts/skull_on_left/pos_sample3322_RGB.b", 'rb'))
    joe_pos = np.array(np.where(rgb == [228, 111, 111]))[0:2, 0]
    skull_pos = np.array(np.where(rgb[100:] == [236, 236, 236]))[0:2, 0] + np.array([100, 0])
    print(joe_pos[1], skull_pos[1])
    plt.imshow(rgb)
    plt.show()
    # print(rgb)
