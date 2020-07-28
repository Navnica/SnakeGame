import pygame
import random

pygame.init()

def setDefault():
    global snake,fruits,side,objects,fps,score,gameOver,run

    pygame.display.set_caption('SnakeGame by TruEnot')

    snake = {
        'color': (0, 255, 0),
        0: [resolution[0] // 2 - 10, resolution[1] // 2 - 10],
    }

    fruits = {
        'color': (255, 0, 0),
        'keys': []
    }

    side = 'up'
    objects = [snake, fruits]
    fps = 15
    score = 1
    gameOver = False
    run = True

def drawAll():
    screen.fill((0, 0, 0))

    for obj in objects:
        for pad in obj:
            if not str(pad).isdigit():
                continue

            pygame.draw.rect(screen, obj['color'], (obj[pad][0], obj[pad][1], 10, 10))

    pygame.display.update()

def snakeMove():
    if gameOver:
        return

    oldSnake = dict(snake)

    if side == 'up' or side == 'down':
        snake.update({0 : [snake[0][0],snake[0][1] + sides[side] * 10]})
    else:
        snake.update({0 : [snake[0][0] + sides[side] * 10,snake[0][1]]})

    for pad in snake:
        if pad == 'color' or pad == 0:
            continue

        snake[pad] = oldSnake[pad-1]

def fruitGenerate():
    if gameOver:
        return

    chance = random.randint(0,100)

    x = random.randint(0,resolution[0])
    y = random.randint(0,resolution[1])

    x += 10 - x % 100 % 10
    y += 10 - y % 100 % 10

    if len(fruits) == 2 and chance in range(50,55) or len(fruits) in range(3,5) and chance == 50:
        while True:
            fruitID = random.randint(0,10**10)
            if not fruitID in fruits['keys']:
                fruits['keys'].append(fruitID)
                fruits.update({fruitID : [x,y]})
                break


resolution = (800, 600)

if str(resolution[0])[1:] != '00' or str(resolution[1])[1:] != '00':exit()

pygame.display.set_caption('SnakeGame by TruEnot')
screen = pygame.display.set_mode(resolution)

sides = {
    'up': -1,
    'down': 1,
    'left': -1,
    'right': 1
}

setDefault()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if gameOver:
        pygame.display.set_caption('Game over | Press R for game again')
    
    pygame.time.Clock().tick(fps)
    drawAll()
    snakeMove()
    fruitGenerate()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        setDefault()
    elif keys[pygame.K_UP]:
        side = 'up' if side != 'down' else side
    elif keys[pygame.K_DOWN]:
        side = 'down' if side != 'up' else side
    elif keys[pygame.K_LEFT]:
        side = 'left' if side != 'right' else side
    elif keys[pygame.K_RIGHT]:
        side = 'right' if side != 'left' else side

    for fruit in fruits:
        if not str(fruit).isdigit():
            continue

        if snake[0] == fruits[fruit]:
            fruits.pop(fruit)
            snake.update({len(snake) - 1 : [resolution[0]+10,resolution[1]+10]})
            score += 1
            fps = 15 + score // 10

            pygame.display.set_caption(f'Score: {score} | Game speed : {fps}')

            break

    for pad in snake:
        if not str(pad).isdigit() or pad == 0:
            continue

        if snake[0] == snake[pad]:
            gameOver: bool = True

    if snake[0][0] > resolution[0] - 1:
        snake[0][0] = 0

    if snake[0][0] < 0:
        snake[0][0] = resolution[0] - 10

    if snake[0][1] > resolution[1] - 1:
        snake[0][1] = 0

    if snake[0][1] < 0:
        snake[0][1] = resolution[1] - 10


pygame.quit()
