# from config import *
import pickle
import pathlib


def get_class_name():
    return 'MyPlayer'


class MyPlayer():
    """Example class for a Kingsheep player"""

    def __init__(self):
        self.name = "My Player"
        self.uzh_shortname = "mplayer"

    def get_sheep_model(self):
        file_path = pathlib.Path(__file__).parent.absolute().joinpath('mplayer_sheep_model.sav')
        return pickle.load(open(file_path, 'rb'))

    def get_wolf_model(self):
        file_path = pathlib.Path(__file__).parent.absolute().joinpath('mplayer_wolf_model.sav')
        return pickle.load(open(file_path, 'rb'))

    def move_sheep(self, p_num, p_state, p_time_remaining, field):
        if 'sheep_model' not in p_state:
            p_state['sheep_model'] = self.get_sheep_model()

        sheep_model = p_state['sheep_model']

        X_sheep = []
        
        #preprocess field to get features, add to X_field
        #this code is largely copied from the Jupyter Notebook where the models were trained
        
        #create empty feature array for this game state
        game_features = []
        
        if p_num == 1:
            sheep = CELL_SHEEP_1
            wolf = CELL_WOLF_2
        else:
            sheep = CELL_SHEEP_2
            wolf = CELL_WOLF_1

        #get positions of sheep, wolf and food items
        food = []
        y=0
        for field_row in field:
            x = 0
            for item in field_row:
                if item == sheep:
                    sheep_position = (x,y)
                elif item == wolf:
                    wolf_position = (x,y)
                elif item == CELL_RHUBARB or item == CELL_GRASS:
                    food.append((x,y))
                x += 1
            y+=1
        
        #feature 1: determine if wolf within two steps up
        if sheep_position[1] - wolf_position[1] <= 2 and sheep_position[1] - wolf_position[1] > 0:
            s_feature1 = 1
        else:
            s_feature1 = 0
        game_features.append(s_feature1)
        
        #feature 2: determine if wolf within two steps down
        if sheep_position[1] - wolf_position[1] >= -2 and sheep_position[1] - wolf_position[1] < 0:
            s_feature2 = 1
        else:
            s_feature2 = 0
        game_features.append(s_feature2)
        
        #feature 3: determine if wolf within two steps left
        if sheep_position[0] - wolf_position[0] <= 2 and sheep_position[0] - wolf_position[0] > 0:
            s_feature3 = 1
        else:
            s_feature3 = 0
        game_features.append(s_feature3)
        
        #feature 4: determine if wolf within two steps right
        if sheep_position[0] - wolf_position[0] >= -2 and sheep_position[0] - wolf_position[0] < 0:
            s_feature4 = 1
        else:
            s_feature4 = 0
        game_features.append(s_feature4)
        
        s_feature5 = 0
        s_feature6 = 0
        s_feature7 = 0
        s_feature8 = 0
        
        for food_item in food:
            #feature 5: determine if food within two steps up
            if sheep_position[1] - food_item[1] <= 2 and sheep_position[1] - food_item[1] > 0:
                s_feature5 = 1
            
            #feature 6: determine if food within two steps down
            if sheep_position[1] - food_item[1] >= -2 and sheep_position[1] - food_item[1] < 0:
                s_feature6 = 1
            
            #feature 7: determine if food within two steps left    
            if sheep_position[0] - wolf_position[0] <= 2 and sheep_position[0] - food_item[0] > 0:
                s_feature7 = 1
            
            #feature 8: determine if food within two steps right
            if sheep_position[0] - wolf_position[0] >= -2 and sheep_position[0] - food_item[0] < 0:
                s_feature8 = 1
            
        game_features.append(s_feature5)
        game_features.append(s_feature6)
        game_features.append(s_feature7)
        game_features.append(s_feature8)
        
        #add features and move to X_sheep and Y_sheep
        X_sheep.append(game_features)

        result = sheep_model.predict(X_sheep)

        return result, p_state

    def move_wolf(self, p_num, p_state, p_time_remaining, field):
        if 'wolf_model' not in p_state:
            p_state['wolf_model'] = self.get_wolf_model()

        wolf_model = p_state['wolf_model']

        #create empty feature array for this game state
        game_features = []
        X_wolf = []

        if p_num == 1:
            sheep = CELL_SHEEP_2
            wolf = CELL_WOLF_1
        else:
            sheep = CELL_SHEEP_1
            wolf = CELL_WOLF_2
        
        #get positions of sheep, wolf and food items
        y=0
        for field_row in field:
            x = 0
            for item in field_row:
                if item == sheep:
                    sheep_position = (x,y)
                elif item == wolf:
                    wolf_position = (x,y)
                x += 1
            y+=1
        
        #feature 1: determine if the sheep is above the wolf
        if wolf_position[1] - sheep_position[1] > 0:
            w_feature1 = 1
        else:
            w_feature1 = 0
        game_features.append(w_feature1)

        #feature 2: determine if the sheep is above the wolf
        if wolf_position[1] - sheep_position[1] > 0:
            w_feature2 = 1
        else:
            w_feature2 = 0
        game_features.append(w_feature2)
            
        #feature 3: determine if the sheep is above the wolf
        if wolf_position[1] - sheep_position[1] > 0:
            w_feature3 = 1
        else:
            w_feature3 = 0
        game_features.append(w_feature3)
            
        #feature 4: determine if the sheep is above the wolf
        if wolf_position[1] - sheep_position[1] > 0:
            w_feature4 = 1
        else:
            w_feature4 = 0
        game_features.append(w_feature4)
        
        #add features and move to X_wolf and Y_wolf
        X_wolf.append(game_features)

        result = wolf_model.predict(X_wolf)

        return result, p_state