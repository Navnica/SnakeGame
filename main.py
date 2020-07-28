import pygame
import random
import pkg_resources.py2_warn

pygame.init()

def setDefault():
    global snake,fruits,side,objects,fps,score,gameOver,run,fruitColors

    pygame.display.set_caption('SnakeGame by TruEnot')

    snake = {
        'colors' : {0 : (0,255,0)},
        0 : [resolution[0] // 2 - 10,resolution[1] // 2 - 10]
    }

    fruits = {
        'keys': []
    }

    fruitColors = {
        0 : (255,0,0),
        1 : (255,255,0),
        2 : (0,0,255)
    }

    side = 'up'
    fps = 15
    score = 1
    gameOver = False
    run = True

def drawAll():
    screen.fill((0, 0, 0))

    for obj in snake:
        if not str(obj).isdigit():
            continue

        pygame.draw.rect(screen,snake['colors'][obj],(snake[obj][0],snake[obj][1],10,10))

    for fruit in fruits:
        if not str(fruit).isdigit():
            continue

        pygame.draw.rect(screen,fruits[fruit]['color'],(fruits[fruit]['position'][0],fruits[fruit]['position'][1],10,10))


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
        if pad == 0 or not str(pad).isdigit():
            continue

        snake[pad] = oldSnake[pad - 1]

def fruitGenerate():
    if gameOver:
        return

    chance = random.randint(0,100)

    x = random.randint(0,resolution[0])
    y = random.randint(0,resolution[1])

    x += 10 - x % 100 % 10
    y += 10 - y % 100 % 10

    if len(fruits) == 1 and chance in range(50,55) or len(fruits) in range(2,4) and chance == 50:
        while True:
            fruitID = random.randint(0,10**10)
            fruitColor = fruitColors[random.randint(0,2)]
            if not fruitID in fruits['keys']:
                fruits['keys'].append(fruitID)
                fruits.update({fruitID : {'position' : [x,y],'color' : fruitColor}})
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

        if snake[0] == fruits[fruit]['position']:

            l = len(snake) - 1
            snake.update({l : [resolution[0]+10,resolution[1]+10]})
            snake['colors'].update({l : fruits[fruit]['color']})

            fruits.pop(fruit)
            score += 1
            fps = 15 + score // 10

            pygame.display.set_caption(f'Score: {score} | Game speed : {fps}')

            break

    for pad in snake:
        if not str(pad).isdigit() or pad == 0:
            continue

        if snake[0] == snake[pad]:
            gameOver = True


    if snake[0][0] > resolution[0] - 1:
        snake[0][0] = 0

    if snake[0][0] < 0:
        snake[0][0] = resolution[0] - 10

    if snake[0][1] > resolution[1] - 1:
        snake[0][1] = 0

    if snake[0][1] < 0:
        snake[0][1] = resolution[1] - 10

pygame.quit()
