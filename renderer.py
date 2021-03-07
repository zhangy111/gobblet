import pygame

class Renderer:

    GRAY = (200, 200, 200)
    BLACK = (128, 51, 0)
    WHITE = (255, 194, 153)

    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.start_vis()

    def start_vis(self):  # setup pygame
        pygame.init()
        pygame.display.set_caption("Gobblet!")
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_width))  # set canvas

    def draw_grid(self, board):
        pygame.display.flip()  # refresh buffer
        gap = self.screen_width // (board.size + 2)

        # draw grid
        x = 0
        y = 0
        for i in range(1, board.size + 2):
            x = i * gap
            pygame.draw.line(self.screen, self.GRAY, (x, gap), (x, self.screen_width - gap), 3)
            pygame.draw.line(self.screen, self.GRAY, (gap, x), (self.screen_width - gap, x), 3)

    def draw_pieces(self, board):
        pygame.display.flip()  # refresh buffer
        # add pieces
        gap = self.screen_width // (board.size + 2)
        for pos, stack in board.board.items():
            if len(stack) == 0:
                continue
            circle_center = tuple(gap * (i+1) - gap//2 for i in pos)
            for piece in stack:
                circle_color = self.WHITE if piece[0] == 'white' else self.BLACK
                radius = (piece[1] / board.size) * (gap // 3)
                pygame.draw.circle(self.screen, circle_color,
                                   circle_center, int(radius), 3)
        pygame.display.flip()

    def draw_board(self, board):
        self.screen.fill((0,0,0))
        self.draw_grid(board)
        self.draw_pieces(board)

    def __exit__(self):  # housekeeping
        pygame.quit()
