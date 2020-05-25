import heapq
import math

import networkx as nx

import util

"""
Let’s Travel! (Uniform Cost Search)
"""


class UCSPathPlanner:
    """
    implementation using heapq
    so only the first item is the smallest (i.e not complete sorted)
    """

    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.frontier = []
        # push the cost, city, path to the heapq
        heapq.heappush(self.frontier, (0, start, [start]))
        self.explored = set()
        self.maxSpeed = 300

    def ucs(self):
        # for i in range(3):
        while len(self.frontier) > 0:
            print('frontier = {}'.format(self.frontier[0]))
            c, current, path = heapq.heappop(self.frontier)
            print('explored = {}'.format(self.explored))
            if current == self.goal:
                return path, c
            self.explored.add(current)
            for n in nx.neighbors(self.graph, current):
                # try out different cost function
                # cost = self.graph[current][n]['weight']
                cost = self.cost_d(current, n)
                if (n not in self.explored) and (n not in self.frontier):
                    # insert
                    heapq.heappush(self.frontier, (cost + c, n, path + [n]))
                # if neighbour in frontier and have lower cost
                elif (n not in self.explored) and n in (t[1] for t in self.frontier):
                    idx = util.find_idx(n, self.frontier)
                    if idx is not None:
                        # replace
                        self.frontier[idx] = (cost + c, n, path + [n])
        return None

    def cost_d(self, cityFrom, cityTo):
        dist = self.graph[cityFrom][cityTo]['weight']
        cost = 1000000
        # try for all speed in range (V_lim - V_max)
        for speed in range(min(self.maxSpeed, dist), self.maxSpeed + 1):
            temp = 100 * (dist / speed) + self.fine(dist, speed)
            if temp < cost:
                cost = temp
        # return minimum cost
        # print(cost)
        return cost

    def fine(self, dist, speed):
        # if the distance is greater than max speed you always drive as fast as possible
        if dist >= self.maxSpeed:
            return 0
        else:
            # legal
            if speed <= dist:
                return 0
            # illegal
            else:
                return (1 - math.pow(math.e, -speed + dist)) * 1000


if __name__ == '__main__':
    # load the map
    cities = util.load_graph_from_file('UK_cities.json')

    planner = UCSPathPlanner(cities, 'london', 'aberdeen')
    try:
        route, length = planner.ucs()
        print('path = {}, length = {}'.format(route, length))
    except TypeError as e:
        print("Solution not found or not enough iteration...{}".format(e.args))
