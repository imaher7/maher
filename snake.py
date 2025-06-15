import curses
from random import randint

# Initialize the screen
stdscr = curses.initscr()
curses.curs_set(0)  # Hide cursor
height, width = 20, 60
window = curses.newwin(height, width, 0, 0)
window.keypad(1)
window.nodelay(1)  # Non-blocking input
window.border(0)

# Initial snake and food positions
snake = [[height//2, width//4 + i] for i in range(3)][::-1]  # Starting length 3
food = [randint(1, height-2), randint(1, width-2)]
window.addch(food[0], food[1], '*')

# Directions: 0=right, 1=left, 2=up, 3=down
key = curses.KEY_RIGHT

def move(head, direction):
    y, x = head
    if direction == curses.KEY_RIGHT:
        x += 1
    elif direction == curses.KEY_LEFT:
        x -= 1
    elif direction == curses.KEY_UP:
        y -= 1
    elif direction == curses.KEY_DOWN:
        y += 1
    return [y, x]

try:
    score = 0
    while True:
        window.border(0)
        window.addstr(0, 2, f'Score: {score} ')
        window.timeout(100)
        next_key = window.getch()
        if next_key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            key = next_key
        head = move(snake[0], key)
        snake.insert(0, head)

        # Check for collisions
        if (head[0] in [0, height-1] or
            head[1] in [0, width-1] or
            head in snake[1:]):
            break

        # Check food
        if head == food:
            score += 1
            food = None
            while food is None:
                nf = [randint(1, height-2), randint(1, width-2)]
                if nf not in snake:
                    food = nf
            window.addch(food[0], food[1], '*')
        else:
            tail = snake.pop()
            window.addch(tail[0], tail[1], ' ')

        window.addch(head[0], head[1], '#')

except KeyboardInterrupt:
    pass
finally:
    curses.endwin()
    print(f'Final score: {score}')
