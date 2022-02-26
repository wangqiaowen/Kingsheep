import random
from config import *

def get_class_name():
    return 'RandomPlayer'


class RandomPlayer:
    def __init__(self):
        self.name = "Random Player"
        self.uzh_shortname = "pplayer"

    def get_player_position(self,figure,field):
        x = [x for x in field if figure in x][0]
        return (field.index(x), x.index(figure))

    def move_sheep(self, p_num, p_state, p_time_remaining, field):
        return random.randint(0, 4) - 2, p_state

    def move_wolf(self, p_num, p_state, p_time_remaining, field):
        if p_num == 1:
            wolf_position = self.get_player_position(CELL_WOLF_1,field)
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            # print (sheep_position)

        return random.randint(0, 4) - 2, p_state
