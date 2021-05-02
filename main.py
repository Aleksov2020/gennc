import math
import random
import time

import pygame

TARGET_NUM = 16
POPULATION = 1


# define target points
class Target:

    def __init__(self, i):
        self.x_vertex = random.randint(0, 500)
        self.y_vertex = random.randint(0, 500)
        self.color = (0, 255, 0)
        self.code = bin(i)

    def taken(self):
        self.color = (255, 255, 255)

    def reload(self):
        self.color = (0, 255, 0)


class Base:

    def __init__(self):
        self.x_vertex = 255
        self.y_vertex = 255
        self.color = (0, 0, 0)


class Drone:

    def __init__(self):
        self.x_vertex = 255
        self.y_vertex = 255
        self.color = (255, 0, 0)
        self.length_route = 0
        self.F = 0
        self.chromosome = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        random.shuffle(self.chromosome)

    def move(self, x, y):
        if (self.x_vertex - x) + (self.y_vertex - y) == 0:
            self.length_route += 100000
        else:
            self.length_route += math.sqrt((self.x_vertex - x) ** 2 + (self.y_vertex - y) ** 2)
            self.x_vertex = x
            self.y_vertex = y


# set map
target_list = []
for i in range(TARGET_NUM):
    a = Target(i)
    target_list.append(a)

base = Base()

drone_list = []
for i in range(POPULATION):
    drone = Drone()
    drone_list.append(drone)

# run process
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
step = 0
gen = 0
step_null = False
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid green points. This is our targets
    for i in range(TARGET_NUM):
        pygame.draw.circle(screen, target_list[i].color, (target_list[i].x_vertex, target_list[i].y_vertex), 5)

    # Draw a solid black point. This is our base
    pygame.draw.circle(screen, base.color, (base.x_vertex, base.y_vertex), 10)

    for i in range(POPULATION):
        pygame.draw.circle(screen, drone_list[i].color, (drone_list[i].x_vertex, drone_list[i].y_vertex), 5)

    # drone go home
    if step % 4 == 0:
        new_x_vertex = base.x_vertex
        new_y_vertex = base.y_vertex
        drone_list[i].move(new_x_vertex, new_y_vertex)

    # find tagrets
    for i in range(POPULATION):
        target_index = drone_list[i].chromosome[step]
        new_x_vertex = target_list[target_index].x_vertex
        new_y_vertex = target_list[target_index].y_vertex
        drone_list[i].move(new_x_vertex, new_y_vertex)
        target_list[target_index].taken()

    # new gen
    if step == 15:
        step_null = True
        gen += 1
        step = 0
        min_ = 10000000
        sum_ = 0

        # find min route to print
        for i in range(POPULATION):
            if drone_list[i].length_route < min_:
                min_ = drone_list[i].length_route

        # find sum of result F
        for i in range(POPULATION):
            drone_list[i].F = 1 / drone_list[i].length_route * 100000
            sum_ += drone_list[i].F

        list_ver = []
        for i in range(POPULATION):
            list_ver.append(drone_list[i].F / sum_)

        roulette = [0]
        for i in range(1, POPULATION):
            roulette.append(list_ver[i] + roulette[i - 1])

        # childs
        new_drones = []
        for i in range(POPULATION):
            a = Drone()
            child_ = random.random()
            child_num = 0
            for j in range(POPULATION):
                if roulette[j] > child_:
                    child_num = j - 1
                    break
            a.chromosome = drone_list[child_num].chromosome
            new_drones.append(a)

        drone_list = new_drones

        # mutation
        for i in range(POPULATION):
            if random.randint(1, 10) % 4 == 0:
                a_v = random.randint(0, 15)
                b_v = random.randint(0, 15)
                temp = drone_list[i].chromosome[a_v]
                drone_list[i].chromosome[a_v] = drone_list[i].chromosome[b_v]
                drone_list[i].chromosome[b_v] = temp

        for i in range(TARGET_NUM):
            target_list[i].reload()

        print('Поколение - ' + str(gen))
        print('Лучший маршрут - ' + str(min_))

    step += 1

    if step_null:
        step_null = False
        step = 0

    # Flip the display
    pygame.display.flip()

    # Sleep
    time.sleep(0.5)
# Done! Time to quit.
pygame.quit()
