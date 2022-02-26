
from config import *
import pickle
import numpy as np
import random

def get_class_name():
    return 'SheepTheVictim'


class SheepTheVictim():

    def __init__(self):
        self.name = "SheepTheVictim"
        self.uzh_shortname = "qiawan"

    def get_sheep_model(self):  
        return pickle.load(open('qiawan_sheep_model.sav','rb'))

    def get_wolf_model(self): 
        return pickle.load(open('qiawan_wolf_model.sav','rb'))

    def is_wolf_nearby(sheep_position, wolf_position):

        if (sheep_position[1] - wolf_position[1] <= 2 and sheep_position[1] - wolf_position[1] > 0) \
        or (sheep_position[1] - wolf_position[1] >= -2 and sheep_position[1] - wolf_position[1] < 0) \
        or (sheep_position[0] - wolf_position[0] <= 2 and sheep_position[0] - wolf_position[0] > 0) \
        or (sheep_position[0] - wolf_position[0] >= -2 and sheep_position[0] - wolf_position[0] < 0) :
            return True

    def new_sheep_position(result, sheep_position):

        if result[0] == -2:
            return ((sheep_position[0]-1),sheep_position[1])
        elif result[0] == 2:
            return ((sheep_position[0]+1),sheep_position[1])
        elif result[0] == -1:
            return (sheep_position[0],(sheep_position[1]-1))
        elif result[0] == 1:
            return (sheep_position[0],(sheep_position[1]+1))
        else: 
            return sheep_position

    def new_wolf_position(result, wolf_position):

        if result[0] == -2:
            return ((wolf_position[0]-1),wolf_position[1])
        elif result[0] == 2:
            return ((wolf_position[0]+1),wolf_position[1])
        elif result[0] == -1:
            return (wolf_position[0],(wolf_position[1]-1))
        elif result[0] == 1:
            return (wolf_position[0],(wolf_position[1]+1))
        else: 
            return wolf_position

    def manhattan_D(x,y):

        return sum(map(lambda i,j: abs(i-j),x,y))

    def fence_surrounded(sheep_position, fence):
        right = (sheep_position[0]+1,sheep_position[1])
        left = (sheep_position[0]-1,sheep_position[1])
        above = (sheep_position[0],sheep_position[1]-1)
        below = (sheep_position[0],sheep_position[1]+1)

        if right in fence and above in fence:
            return True
        elif right in fence and below in fence:
            return True
        elif left in fence and above in fence :
            return True
        elif left in fence and below in fence:
            return True
        else :return False

    def food_exist(sheep_position, foods):
        if sheep_position in foods:
            return True
        else: return False

    def valid_move(self, figure, x_new, y_new, field):
         # Neither the sheep nor the wolf, can step on a square outside the map. Imagine the map is surrounded by fences.
        if x_new > FIELD_HEIGHT - 1:
            return False
        elif x_new < 0:
            return False
        elif y_new > FIELD_WIDTH -1:
            return False
        elif y_new < 0:
            return False

        # Neither the sheep nor the wolf, can enter a square with a fence on.
        if field[x_new][y_new] == CELL_FENCE:
            return False

        # Wolfs can not step on squares occupied by the opponents wolf (wolfs block each other).
        # Wolfs can not step on squares occupied by the sheep of the same player .
        if figure == CELL_WOLF_1:
            if field[x_new][y_new] == CELL_WOLF_2:
                return False
            elif field[x_new][y_new] == CELL_SHEEP_1:
                return False
        elif figure == CELL_WOLF_2:
            if field[x_new][y_new] == CELL_WOLF_1:
                return False
            elif field[x_new][y_new] == CELL_SHEEP_2:
                return False


        # Sheep can not step on squares occupied by the wolf of the same player.
        # Sheep can not step on squares occupied by the opposite sheep.
        if figure == CELL_SHEEP_1:
            if field[x_new][y_new] == CELL_SHEEP_2 or \
                field[x_new][y_new] == CELL_WOLF_1:
                return False
        elif figure == CELL_SHEEP_2:
            if field[x_new][y_new] == CELL_SHEEP_1 or \
                    field[x_new][y_new] == CELL_WOLF_2:
                return False

        return True

    def fence_between(sheep_position,wolf_position, fence):
        if sheep_position[0] - wolf_position[0] >=1 and sheep_position[1] - wolf_position[1] == 0:
            # sheep right wolf
            x_dis = abs(sheep_position[0] - wolf_position[0])
            for i in range(x_dis+1):
                if (sheep_position[0]-i, sheep_position[1]) in fence:
                    return True
                    break
                else: continue
        elif sheep_position[0] - wolf_position[0] <=-1 and sheep_position[1] - wolf_position[1] == 0:
            # sheep left wolf
            x_dis = abs(sheep_position[0] - wolf_position[0])
            for i in range(x_dis+1):
                if (sheep_position[0]+i, sheep_position[1]) in fence:
                    return True
                    break
                else: continue
        elif sheep_position[0] - wolf_position[0] == 0  and sheep_position[1] - wolf_position[1] >= 1:
            # sheep below wolf
            x_dis = abs(sheep_position[1] - wolf_position[1])
            for i in range(x_dis+1):
                if (sheep_position[0], sheep_position[1]-i) in fence:
                    return True
                    break
                else: continue
        elif sheep_position[0] - wolf_position[0] == 0  and sheep_position[1] - wolf_position[1] <= -1:
            # sheep above wolf
            x_dis = abs(sheep_position[1] - wolf_position[1])
            for i in range(x_dis+1):
                if (sheep_position[0], sheep_position[1]+i) in fence:
                    return True
                    break
                else: continue
        elif sheep_position[0] - wolf_position[0] >= 1  and sheep_position[1] - wolf_position[1] >= 1:
            # sheep right  below wolf
            x_dis = abs(sheep_position[0] - wolf_position[0])
            y_dis = abs(sheep_position[1] - wolf_position[1])
            for i in range(x_dis+1):
                for j in range(y_dis+1):
                    if (sheep_position[0]-i, sheep_position[1]-j) in fence:
                        return True
                        break
                    else: continue
        elif sheep_position[0] - wolf_position[0] >= 1  and sheep_position[1] - wolf_position[1] <= -1:
            # sheep right  above wolf
            x_dis = abs(sheep_position[0] - wolf_position[0])
            y_dis = abs(sheep_position[1] - wolf_position[1])
            for i in range(x_dis+1):
                for j in range(y_dis+1):
                    if (sheep_position[0]-i, sheep_position[1]+j) in fence:
                        return True
                        break
                    else: continue
        elif sheep_position[0] - wolf_position[0] <= -1  and sheep_position[1] - wolf_position[1] <= -1:
            # sheep left  above wolf
            x_dis = abs(sheep_position[0] - wolf_position[0])
            y_dis = abs(sheep_position[1] - wolf_position[1])
            for i in range(x_dis+1):
                for j in range(y_dis+1):
                    if (sheep_position[0]+i, sheep_position[1]+j) in fence:
                        return True
                        break
                    else: continue
        elif sheep_position[0] - wolf_position[0] <= -1  and sheep_position[1] - wolf_position[1] >= 1:
            # sheep left  below wolf
            x_dis = abs(sheep_position[0] - wolf_position[0])
            y_dis = abs(sheep_position[1] - wolf_position[1])
            for i in range(x_dis+1):
                for j in range(y_dis+1):
                    if (sheep_position[0]+i, sheep_position[1]-j) in fence:
                        return True
                        break
                    else: continue
        else: return False

    def fence_nextto(sheep_position,food_goal,fence):
        if sheep_position[0] - food_goal[0] == 2 and sheep_position[1] - food_goal[1] == 0:
            if (sheep_position[0]-1, sheep_position[1]) in fence:
                return True
        elif sheep_position[0] - food_goal[0] == -2  and sheep_position[1] - food_goal[1] == 0:
            if (sheep_position[0]+1, sheep_position[1]) in fence:
                return True
        elif sheep_position[0] - food_goal[0] == 0  and sheep_position[1] - food_goal[1] == 2:
            if (sheep_position[0], sheep_position[1]-1) in fence:
                return True
        elif sheep_position[0] - food_goal[0] == 0  and sheep_position[1] - food_goal[1] == -2:
            if (sheep_position[0], sheep_position[1]+1) in fence:
                return True
        else: return False


    def move_sheep(self, p_num ,p_state, p_time_remaining, field):

        if 'sheep_model' not in p_state:
            p_state['sheep_model'] = self.get_sheep_model()

        sheep_model = p_state['sheep_model']
 

        X_sheep = []
        game_features = []
        
        #preprocess field to get features, add to X_sheep
        #this code is largely copied from the Jupyter Notebook where the models were trained
        
        #create empty feature array for this game state
        
        #add features and move to X_sheep 
        
        if p_num == 1:
            sheep = CELL_SHEEP_1
            wolf = CELL_WOLF_2
            op_wolf = CELL_WOLF_1
            op_sheep = CELL_SHEEP_2
        else:
            sheep = CELL_SHEEP_2
            wolf = CELL_WOLF_1
            op_wolf = CELL_WOLF_2
            op_sheep = CELL_SHEEP_1

        #get positions of sheep, wolf and food items
        food = []
        obstacles = []
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
                elif item == CELL_FENCE:
                    obstacles.append((x,y))
                elif item == op_wolf:
                    op_wolf_position = (x,y)
                elif item == op_sheep:
                    op_sheep_position = (x,y)
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
        
        #determine closest food:
        food_distance = 1000
        food_goal = None
        for food_item in food:
            distance = abs(food_item[0] - sheep_position[0]) + abs(food_item[1] - sheep_position[1])
            if distance < food_distance:
                food_distance = distance
                food_goal = food_item
        if food_goal != None:
            #feature 5: determine if food within two steps up

            if food_goal != None:
            #feature 5: determine if closest food is below the sheep
                if sheep_position[1] - food_goal[1] < 0:
                    s_feature5 = 1

            #feature 6: determine if closest food is above the sheep
                if sheep_position[1] - food_goal[1] > 0:
                    s_feature6 = 1

            #feature 7: determine if closest food is right of the sheep
                if sheep_position[0] - food_goal[0] < 0:
                    s_feature7 = 1

            #feature 8: determine if closest food is left of the sheep
                if sheep_position[0] - food_goal[0] > 0:
                    s_feature8 = 1
            
        game_features.append(s_feature5)
        game_features.append(s_feature6)
        game_features.append(s_feature7)
        game_features.append(s_feature8)
        
        s_feature9 = abs(sheep_position[0]-wolf_position[0])+abs(sheep_position[1]-wolf_position[1])
        
        game_features.append(s_feature9)

        X_sheep.append(game_features)

        result = sheep_model.predict(X_sheep)

        proba = sheep_model.predict_proba(X_sheep)

        proba_dic = {-2:proba[0][0], -1:proba[0][1], 0:proba[0][2], 1:proba[0][3], 2:proba[0][4]}

        while True:

            if result[0] == 0:
                if 0 in proba_dic.keys():
                    proba_dic.pop(result[0])
                next_max = max(proba_dic.values())
                next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                result = np.array([next_step])

            if result[0] == -2:
                new_position = ((sheep_position[0]-1),sheep_position[1])
            elif result[0] == 2:
                new_position = ((sheep_position[0]+1),sheep_position[1])
            elif result[0] == -1:
                new_position = (sheep_position[0],(sheep_position[1]-1))
            elif result[0] == 1:
                new_position = (sheep_position[0],(sheep_position[1]+1))


            if new_position in obstacles or not self.valid_move(sheep,new_position[1] , new_position[0], field) : 
                proba_dic.pop(result[0])
                if proba_dic:
                    next_max = max(proba_dic.values())
                    next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                    result = np.array([next_step])

            else :
                break

       
       
        if SheepTheVictim.manhattan_D(sheep_position, wolf_position) >2  or SheepTheVictim.fence_between(sheep_position, wolf_position, obstacles):

            if food_goal :
               
                if not SheepTheVictim.fence_surrounded(sheep_position, obstacles):

                    if SheepTheVictim.manhattan_D(SheepTheVictim.new_sheep_position(result,sheep_position), food_goal) > SheepTheVictim.manhattan_D(sheep_position,food_goal) \
                    and not SheepTheVictim.fence_between(sheep_position, food_goal, obstacles) :
                        
                    
                        if (abs(food_goal[0]-sheep_position[0]) >= 1 and abs(food_goal[1]-sheep_position[1]) == 0) \
                        or (abs(food_goal[0]-sheep_position[0]) == 0 and abs(food_goal[1]-sheep_position[1]) >= 1):
                            
                            if food_goal[0]-sheep_position[0] >= 1 :
                                if proba_dic:
                            
                                    proba_dic.pop(result[0])
                                
                                if proba_dic:
                                    next_max = max(proba_dic.values())
                                    next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                                    result = np.array([next_step])

                              
                            elif food_goal[0]-sheep_position[0] <= -1 :
                                if proba_dic:
                                
                                    proba_dic.pop(result[0])
                               
                                if proba_dic:
                                    next_max = max(proba_dic.values())
                                    next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                                    result = np.array([next_step])

                            
                            elif food_goal[1]-sheep_position[1] >= 1 :
                                if proba_dic:
                            
                                    proba_dic.pop(result[0])
                               
                                if proba_dic:
                                    next_max = max(proba_dic.values())
                                    next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                                    result = np.array([next_step])

                           
                            elif food_goal[1]-sheep_position[1] <= -1 :
                                if proba_dic:
                               
                                    proba_dic.pop(result[0])
                                
                                if proba_dic:
                                    next_max = max(proba_dic.values())
                                    next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                                    result = np.array([next_step])

                            

                        else:
                            result[0] = -result[0]

                    elif SheepTheVictim.fence_nextto(SheepTheVictim.new_sheep_position(result,sheep_position),food_goal,obstacles) and \
                    not SheepTheVictim.food_exist(SheepTheVictim.new_sheep_position(result,sheep_position),food):
                        
                        if (abs(food_goal[0]-sheep_position[0]) >= 1 and abs(food_goal[1]-sheep_position[1]) == 0) \
                        or (abs(food_goal[0]-sheep_position[0]) == 0 and abs(food_goal[1]-sheep_position[1]) >= 1):
                            if proba_dic:
                                proba_dic.pop(result[0]) 
                                if proba_dic:
                                    next_max = max(proba_dic.values())
                                    next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                                    result = np.array([next_step])

                    elif SheepTheVictim.fence_nextto(sheep_position,food_goal,obstacles):
                        if (abs(food_goal[0]-sheep_position[0]) >= 1 and abs(food_goal[1]-sheep_position[1]) == 0) \
                        or (abs(food_goal[0]-sheep_position[0]) == 0 and abs(food_goal[1]-sheep_position[1]) >= 1):
                            if proba_dic:
                                proba_dic.pop(result[0])
                                if proba_dic:
                                    next_max = max(proba_dic.values())
                                    next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                                    result = np.array([next_step])


                    elif SheepTheVictim.fence_surrounded(SheepTheVictim.new_sheep_position(result,sheep_position), obstacles) and \
                    not SheepTheVictim.food_exist(SheepTheVictim.new_sheep_position(result,sheep_position),food):
                        if proba_dic:
                            proba_dic.pop(result[0])
                            if proba_dic:
                                next_max = max(proba_dic.values())
                                next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                                result = np.array([next_step])

                elif SheepTheVictim.fence_surrounded(sheep_position, obstacles):

                    right = (sheep_position[0]+1,sheep_position[1])
                    left = (sheep_position[0]-1,sheep_position[1])
                    above = (sheep_position[0],sheep_position[1]-1)
                    below = (sheep_position[0],sheep_position[1]+1)


                    if right in obstacles and above in obstacles:
                        if 2 in proba_dic:
                            proba_dic.pop(2)
                        if -1 in proba_dic:
                            proba_dic.pop(-1)
                        if proba_dic :
                            next_max = max(proba_dic.values())
                            next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                            result = np.array([next_step])

                    elif right in obstacles and below in obstacles:
                        if 1 in proba_dic:
                            proba_dic.pop(1)
                        if 2 in proba_dic:
                            proba_dic.pop(2)
                        if proba_dic :
                            next_max = max(proba_dic.values())
                            next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                            result = np.array([next_step])
                    elif left in obstacles and above in obstacles :
                        if -2 in proba_dic:
                            proba_dic.pop(-2)
                        if -1 in proba_dic:
                            proba_dic.pop(-1)
                        if proba_dic :
                            next_max = max(proba_dic.values())
                            next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                            result = np.array([next_step])
                    elif left in obstacles and below in obstacles:
                        if 1 in proba_dic:
                            proba_dic.pop(1)
                        if -2 in proba_dic:
                            proba_dic.pop(-2)
                        if proba_dic :
                            next_max = max(proba_dic.values())
                            next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                            result = np.array([next_step])
                elif SheepTheVictim.fence_surrounded(SheepTheVictim.new_sheep_position(result,sheep_position), obstacles) and \
                not SheepTheVictim.food_exist(SheepTheVictim.new_sheep_position(result,sheep_position),food):
                    if proba_dic:
                            proba_dic.pop(result[0])
                            if proba_dic:
                                next_max = max(proba_dic.values())
                                next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                                result = np.array([next_step])


        else:

                    while True:
                            new_position = SheepTheVictim.new_sheep_position(result,sheep_position)

                            if self.valid_move(sheep,new_position[1] , new_position[0], field) and \
                            (SheepTheVictim.manhattan_D(SheepTheVictim.new_sheep_position(result,sheep_position), wolf_position)) > SheepTheVictim.manhattan_D(sheep_position, wolf_position):
                        
                                break
                            elif proba_dic:
                                proba_dic.pop(result[0])
                                if proba_dic:
                                    next_max = max(proba_dic.values())
                                    next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                                    result = np.array([next_step])
                                continue
                            else:
                                result[0] = 0
                                break

        return result, p_state


    def move_wolf(self, p_num, p_state, p_time_remaining, field):
        if 'wolf_model' not in p_state:
            p_state['wolf_model'] = self.get_wolf_model()

        wolf_model = p_state['wolf_model']
        X_wolf = []
        game_features = []
        
        #preprocess field to get features, add to X_wolf
        #this code is largely copied from the Jupyter Notebook where the models were trained
        
        #create empty feature array for this game state
        
        #add features and move to X_wolf and Y_wolf
        
        if p_num == 1:
            sheep = CELL_SHEEP_2
            wolf = CELL_WOLF_1
            op_wolf = CELL_WOLF_2
            my_sheep = CELL_SHEEP_1
        else:
            sheep = CELL_SHEEP_1
            wolf = CELL_WOLF_2
            op_wolf = CELL_WOLF_1
            my_sheep = CELL_SHEEP_2
            
            
        y=0
        obstacles = []
        for field_row in field:
            x = 0
            for item in field_row:
                if item == sheep:
                    sheep_position = (x,y)
                elif item == wolf:
                    wolf_position = (x,y)
                elif item == CELL_FENCE:
                    obstacles.append((x,y))
                elif item == op_wolf:
                    op_wolf_position = (x,y)
                elif item == my_sheep:
                    my_sheep_position = (x,y)
                x += 1
            y+=1
            
        #feature 1: determine if the sheep is above the wolf
        if wolf_position[1] - sheep_position[1] > 0:
            w_feature1 = 1
        else:
            w_feature1 = 0
        game_features.append(w_feature1)

        #feature 2: determine if the sheep is below the wolf
        if wolf_position[1] - sheep_position[1] < 0:
            w_feature2 = 1
        else:
            w_feature2 = 0
        game_features.append(w_feature2)

        #feature 3: determine if the sheep is left of the wolf
        if wolf_position[0] - sheep_position[0] > 0:
            w_feature3 = 1
        else:
            w_feature3 = 0
        game_features.append(w_feature3)

        #feature 4: determine if the sheep is right from the wolf
        if wolf_position[0] - sheep_position[0] < 0:
            w_feature4 = 1
        else:
            w_feature4 = 0
        game_features.append(w_feature4)

        s_feature5 = abs(sheep_position[0]-wolf_position[0])+abs(sheep_position[1]-wolf_position[1])
        
        game_features.append(s_feature5)

        s_feature6 = abs(op_wolf_position[0]-wolf_position[0])+abs(op_wolf_position[1]-wolf_position[1])
        
        game_features.append(s_feature6)
        
        X_wolf.append(game_features)

        result = wolf_model.predict(X_wolf)

        proba = wolf_model.predict_proba(X_wolf)

        proba_dic = {-2:proba[0][0], -1:proba[0][1], 0:proba[0][2], 1:proba[0][3], 2:proba[0][4]}

        while True:

            if result[0] == 0:
                if 0 in proba_dic.keys():
                    proba_dic.pop(result[0])
                next_max = max(proba_dic.values())
                next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                result = np.array([next_step])

            if result[0] == -2:
                new_position = ((wolf_position[0]-1),wolf_position[1])
            elif result[0] == 2:
                new_position = ((wolf_position[0]+1),wolf_position[1])
            elif result[0] == -1:
                new_position = (wolf_position[0],(wolf_position[1]-1))
            elif result[0] == 1:
                new_position = (wolf_position[0],(wolf_position[1]+1))


            if new_position in obstacles or not self.valid_move(wolf, new_position[1], new_position[0],field): 
                proba_dic.pop(result[0])
                if proba_dic:
                    next_max = max(proba_dic.values())
                    next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                    result = np.array([next_step])

            else :
                break


        if SheepTheVictim.fence_surrounded(wolf_position, obstacles) :
                    step_dic = {-2:-2, -1:-1, 1:1, 2:2}

                    right = (wolf_position[0]+1,wolf_position[1])
                    left = (wolf_position[0]-1,wolf_position[1])
                    above = (wolf_position[0],wolf_position[1]-1)
                    below = (wolf_position[0],wolf_position[1]+1)

                    if right in obstacles and above in obstacles:
                        if 2 in proba_dic:
                            proba_dic.pop(2)
                        if -1 in proba_dic:
                            proba_dic.pop(-1)
                        if proba_dic :
                            next_max = max(proba_dic.values())
                            next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                            result = np.array([next_step])
                    elif right in obstacles and below in obstacles:
                        if 2 in proba_dic:
                            proba_dic.pop(2)
                        if 1 in proba_dic:
                            proba_dic.pop(1)
                        if proba_dic :
                            next_max = max(proba_dic.values())
                            next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                            result = np.array([next_step])
                    elif left in obstacles and above in obstacles :
                        if -2 in proba_dic:
                            proba_dic.pop(-2)
                        if -1 in proba_dic:
                            proba_dic.pop(-1)
                        if proba_dic :
                            next_max = max(proba_dic.values())
                            next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                            result = np.array([next_step])
                    elif left in obstacles and below in obstacles:
                        if -2 in proba_dic:
                            proba_dic.pop(-2)
                        if 1 in proba_dic:
                            proba_dic.pop(1)
                        if proba_dic :
                            next_max = max(proba_dic.values())
                            next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                            result = np.array([next_step])

                    new_position = SheepTheVictim.new_wolf_position(result,wolf_position)

                    if not self.valid_move(wolf, new_position[1], new_position[0],field):

                        proba_dic.pop(result[0])
                        if proba_dic:
                            next_max = max(proba_dic.values())
                            next_step = list(proba_dic.keys())[list(proba_dic.values()).index(next_max)]
                            result = np.array([next_step])
                        else:
                            remain_choice = list(step_dic.keys())
                            random_step = random.choice(remain_choice)
                            result = np.array([random_step])

        return result, p_state



        