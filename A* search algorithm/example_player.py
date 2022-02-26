
from config import *

# import point

import sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = sys.maxsize

def get_class_name():
    return 'SheepTheVictim'

class SheepTheVictim:
    """Example class for a Kingsheep player"""

    def __init__(self):
        self.name = "SheepTheVictim"
        self.uzh_shortname = "qiawan"
        self.open_set = []
        self.close_set = [] 
        self.open_set_sheep = []
        self.close_set_sheep = []
    
    def BaseCost(self, start, point):
        dx = abs(start.x - point.x)
        dy = abs(start.y - point.y)
        # Distance to start point
        return dx + dy

    def HeuristicCost(self, des, point):
        dx = abs(des.x - point.x)
        dy = abs(des.y - point.y)
        return dx + dy

    def TotalCost(self, start, des, point):
        return (self.BaseCost(start, point) + self.HeuristicCost(des,point))

    def IsInPointList(self, p, point_list):
        for point in point_list:
            if point.x == p.x and point.y == p.y:
                return True
        return False

    def IsInOpenList(self, p):
        return self.IsInPointList(p, self.open_set)

    def IsInCloseList(self, p):
        return self.IsInPointList(p, self.close_set)
    
    def IsInOpenList_sheep(self, p):
        return self.IsInPointList(p, self.open_set_sheep)

    def IsInCloseList_sheep(self, p):
        return self.IsInPointList(p, self.close_set_sheep)

    def get_player_position(self,figure,field):
        x = [x for x in field if figure in x][0]
        return (field.index(x), x.index(figure))

    def food_present(self,field):   #find if there is still food left in the field
        food_present = False

        for line in field: 
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    food_present = True
                    break
        return food_present

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



    def move_sheep(self, p_num, p_state, p_time_remaining, field):
        # edit here incl. the return statement
        if p_num == 1:
            figure = CELL_SHEEP_1
            sheep_position = self.get_player_position(CELL_SHEEP_1, field)
            wolf_position = self.get_player_position(CELL_WOLF_2, field)
            sheep = CELL_SHEEP_1
        else:
            figure = CELL_SHEEP_2
            sheep_position = self.get_player_position(CELL_SHEEP_2, field)
            wolf_position = self.get_player_position(CELL_WOLF_1, field)
            sheep = CELL_SHEEP_2


        if self.food_present(field):
            path = []
            next_goal = self.closest_goal(p_num, field)
            start_point = Point (sheep_position[1], sheep_position[0]) 
            start_point.cost = 0
            end_point = Point (next_goal[1], next_goal[0])  
            self.open_set_sheep.append(start_point)

            while True:
                index = self.SelectPointInOpenList_sheep(start_point, end_point)
                if index < 0:
                    move = MOVE_NONE
                    return move, p_state             
                else:
                    p = self.open_set_sheep[index]

                    if p.x == end_point.x and p.y == end_point.y:
                        path = self.BuildPath(p, start_point)
                        
                        first_step = path[1]
                        if (abs(first_step.x - wolf_position[1]) <=1 and abs(first_step.y - wolf_position[0]) <=1):
                            move = self.run_from_wolf(p_num, field)
                            # return move, p_state
                        elif first_step.x == start_point.x:
                            if first_step.y < start_point.y:
                                move = MOVE_UP
                            elif first_step.y > start_point.y:
                                move = MOVE_DOWN
                        elif first_step.y == start_point.y:
                            if first_step.x < start_point.x:
                                move = MOVE_LEFT
                            elif first_step.x > start_point.x:
                                move = MOVE_RIGHT

                        return move, p_state
                    del self.open_set_sheep[index]
                    self.close_set_sheep.append(p)

                    x = p.x
                    y = p.y


                    self.ProcessPoint_sheep(sheep, y, x-1, p, start_point, end_point, field)
                    self.ProcessPoint_sheep(sheep, y-1, x, p, start_point, end_point, field)
                    self.ProcessPoint_sheep(sheep, y, x+1, p, start_point, end_point, field)
                    self.ProcessPoint_sheep(sheep, y+1, x, p, start_point, end_point, field)

        elif self.wolf_close(p_num, field):
            move = self.run_from_wolf(p_num, field)
            return move, p_state
        elif wolf_position[0] > sheep_position[0]:
            
            if self.valid_move(sheep,sheep_position[0]-1,sheep_position[1], field):
                move = MOVE_UP
                return move, p_state
            elif sheep_position[1] >= FIELD_WIDTH%2 and wolf_position[1] >= sheep_position[1] and self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                move = MOVE_LEFT
                return move, p_state
            elif sheep_position[1] < FIELD_WIDTH%2 and wolf_position[1] <= sheep_position[1] and self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                move = MOVE_RIGHT
                return move, p_state 
            # elif (not self.valid_move(sheep,sheep_position[0]-1,sheep_position[1], field)) and (abs (wolf_position[0] - sheep_position[0]))>=3 and self.valid_move(sheep,sheep_position[0]+1,sheep_position[1], field):
            #     move = MOVE_DOWN
            #     return move, p_state
            else:
                move = MOVE_NONE

                return move, p_state

        elif wolf_position[0] < sheep_position[0]:
            if self.valid_move(sheep,sheep_position[0]+1,sheep_position[1], field):
                move = MOVE_DOWN
                return move, p_state
            elif sheep_position[1] >= FIELD_WIDTH%2 and wolf_position[1] >= sheep_position[1] and self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                move = MOVE_LEFT
                return move, p_state
            elif sheep_position[1] < FIELD_WIDTH%2 and wolf_position[1] <= sheep_position[1] and self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                move = MOVE_RIGHT
                return move, p_state
            elif (not self.valid_move(sheep,sheep_position[0]+1,sheep_position[1], field)) and (abs (wolf_position[0] - sheep_position[0]))>=3 and self.valid_move(sheep,sheep_position[0]-1,sheep_position[1], field):
                move = MOVE_UP
                return move, p_state
            else:
                move = MOVE_NONE

                return move, p_state

        elif wolf_position[0] == sheep_position[0] and wolf_position[1] < sheep_position [1] and self.valid_move(sheep,sheep_position[0]-1,sheep_position[1], field):
            move = MOVE_DOWN
            return move, p_state
        elif wolf_position[0] == sheep_position[0] and wolf_position[1] < sheep_position [1] and self.valid_move(sheep,sheep_position[0]+1,sheep_position[1], field):
            move = MOVE_UP
            return move, p_state
        else:
            move = MOVE_NONE

            return move, p_state

    def wolf_close(self,player_number,field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
            wolf_position = self.get_player_position(CELL_WOLF_2,field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            wolf_position = self.get_player_position(CELL_WOLF_1,field)

        if (abs(sheep_position[0]-wolf_position[0]) <= 2 and abs(sheep_position[1]-wolf_position[1]) <= 2):
            return True
        return False

    def run_from_wolf(self,player_number,field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
            wolf_position = self.get_player_position(CELL_WOLF_2,field)
            sheep = CELL_SHEEP_1
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            wolf_position = self.get_player_position(CELL_WOLF_1,field)
            sheep = CELL_SHEEP_2

        distance_x = sheep_position[1] - wolf_position[1]
        abs_distance_x = abs(sheep_position[1] - wolf_position[1])
        distance_y = sheep_position[0] - wolf_position[0]
        abs_distance_y = abs(sheep_position[0] - wolf_position[0])

        if abs_distance_y == 1 and distance_x == 0:
            if distance_y > 0 and sheep_position[1] < FIELD_WIDTH%2:
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                    return MOVE_RIGHT
                elif self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                    return MOVE_LEFT
                elif sheep_position[0]+1 != wolf_position[0]:
                    return MOVE_DOWN 
                elif sheep_position[0]-1 != wolf_position[0]:
                    return MOVE_UP  
            else: #it's below the sheep, move up if possible
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                    return MOVE_LEFT  
                elif self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                    return MOVE_RIGHT  
                elif sheep_position[0]+1 != wolf_position[0]:
                    return MOVE_DOWN 
                elif sheep_position[0]-1 != wolf_position[0]:
                    return MOVE_UP      
            # if this is not possible, flee to the right or left
            if self.valid_move(sheep,sheep_position[0]+1,sheep_position[1], field):
                return MOVE_DOWN
            elif self.valid_move(sheep,sheep_position[0]-1,sheep_position[1], field):
                return MOVE_UP
            else: #nowhere to go
                return MOVE_NONE

        #else if the wolf is close horizontally
        elif abs_distance_x == 1 and distance_y == 0:
            #print('wolf is close horizontally')
            #if it's to the left, move to the right if possible
            if distance_x > 0 and sheep_position[0] < FIELD_HEIGHT%2:
                if self.valid_move(sheep,sheep_position[0]+1,sheep_position[1], field):
                    return MOVE_DOWN
                elif self.valid_move(sheep,sheep_position[0]-1,sheep_position[1], field):
                    return MOVE_UP
                elif sheep_position[1]+1 != wolf_position[1]:
                    return MOVE_RIGHT 
                elif sheep_position[1]-1 != wolf_position[1]:
                    return MOVE_LEFT
            else: #it's to the right, move left if possible
                if self.valid_move(sheep,sheep_position[0]-1,sheep_position[1], field):
                    return MOVE_UP
                elif self.valid_move(sheep,sheep_position[0]+1,sheep_position[1], field):
                    return MOVE_DOWN
                elif sheep_position[1]+1 != wolf_position[1]:
                    return MOVE_RIGHT 
                elif sheep_position[1]-1 != wolf_position[1]:
                    return MOVE_LEFT
            #if this is not possible, flee up or down
            if self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                return MOVE_RIGHT
            elif self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                return MOVE_LEFT
            else: #nowhere to go
                return MOVE_NONE

        elif abs_distance_x == 1 and abs_distance_y == 1:
            #print('wolf is in my surroundings')
            #wolf is left and up
            if distance_x > 0 and distance_y > 0:
                #move right or down
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_DOWN
            #wolf is left and down
            if distance_x > 0 and distance_y < 0:
                #move right or up
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_UP
            #wolf is right and up
            if distance_x < 0 and distance_y > 0:
                #move left or down
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_DOWN
            #wolf is right and down
            if distance_x < 0 and distance_y < 0:
                #move left and up
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_UP

        else: #this method was wrongly called
            return MOVE_NONE

    def closest_goal(self,player_number,field):  
        possible_goals = []
        
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)

        #make list of possible goals

        y_position = 0
        for line in field:
            x_position = 0
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    possible_goals.append((y_position,x_position))
                x_position += 1
            y_position += 1

        #determine closest item and return
        distance = 1000
        for possible_goal in possible_goals:
            if (abs(possible_goal[0]-sheep_position[0])+abs(possible_goal[1]-sheep_position[1])) < distance:
                distance = abs(possible_goal[0]-sheep_position[0])+abs(possible_goal[1]-sheep_position[1])
                final_goal = (possible_goal)
                
        return final_goal

    def gather_closest_goal(self,closest_goal,field,figure):  
        figure_position = self.get_player_position(figure,field)  

        distance_x = figure_position[1]-closest_goal[1]
        distance_y = figure_position[0]-closest_goal[0]
        
        if distance_x == 0:

            if distance_y > 0:
                if self.valid_move(figure, figure_position[0]-1,figure_position[1],field):
                    return MOVE_UP
                else:
                    return MOVE_RIGHT
            else:
                if self.valid_move(figure, figure_position[0]+1,figure_position[1],field):
                    return MOVE_DOWN
                else:
                    return MOVE_RIGHT
        elif distance_y == 0:
            #print('item right beside me')
            if distance_x > 0:
                if self.valid_move(figure, figure_position[0],figure_position[1]-1,field):
                    
                    return MOVE_LEFT
                else:
                    return MOVE_UP
            else:
                if self.valid_move(figure, figure_position[0],figure_position[1]+1,field):
                    return MOVE_RIGHT
                else:
                    return MOVE_UP
        
        else:
            #go left or up
            if distance_x > 0 and distance_y > 0:
                if self.valid_move(figure, figure_position[0],figure_position[1]-1,field):
                    return MOVE_LEFT
                else:
                    return MOVE_UP

            #go left or down
            elif distance_x > 0 and distance_y < 0:
                if self.valid_move(figure, figure_position[0],figure_position[1]-1,field):
                    return MOVE_LEFT
                else:
                    return MOVE_DOWN

            #go right or up
            elif distance_x < 0 and distance_y > 0:
                if self.valid_move(figure,figure_position[0],figure_position[1]+1,field):
                    return MOVE_RIGHT
                else:
                    return MOVE_UP

            #go right or down
            elif distance_x < 0 and distance_y < 0:
                if self.valid_move(figure,figure_position[0],figure_position[1]+1,field):
                    return MOVE_RIGHT
                else:
                    return MOVE_DOWN

            else:
                # print('fail')
                return MOVE_NONE

    def move_wolf(self, p_num, p_state, p_time_remaining, field):
        # edit here incl. the return statement
        path = []
        if p_num == 1:
            wolf_position = self.get_player_position(CELL_WOLF_1,field)
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            wolf = CELL_WOLF_1
        else:
            wolf_position = self.get_player_position(CELL_WOLF_2,field)
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
            wolf = CELL_WOLF_2

        start_point = Point (wolf_position[1], wolf_position[0])  #$$$
        start_point.cost = 0
        end_point = Point (sheep_position[1], sheep_position[0])   #$$$
        self.open_set.append(start_point)

        while True:

            index = self.SelectPointInOpenList(start_point, end_point)
            if index < 0:
                move = MOVE_NONE
                return move, p_state
                
            p = self.open_set[index]


            if p.x == end_point.x and p.y == end_point.y:
                path = self.BuildPath(p, start_point)
                first_step = path[1]
                if first_step.x == start_point.x:
                    if first_step.y < start_point.y:
                        move = MOVE_UP
                    elif first_step.y > start_point.y:
                        move = MOVE_DOWN
                elif first_step.y == start_point.y:
                    if first_step.x < start_point.x:
                        move = MOVE_LEFT
                    elif first_step.x > start_point.x:
                        move = MOVE_RIGHT

                return move, p_state

            del self.open_set[index]
            self.close_set.append(p)

            x = p.x
            y = p.y


            self.ProcessPoint(wolf, y, x-1, p, start_point, end_point, field)
            self.ProcessPoint(wolf, y-1, x, p, start_point, end_point, field)
            self.ProcessPoint(wolf, y, x+1, p, start_point, end_point, field)
            self.ProcessPoint(wolf, y+1, x, p, start_point, end_point, field) 

    def ProcessPoint(self, figure, y, x, parent, start_point, end_point, field):
        if not self.valid_move(figure, y, x, field):
            return 
        p = Point(x, y)  
        if self.IsInCloseList(p):
            return 
        if not self.IsInOpenList(p):
            p.parent = parent
            p.cost = self.TotalCost(start_point, end_point, p)
            self.open_set.append(p)

    def SelectPointInOpenList(self, start_point, end_point):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            cost = self.TotalCost(start_point, end_point, p)
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index

    def BuildPath(self, p, start_point):
        path = []
        while True:
            path.insert(0, p) # Insert first
            if p.x == start_point.x and p.y == start_point.y:
                break
            else:
                p = p.parent
        return path

    def ProcessPoint_sheep(self, figure, y, x, parent, start_point, end_point, field):
        if not self.valid_move(figure, y, x, field):
            return 
        p = Point(x, y)   
        if self.IsInCloseList_sheep(p):
            return 
        if not self.IsInOpenList_sheep(p):
            p.parent = parent
            p.cost = self.TotalCost(start_point, end_point, p)
            self.open_set_sheep.append(p)

    def SelectPointInOpenList_sheep(self, start_point, end_point):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set_sheep:
            cost = self.TotalCost(start_point, end_point, p)
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index
