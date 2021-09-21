import pygame
import random

height1 = 650
width1 = 600
width2 = 300
height2 = 600
block_size = 30
win = pygame.display.set_mode((width1, height1))
pygame.display.set_caption("try")
fps = 30
X = 150
Y = 50
a = [[".....",
      ".....",
      "..00.",
      ".00..",
      "....."],
     [".....",
      "..0..",
      "..00.",
      "...0.",
      "....."]]
b = [[".....",
      ".....",
      ".00..",
      "..00.",
      "....."],
     [".....",
      "..0..",
      ".00..",
      ".0...",
      "....."]]
c = [[".....",
      ".....",
      "0000.",
      ".....",
      "....."],
     ["..0..",
      "..0..",
      "..0..",
      "..0..",
      "....."]]
e = [[".....",
      ".....",
      "..00.",
      "..00.",
      "....."]]
f = [[".....",
      "..0..",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..0..",
      "..00.",
      "..0..",
      "....."],
     [".....",
      ".....",
      ".000.",
      "..0..",
      "....."],
     [".....",
      "..0..",
      ".00..",
      "..0..",
      "....."]]
g = [[".....",
      "..0..",
      "..0..",
      "..00.",
      "....."],
     [".....",
      ".....",
      ".000.",
      ".0...",
      "....."],
     [".....",
      ".00..",
      "..0..",
      "..0..",
      "....."],
     [".....",
      "...0.",
      ".000.",
      ".....",
      "....."]]

shapes = [a, b, c, e, f, g]
colors = [(0, 255, 125), (121, 169, 196), (0, 200, 0), (81, 75, 156), (201, 95, 1), (69, 210, 66)]


class things(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = colors[shapes.index(shape)]
        self.rotation = 0


def make_grid(locked_posit={}):
    grid = [[(0, 0, 0)for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_posit:
                z = locked_posit[(j, i)]
                grid[i][j] = z

    return grid


def draw_grid(win, grid):
    for i in range(len(grid)):
        pygame.draw.line(win, (100, 100, 100), (X, 50 + i*30), (450, Y + i*30))
        for j in range(len(grid[i])):
            pygame.draw.line(win, (100, 100, 100), (X + j*30, Y), (X + j*30, 650))


def draw_win(win, grid):
    win.fill((0, 0, 0))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(win, grid[i][j], (X + j*30, Y + i*30, 30, 30), 0)
    pygame.draw.rect(win, (255, 0, 0), (X, Y, width2, height2), 4)
    draw_grid(win, grid)


def get_shape():
    return things(5, 0, random.choice(shapes))


def spin_shape(shape):
    posit = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                posit.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(posit):
        posit[i] = (pos[0] - 2, pos[1] - 4)

    return posit


def good_spot(shape, grid):
    good_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)]for i in range(20)]
    gooder_pos = [j for sub in good_pos for j in sub]
    sponed = spin_shape(shape)
    for pos in sponed:
        if pos not in gooder_pos:
            if pos[1] > -1:
                return False
    return True


def lost(posit):
    for pos in posit:
        x, y = pos
        if y < 1:
            return True
    return False


def show_next(shape, win):
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(win, shape.color, (460 + j*30, 300 + i*30, 30, 30), 0)


def full(grid, locked):
    n = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            n += 1
            o = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if n > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < o:
                new = (x, y + n)
                locked[new] = locked.pop(key)


def main():
    locked_posit = { }
    grid = make_grid(locked_posit)
    change_thing = False

    thing = get_shape()
    next_thing = get_shape()
    timer = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    run = True
    while run:
        grid = make_grid(locked_posit)

        fall_time += timer.get_rawtime()

        timer.tick(fps)
        if fall_time/1000 > fall_speed:
            fall_time = 0
            thing.y += 1
            if not (good_spot(thing, grid)) and thing.y > 0:
                thing.y -= 1
                change_thing = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    thing.x -= 1
                    if not good_spot(thing, grid):
                        thing.x += 1

                if event.key == pygame.K_d:
                    thing.x += 1
                    if not good_spot(thing, grid):
                        thing.x -= 1

                if event.key == pygame.K_s:
                    thing.y += 1
                    if not good_spot(thing, grid):
                        thing.y -= 1

                if event.key == pygame.K_SPACE:
                    thing.rotation += 1
                    if not good_spot(thing, grid):
                        thing.rotation -= 1
        shape_pos = spin_shape(thing)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = thing.color
        if change_thing:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_posit[p] = thing.color

            thing = next_thing
            next_thing = get_shape()
            change_thing = False
            full(grid, locked_posit)

        if lost(locked_posit):
            run = False
            print("lost")

        draw_win(win, grid)
        show_next(next_thing, win)
        pygame.display.update()


if __name__ == "__main__":
    main()
