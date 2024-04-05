"""Main entry for the snake game."""

from tkinter import Tk, Label, Canvas, ALL
import random

GAME_WIDTH: int = 400
GAME_HEIGHT: int = 600
speed: int = 100
MAX_SPEED: int = 20
SPACE_SIZE: int = 20
SNAKE_COLOR: str = "#00FF00"
FOOD_COLOR: str = "#FF0000"
BACKGROUND_COLOR: str = "#d5d5d5"
SCORE_TITLE_TEXT: str = "Score: {}"


class Snake:
    def __init__(self):
        self.body_size: int = 3
        self.coordinates: [] = []
        self.squares: [] = []

        for i in range(0, self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x,
                y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=SNAKE_COLOR,
                tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):
        self.place_food()

    def place_food(self):
        empty_squares = self.get_empty_squares()

        if empty_squares:
            x, y = random.choice(empty_squares)
            self.coordinates = [x, y]
            canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
        else:
            # If there are no empty squares, end the game
            game_over()

    def get_empty_squares(self):
        occupied_squares = []
        for item in canvas.find_withtag("snake"):
            coords = canvas.coords(item)
            occupied_squares.append((int(coords[0]), int(coords[1])))

        empty_squares = [
            (x, y)
            for x in range(0, GAME_WIDTH, SPACE_SIZE)
            for y in range(0, GAME_HEIGHT, SPACE_SIZE)
            if (x, y) not in occupied_squares
        ]
        return empty_squares

def game_loop(snake: Snake, food: Food):
    x, y = snake.coordinates[0]
    if init_direction == "up":
        y -= SPACE_SIZE
    elif init_direction == "down":
        y += SPACE_SIZE
    elif init_direction == "left":
        x -= SPACE_SIZE
    elif init_direction == "right":
        x += SPACE_SIZE
    else:
        raise Exception("Invalid direction")

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        score_label.config(text=SCORE_TITLE_TEXT.format(score))
        canvas.delete("food")
        food = Food()

        global speed

        if speed > MAX_SPEED:
            speed -= 5
        print(f"Score: {score}, Speed: {speed}")
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        window.after(speed, game_loop, snake, food)


def change_direction(new_direction: str):
    global init_direction

    if new_direction == "left" and init_direction != "right":
        init_direction = new_direction

    elif new_direction == "right" and init_direction != "left":
        init_direction = new_direction

    elif new_direction == "up" and init_direction != "down":
        init_direction = new_direction

    elif new_direction == "down" and init_direction != "up":
        init_direction = new_direction


def check_collision(snake: Snake) -> bool:
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font="helvetica 20 bold",
        text="GAME OVER",
        fill="red",
        tag="game_over"
    )
    window.bind("<Return>", lambda event: restart())


def restart(event=None):
    global score, init_direction, snake, food, speed
    speed = 100
    score = 0
    init_direction = 'down'
    score_label.config(text=SCORE_TITLE_TEXT.format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    game_loop(snake, food)


window: Tk = Tk()
window.title("Snake Game")
window.resizable(False, False)

score: int = 0
init_direction: str = 'down'

score_label = Label(
    window,
    text=SCORE_TITLE_TEXT.format(score),
    font=("Helvetica", 40),
)
score_label.pack()

canvas: Canvas = Canvas(
    window,
    bg=BACKGROUND_COLOR,
    width=GAME_WIDTH,
    height=GAME_HEIGHT)
canvas.pack()
window.update()

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake: Snake = Snake()
food: Food = Food()

game_loop(snake, food)
window.mainloop()
