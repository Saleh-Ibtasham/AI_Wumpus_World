import os
import time
import pygame
from pygame.locals import *
from random import randrange

###########Global variable ##################
list_of_caves = []
cave_color = (240,255,255)  
agent_image = pygame.image.load('images/agent.jpg')
wumpus_image = pygame.image.load('images/wumpus.jpg')
gold_image = pygame.image.load('images/gold.jpg')
pit_image = pygame.image.load('images/pit.jpg')
breeze_image = pygame.image.load('images/breeze.png')
stench_image = pygame.image.load('images/stench.jpg')
agent_position = []

path_cost_so_far = 0

###################Map elemnts list #######################
def print_list(list_name):
        for i in range(0,len(list_name)):
                for j in range(0,len(list_name[i])):
                        print(pit_in_cave[i][j], end =" ")
                print()



def create_list(row_size,column_size):
        new_list = [[0 for x in range(column_size)] for x in range(row_size)] 
        return new_list


pit_in_cave = create_list(10,10)
wumpus_in_cave = create_list(10,10)
glitter_in_cave = create_list(10,10)
agent_in_cave = create_list(10,10)
breeze_in_cave = create_list(10,10)
strench_in_cave = create_list(10,10)

######Initialize screen of game window ####################

game_window_width = 1000 
game_window_height = 700

pygame.init()
screen = pygame.display.set_mode((game_window_width, game_window_height))
pygame.display.set_caption('Wumpus World')


def event_handler():    
    for event in pygame.event.get():
        #print(event)
        if event.type == QUIT or (
             event.type == KEYDOWN and (
              event.key == K_ESCAPE or
              event.key == K_q
             )):    
            pygame.quit() #quit from pygame
            quit() #quit from py system


def draw_map():

        rect_width = 60
        rect_height = 60
                      
        left_padding = 200
        top_padding = 25

        for j in range(0,10):
                for i in range(0,10):

                        pos_x = (i*65)+left_padding
                        pos_y = (j*65)+top_padding
                        pygame.draw.rect(screen,cave_color,pygame.Rect(pos_x, pos_y, rect_width, rect_height))

                        cave_index = [pos_x,pos_y]
                        list_of_caves.append(cave_index)


def get_adjacent_caves(i,j):
        adjacent_caves = []
        
        if((i-1)>=0):
                adjacent_caves.append([i-1,j])
        if((i+1)<=9):
                adjacent_caves.append([i+1,j])
        if((j-1)>=0):
                adjacent_caves.append([i,j-1])
        if((j+1)<=9):
                adjacent_caves.append([i,j+1])
        
        return adjacent_caves


def get_image(name):
        global agent_image
        global wumpus_image
        global gold_image
        global pit_image

        if name == 'agent_image':
                return agent_image
        elif name == 'wumpus_image':
                return wumpus_image
        elif name == 'gold_image':
                return gold_image
        elif name == 'pit_image':
                return pit_image
        elif name == 'breeze_image':
                return breeze_image
        elif name == 'stench_image':
                return stench_image
        


def update_map_insights(element_type,index):
        
        str_index = str(index-1)
        i = int(str_index[0])
        j = int(str_index[1])
        
        if element_type == agent_image:
                agent_in_cave[i][j] = 1
        elif element_type == gold_image:
                glitter_in_cave[i][j] = 1
        
        elif element_type == wumpus_image:
                wumpus_in_cave[i][j] = 1
                adjacent_caves = get_adjacent_caves(i,j)
                image_add_list = []
                
                for neighbour in adjacent_caves:
                        neighbour_i = int(neighbour[0])
                        neighbour_j = int(neighbour[1])
                        
                        print('i,j ::',i,' ',j)
                        strench_in_cave[neighbour_i][neighbour_j] = 1
                        
                        cave_number = str(neighbour_i)+str(neighbour_j)
                        str_cave_number = str(int(cave_number)+1) #add_image_to_map will decrease the cave number again by 1
                        image_add_list.append(['stench_image',str_cave_number])
                
                add_image_to_map(image_add_list)                       
                        
        elif element_type == pit_image:
                pit_in_cave[i][j] = 1
                adjacent_caves = get_adjacent_caves(i,j)
                image_add_list = []
                
                for neighbour in adjacent_caves:
                        neighbour_i = int(neighbour[0])
                        neighbour_j = int(neighbour[1])
                        breeze_in_cave[neighbour_i][neighbour_j] = 1
                        cave_number = str(neighbour_i)+str(neighbour_j)
                        str_cave_number = str(int(cave_number)+1) #add_image_to_map will decrease the cave number again by 1
                        image_add_list.append(['breeze_image',str_cave_number]) 
                
                add_image_to_map(image_add_list)


def add_image_to_map(all_cave_item):
        image_left_padding = 5
        image_top_padding = 5

        for cave in all_cave_item:
                image = get_image(cave[0])
                cave_number = int(cave[1].rjust(2, '0'))
                index_x = list_of_caves[cave_number-1][0] + image_left_padding #cave number starts from 1
                index_y = list_of_caves[cave_number-1][1] + image_top_padding  #cave number starts from 
                
                screen.blit(image,(index_x,index_y))
                update_map_insights(image,cave_number)


def get_cave_description():
        all_cave_item = []
        
        environemnt_description_file = open("environment.txt", "r")
        line = environemnt_description_file.readline()
        while line:
                parsed_line =  line.split(',')
                single_cave = [x.strip() for x in parsed_line] 
                all_cave_item.append(single_cave)

                line = environemnt_description_file.readline()
                
        environemnt_description_file.close()
        return all_cave_item
            


def add_environments_elements():
        
        all_cave_item = get_cave_description()
        add_image_to_map(all_cave_item)
        


def update_total_cost():
        global path_cost_so_far
        path_cost_so_far = path_cost_so_far + 1
                
                
def keep_map_alive_and_update():
        while True:

                draw_map()
                add_environments_elements()
                event_handler()
                move_agent(list_of_caves[randrange(100)][0],list_of_caves[randrange(100)][1])
                pygame.display.update()
                
                print_list(wumpus_in_cave)
                update_total_cost()
                time.sleep(0.5) #just to make agent move more visible !
                




################agent movement ##################
def move_agent(x,y):
        screen.blit(agent_image,(x,y))
        agent_position = [x,y]
 




########################main function from where the prgram starts#############################
def main():
        keep_map_alive_and_update()
        

if __name__ == '__main__':
        main()