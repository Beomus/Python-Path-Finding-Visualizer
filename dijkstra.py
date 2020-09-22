from settings import *


class Node:
    def __init__(self, position=None, parent=None):
        self.position = position
        self.parent = parent
        self.distance = 0


class Dijkstra:
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.open_list = []
        self.closed_list = []
        self.wall_pos = wall_pos
        self.route = []
        self.route_found = False

    def draw_all_paths(self, current):
        i, j = current

        # draw each node it's visiting as it's searching simultaneously
        pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)

        # redraw start/end nodes on top of all route
        pygame.draw.rect(self.app.screen, TOMATO, (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE, (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)

        # redraw grid
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (GS_X + x * 24, GS_Y), (GS_X + x * 24, GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, ALICE, (GS_X, GS_Y + y * 24), (GE_X, GS_Y + y * 24))

        pygame.display.update()

    def generate_children(self, parent):
        parent_pos = parent.position
        for m in [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
            child_pos = (parent_pos[0] + m[0], parent_pos[1] + m[1])
            if self.check_valid(child_pos):
                child = Node(child_pos, parent)
                self.distance_calc(child, parent, m)

                if self.check_append(child) and self.check_wall_corner(parent, m):
                    self.open_list.append(child)

    def check_wall_corner(self, parent, move):
        move_list = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

        i, j = parent.position
        if move == move_list[0]:
            (x, y) = (0, 1)
            (a, b) = (-1, 0)
        elif move == move_list[1]:
            (x, y) = (0, 1)
            (a, b) = (1, 0)
        elif move == move_list[2]:
            (x, y) = (1, 0)
            (a, b) = (0, -1)
        else:
            (x, y) = (0, -1)
            (a, b) = (-1, 0)

        if (i + x, j + y) not in self.wall_pos or (i + a, j + b) not in self.wall_pos and move not in self.wall_pos:
            return True
        return False

    def distance_calc(self, child, parent, m):
        sum_difference = abs(sum(m))
        if sum_difference == 1:
            child.distance = parent.distance + 10
        elif sum_difference == 0 or sum_difference == 2:
            child.distance = parent.distance + 14

    def check_append(self, child):
        for open_node in self.open_list:
            if child.position == open_node.position and child.distance >= open_node.distance:
                return False
        return True

    def check_valid(self, position):
        if position not in self.wall_pos and position not in self.closed_list:
            return True
        return False

    def findEnd(self, position):
        if position == (self.end_node_x, self.end_node_y):
            return True
        return False

    def dijkstra_execute(self):
        # initialize start/end nodes
        start_node = Node((self.start_node_x, self.start_node_y), None)
        start_node.distance = 0
        end_node = Node((self.end_node_x, self.end_node_y), None)

        self.open_list.append(start_node)

        print(f"Start node: {start_node.position}")

        while len(self.open_list) > 0:
            # search for node with lowest distance traveled from the start node
            current_node = self.open_list[0]
            current_index = 0

            # get node with the lowest F-cost
            for index, node in enumerate(self.open_list):
                if node.distance < current_node.distance:
                    current_node = node
                    current_index = index

            # check if route has been found
            if self.findEnd(current_node.position):
                current = current_node
                # append path until the current node becomes none
                # start node has a parent of None
                while current is not None:
                    self.route.append(current.position)
                    current = current.parent
                self.route.pop(0)
                self.route_found = True
                break

            self.draw_all_paths(current_node.position)
            self.generate_children(current_node)

            self.open_list.pop(current_index)
            self.closed_list.append(current_node.position)
