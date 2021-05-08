import math
import random
import time
import networkx as nx
import pygame
import matplotlib
TARGET_NUM = 7
POPULATION = 100
ver_population = 5
ver_chromosome = 50
ver_fuck = 0


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


class Vert:

    def __init__(self):
        self.x_vertex = 0
        self.y_vertex = 0

    def length(self, x):
        return math.sqrt((self.x_vertex - x.x_vertex) ** 2 + (self.y_vertex - x.y_vertex) ** 2)


class Drone:

    def __init__(self):
        self.x_vertex = 255
        self.y_vertex = 255
        self.color = (255, 0, 0)
        self.length_route = 0
        self.F = 0
        self.chromosome = [0, 1, 2, 3, 4, 5, 6]
        random.shuffle(self.chromosome)

    def move(self, x, y):
        if (self.x_vertex - x) + (self.y_vertex - y) == 0:
            self.length_route += 100000
        else:
            self.length_route += math.sqrt((self.x_vertex - x) ** 2 + (self.y_vertex - y) ** 2)
            self.x_vertex = x
            self.y_vertex = y

    def mutation(self):
        random.shuffle(self.chromosome)


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

true_chromosome = []


def Dijkstra(N, S, target_list, base):
    G = nx.Graph()

    av = Vert()
    av.x_vertex = base.x_vertex
    av.y_vertex = base.y_vertex
    fl_list = []
    fl_list.append(av)
    for i in range(TARGET_NUM):
        av = Vert()
        av.x_vertex = target_list[i].x_vertex
        av.y_vertex = target_list[i].y_vertex
        fl_list.append(av)

    for i in range(TARGET_NUM+1):
        for j in range(TARGET_NUM+1):
            G.add_edge(i, j, weight=fl_list[i].length(fl_list[j]))
    print(nx.dijkstra_path(G, 0, TARGET_NUM))

#Dijkstra(TARGET_NUM+1, 0, target_list, base)

# run process
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

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

    # Draw a solid black point. This is our base
    pygame.draw.circle(screen, base.color, (base.x_vertex, base.y_vertex), 10)

    # find tagrets
    for i in range(POPULATION):
        target_index = drone_list[i].chromosome[step]
        new_x_vertex = target_list[target_index].x_vertex
        new_y_vertex = target_list[target_index].y_vertex
        drone_list[i].move(new_x_vertex, new_y_vertex)
        target_list[target_index].taken()

    time.sleep(3)
    # new gen
    if step == TARGET_NUM-1:
        step_null = True
        gen += 1
        step = 0
        min_ = 10000000
        sum_ = 0
        min_num = 0

        # find min route to print
        for i in range(POPULATION):
            if drone_list[i].length_route < min_:
                min_ = drone_list[i].length_route
                min_num = i

        for i in range(TARGET_NUM):
            target_list[i].reload()

        for i in range(TARGET_NUM):
            pygame.draw.circle(screen, target_list[i].color, (target_list[i].x_vertex, target_list[i].y_vertex), 5)

        if gen % 1 == 0:
            pygame.draw.line(screen, (0, 0, 0),
                             (base.x_vertex,
                              base.y_vertex),
                             (target_list[drone_list[min_num].chromosome[0]].x_vertex,
                              target_list[drone_list[min_num].chromosome[0]].y_vertex),
                             1)
            for i in range(TARGET_NUM - 1):
                if i % 5 == 0 and i != 0:
                    pygame.draw.line(screen, (0, 0, 0),
                                     (target_list[drone_list[min_num].chromosome[i]].x_vertex,
                                      target_list[drone_list[min_num].chromosome[i]].y_vertex),
                                     (base.x_vertex,
                                      base.y_vertex),
                                     1)
                    pygame.draw.line(screen, (0, 0, 0),
                                     (base.x_vertex,
                                      base.y_vertex),
                                     (target_list[drone_list[min_num].chromosome[i + 1]].x_vertex,
                                      target_list[drone_list[min_num].chromosome[i + 1]].y_vertex),
                                     1)
                else:
                    pygame.draw.line(screen, (255, 0, 0),
                                     (target_list[drone_list[min_num].chromosome[i]].x_vertex,
                                      target_list[drone_list[min_num].chromosome[i]].y_vertex),
                                     (target_list[drone_list[min_num].chromosome[i + 1]].x_vertex,
                                      target_list[drone_list[min_num].chromosome[i + 1]].y_vertex),
                                     1)
                pygame.display.flip()
                time.sleep(1)

            pygame.draw.line(screen, (0, 0, 0),
                             (target_list[drone_list[min_num].chromosome[TARGET_NUM-1]].x_vertex,
                              target_list[drone_list[min_num].chromosome[TARGET_NUM-1]].y_vertex),
                             (base.x_vertex,
                              base.y_vertex),
                             1)
            pygame.display.flip()
            time.sleep(5)

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

        new_drones = []

        # childs with roulette
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
            if random.randint(1, 200) < ver_population:
                a_v = random.randint(0, TARGET_NUM-1)
                b_v = random.randint(0, TARGET_NUM-1)

                temp = drone_list[i].chromosome[b_v]
                drone_list[i].chromosome[b_v] = drone_list[i].chromosome[a_v]
                drone_list[i].chromosome[a_v] = temp

        for i in range(TARGET_NUM):
            target_list[i].reload()

    if (gen % 1 == 0) and (gen != 0) and (step % 15 == 3):
        print('Поколение = ' + str(gen))
        print('При ver_chromosome = ' + str(ver_chromosome))
        print('При ver_population = ' + str(ver_population))
        print('Лучший результат = ' + str(min_))
    step += 1

    if step_null:
        step_null = False
        step = 0
