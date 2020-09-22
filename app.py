import sys
from settings import *
from buttons import Button
from bfs import BreadthFirst
from dfs import DepthFirst
from astar import Astar
from dijkstra import Dijkstra
from visualize_path import VisualizePath


pygame.init()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main menu'
        self.algorithm_state = ''
        self.grid_square_length = 24
        # self.load()
        self.start_end_checker = 0
        self.mouse_drag = 0

        # start and end nodes coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # wall nodes list
        self.wall_pos = wall_nodes_coords_list.copy()

        # main menu buttons
        self.bfs_button = Button(self, WHITE, 338, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'BFS')
        self.dfs_button = Button(self, WHITE, 558, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'DFS')
        self.astar_button = Button(self, WHITE, 778, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Astar')
        self.dijkstra_button = Button(self, WHITE, 998, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH,
                                      MAIN_BUTTON_HEIGHT, 'Dijkstra')

        # grid menu options
        self.start_end_node_button = Button(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT,
                                            GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Start/End Node')
        self.wall_node_button = Button(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT +
                                       GRID_BUTTON_HEIGHT + BUTTON_SPACER,
                                       GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT,
                                       'Wall Node')
        self.reset_button = Button(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT +
                                   GRID_BUTTON_HEIGHT * 2 + BUTTON_SPACER * 2,
                                   GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'RESET')
        self.start_button = Button(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT +
                                   GRID_BUTTON_HEIGHT * 3 + BUTTON_SPACER * 3,
                                   GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Visualize')
        self.main_menu_button = Button(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT +
                                       GRID_BUTTON_HEIGHT * 4 + BUTTON_SPACER * 4,
                                       GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Main Menu')

    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.main_menu_events()
            if self.state == 'grid window':
                self.grid_events()
            if self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            if self.state == 'start visualizing':
                self.execute_algo()
            if self.state == 'aftermath':
                self.reset_or_main_menu()
        pygame.quit()
        sys.exit()

    def load(self):
        # self.main_menu_background = pygame.image.load('background.png')
        # self.grid_background = pygame.image.load('grid.png')
        pass

    @staticmethod
    def draw_text(words, screen, pos, size, color, font_name, center=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if center:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def sketch_main_menu(self):
        # draw background
        # self.screen.blit(self.main_menu_background, (0, 0))

        self.bfs_button.draw_button(AQUAMARINE)
        self.dfs_button.draw_button(AQUAMARINE)
        self.astar_button.draw_button(AQUAMARINE)
        self.dijkstra_button.draw_button(AQUAMARINE)

    def sketch_hotbar(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (0, 0, 240, 768), 0)
        # draw grid background
        # self.screen.blit(self.grid_background, (0, 0))

    def sketch_grid(self):
        # add borders
        pygame.draw.rect(self.screen, ALICE, (240, 0, WIDTH, HEIGHT), 0)
        pygame.draw.rect(self.screen, AQUAMARINE, (264, 24, GRID_WIDTH, GRID_HEIGHT), 0)

        # draw grid with size 52, 30
        for x in range(52):
            pygame.draw.line(self.screen, ALICE, (GS_X + x * self.grid_square_length, GS_Y),
                                                 (GS_X + x * self.grid_square_length, GE_Y))
        for y in range(30):
            pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + y * self.grid_square_length),
                                                 (GE_X, GS_Y + y * self.grid_square_length))

    def sketch_grid_buttons(self):
        # draw buttons
        self.start_end_node_button.draw_button(STEELBLUE)
        self.wall_node_button.draw_button(STEELBLUE)
        self.reset_button.draw_button(STEELBLUE)
        self.start_button.draw_button(STEELBLUE)
        self.main_menu_button.draw_button(STEELBLUE)

    def set_menu_buttons_color(self, color):
        self.start_end_node_button.color = color
        self.wall_node_button.color = color
        self.reset_button.color = color
        self.start_button.color = color
        self.main_menu_button.color = color

    def grid_window_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_end_node_button.isOver(pos):
                self.state = 'draw S/E'
            elif self.wall_node_button.isOver(pos):
                self.state = 'draw walls'
            elif self.reset_button.isOver(pos):
                self.execute_reset()
            elif self.start_button.isOver(pos):
                self.state = 'start visualizing'
            elif self.main_menu_button.isOver(pos):
                self.back_to_menu()

        if event.type == pygame.MOUSEMOTION:
            if self.start_end_node_button.isOver(pos):
                self.start_end_node_button.color = MINT
            elif self.wall_node_button.isOver(pos):
                self.wall_node_button.color = MINT
            elif self.reset_button.isOver(pos):
                self.reset_button.color = MINT
            elif self.start_button.isOver(pos):
                self.start_button.color = MINT
            elif self.main_menu_button.isOver(pos):
                self.main_menu_button.color = MINT
            else:
                self.set_menu_buttons_color(STEELBLUE)

    def grid_button_keep_color(self):
        if self.state == 'draw S/E':
            self.start_end_node_button.color = MINT
        elif self.state == 'draw walls':
            self.wall_node_button.color = MINT

    def execute_reset(self):
        self.start_end_checker = 0

        # reset start and end nodes coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # reset wall nodes list
        self.wall_pos = wall_nodes_coords_list.copy()

        # reset state
        self.state = 'grid window'

    def back_to_menu(self):
        self.start_end_checker = 0

        # reset start and end nodes coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # reset wall nodes list
        self.wall_pos = wall_nodes_coords_list.copy()

        # switch state
        self.state = 'main menu'

    def set_algo_buttons_color(self, color):
        self.bfs_button.color = color
        self.dfs_button.color = color
        self.astar_button.color = color
        self.dijkstra_button.color = color

    def main_menu_events(self):
        # draw background
        pygame.display.update()
        self.sketch_main_menu()
        self.draw_text('Path Finding', self.screen, [1200, 720], 28, WHITE, FONT, center=False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    self.algorithm_state = 'bfs'
                    self.state = 'grid window'
                if self.dfs_button.isOver(pos):
                    self.algorithm_state = 'dfs'
                    self.state = 'grid window'
                if self.astar_button.isOver(pos):
                    self.algorithm_state = 'astar'
                    self.state = 'grid window'
                if self.dijkstra_button.isOver(pos):
                    self.algorithm_state = 'dijkstra'
                    self.state = 'grid window'

            if event.type == pygame.MOUSEMOTION:
                if self.bfs_button.isOver(pos):
                    self.bfs_button.color = AQUAMARINE
                elif self.dfs_button.isOver(pos):
                    self.dfs_button.color = AQUAMARINE
                elif self.astar_button.isOver(pos):
                    self.astar_button.color = AQUAMARINE
                elif self.dijkstra_button.isOver(pos):
                    self.dijkstra_button.color = AQUAMARINE
                else:
                    self.set_algo_buttons_color(WHITE)

    def grid_events(self):
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            self.grid_window_buttons(pos, event)

    def draw_nodes(self):
        self.grid_button_keep_color()
        self.sketch_grid_buttons()
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.grid_window_buttons(pos, event)

            if 264 < pos[0] < 1512 and 24 < pos[1] < 744:
                x_grid_pos = (pos[0] - 264) // 24
                y_grid_pos = (pos[1] - 24) // 24

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_drag = 1

                    if self.state == 'draw S/E' and self.start_end_checker < 2:
                        # color and coordinates for start node
                        if self.start_end_checker == 0:
                            node_color = TOMATO
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            self.start_end_checker += 1
                        # color and coordinates for end node, making sure it's different from start node
                        elif self.start_end_checker == 1 \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_node_x, self.start_node_y):
                            node_color = ROYALBLUE
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                            self.start_end_checker += 1
                        else:
                            continue

                        # draw on the grid
                        pygame.draw.rect(self.screen, node_color, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_drag = 0

                # check to see if mouse drag is available to draw wall nodes
                if self.mouse_drag == 1:
                    # draw wall nodes and append them accordingly
                    # check for duplicates in the list and if they are overlapping start/end nodes
                    if self.state == 'draw walls':
                        if (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_pos \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_node_x, self.start_node_y) \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.end_node_x, self.end_node_y):

                            pygame.draw.rect(self.screen, BLACK, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)
                            self.wall_pos.append((x_grid_pos + 1, y_grid_pos + 1))

                for x in range(52):
                    pygame.draw.line(self.screen, ALICE, (GS_X + x * self.grid_square_length, GS_Y),
                                     (GS_X + x * self.grid_square_length, GE_Y))
                for y in range(30):
                    pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + y * self.grid_square_length),
                                     (GE_X, GS_Y + y * self.grid_square_length))

    def execute_algo(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # BFS
        if self.algorithm_state == 'bfs':
            self.bfs = BreadthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y,
                                    self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.bfs.bfs_execute()

            if self.bfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.bfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, center=True)

        # DFS
        elif self.algorithm_state == 'dfs':
            self.dfs = DepthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y,
                                  self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.dfs.dfs_execute()

            if self.dfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.dfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, center=True)

        # ASTAR
        elif self.algorithm_state == 'astar':
            self.astar = Astar(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y,
                               self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.astar.astar_execute()

            if self.astar.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y,
                                               None, self.astar.route)
                self.draw_path.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, center=True)

        # DIJKSTRA
        elif self.algorithm_state == 'dijkstra':
            self.dijkstra = Dijkstra(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y,
                                     self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.dijkstra.dijkstra_execute()

            if self.dijkstra.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y,
                                               None, self.dijkstra.route)
                self.draw_path.draw_path()

            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, center=True)

        pygame.display.update()
        self.state = 'aftermath'

    def reset_or_main_menu(self):
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.color = MINT
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.color = MINT
                elif self.reset_button.isOver(pos):
                    self.reset_button.color = MINT
                elif self.start_button.isOver(pos):
                    self.start_button.color = MINT
                elif self.main_menu_button.isOver(pos):
                    self.main_menu_button.color = MINT
                else:
                    self.set_menu_buttons_color(STEELBLUE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.isOver(pos):
                    self.execute_reset()
                elif self.main_menu_button.isOver(pos):
                    self.back_to_menu()
