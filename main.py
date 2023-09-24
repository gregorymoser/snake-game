from tkinter import *
import random

#constants for the game in capital letters
GAME_WIDTH = 1000
GAME_HEIGHT = 1000
# the lower the number, the faster the game
SPEED = 250
SPACE_SIZE = 50
BODY_PARTS = 5
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGORUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        # set the body size
        self.body_size = BODY_PARTS
        # list of coordinates
        self.coordinates = []
        # list of square graphics
        self.squares = []

        #creating the list of coordinates
        for i in range(0, BODY_PARTS):
            # coordinates for each snake part at the start of the game
            self.coordinates.append([0, 0])
        # creating some squares
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            # now we have a list of squares and we can append each square into our list
            self.squares.append(square)
            # now we have a snake that has a body size a list of graphs and a list of coordinates
class Food:
    # building class constructor -> Food object
    def __init__(self):
        # to convert into pixel, multiply by space size
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        # coordinates, list of x and y
        self.coordinates = [x, y]
        # creating food which is a random circle someplace at somespot on the game board 
        # starting and ending corner for canvas, color and tag to make it easier to delete this object
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    # unpacking the head of snake
    x, y = snake.coordinates[0]

    # y takes the head of the snake to up and down
    # x takes the head of the snake to left and right
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    
    # updating the coordinates for the height for the snake and write that before mooving to the next turn
    snake.coordinates.insert(0, (x,y))

    #creating a new graph for the head of the snake
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    # update snake's list of squares
    snake.squares.insert(0, square)

    # to check if the snake ate the food
    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()
    else:
        # delete the last body part of the snake if we not eat the food object
        del snake.coordinates[-1]

        # update canvas acordingly
        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
         # call the next turn funcion again
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    # access the direction
    global direction

    if new_direction == 'left':
         if direction != 'right':
             direction = new_direction
    elif new_direction == 'right':
         if direction != 'left':
             direction = new_direction
    elif new_direction == 'up':
         if direction != 'down':
             direction = new_direction
    elif new_direction == 'down':
         if direction != 'up':
             direction = new_direction

def check_collisions(snake):
    
    #unpacking the head of snake
    x, y = snake.coordinates[0]

    # check whether it has crossed the left or right border of the game
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    # what if snak touch itself in another body part
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
    
    return False      

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('Times New Roman', 70), text="GAME OVER", fill="red", tag="gameover")
# building the window
window = Tk()
window.title("Snake Game")
# to avoid window resizable
window.resizable(False, False)

# score and label to window
score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('Times New Roman', 40))
label.pack()

canvas = Canvas(window, bg=BACKGORUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# to show up in the center of the window
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenmmwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# setting the geometry
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# giving direction to snake
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# creating snake object and calling snake constructor
snake = Snake()
# creating food object and calling food constructor
food = Food()

# calling next turn funcition, passing snake and food
next_turn(snake, food)

window.mainloop()