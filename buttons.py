from settings import *


class Button:
    def __init__(self, app, color, x, y, width, height, text=''):
        self.app = app
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_button(self, outline=None):
        if outline:
            pygame.draw.rect(self.app.screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(self.app.screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(FONT, 28)
            text = font.render(self.text, 1, (0, 0, 0))
            self.app.screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                                        self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # pos is the mouse position or tuple of (x, y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
