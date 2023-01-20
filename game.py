from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font, Label, StringVar, IntVar, Entry, Button
import pygame
from time import perf_counter as my_timer
from datetime import datetime


def save_info():
    name_info = fullname.get()
    age_info = age.get()

    file = open("Player data.txt", "a")

    file.write("Name:" + name_info)

    file.write("\n")

    file.write("Age:" + str(age_info))

    file.write("\n")

    file.write("Date:" + date)

    file.write("\n")

    file.write("Time:" + start_time1)

    file.write("\n")
    file.close()
    data_screen.destroy()


data_screen = Tk()

now = datetime.now()
date = now.strftime("%B %d, %Y")
start_time1 = now.strftime("%H:%M:%S")

data_screen.geometry("300x250")
data_screen.title("Player Entry")
heading = Label(text='Enter Details', bg='turquoise1', fg='Black', width='300', font='10')
heading.pack()

fullname = Label(text="Name:", bg='turquoise1', fg='black', font='10')
age = Label(text='Age:', bg='turquoise1', fg='black', font='10')
fullname.place(x=15, y=50)
age.place(x=15, y=120)

fullname = StringVar()
age = IntVar()

fullname_entry = Entry(textvariable=fullname, bg='turquoise1', fg='black', width="15", font='10')
age_entry = Entry(textvariable=age, bg='turquoise1', fg='black', width="15", font='10')

fullname_entry.place(x=80, y=50)
age_entry.place(x=80, y=120)

save_button = Button(data_screen, text="Save", command=save_info, bg="turquoise1", width="30", height="2")
save_button.place(x=45, y=180)
data_screen.mainloop()

start_time = my_timer()
canvas_width = 1000
canvas_height = 500
root = Tk()
c = Canvas(root, width=canvas_width, height=canvas_height, background='deep sky blue')
c.create_rectangle(-5, canvas_height-100, canvas_width+5, canvas_height+5, fill='sea green', width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)
ball_drop_sound = pygame.mixer.Sound('drop.wav')
splash_sound = pygame.mixer.Sound('splash.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

# variable initialization
color_cycle = cycle(['red', 'light green', 'light pink', 'light yellow', 'orange'])
ball_width = 45
ball_height = 55
ball_score = 10
ball_speed = 300
ball_interval = 4000
difficulty_factor = 0.95

basket_color = 'brown'
basket_width = 100
basket_height = 100
basket_start_x = canvas_width/2 - basket_width/2
basket_start_y = canvas_height - basket_height-20
basket_start_x2 = basket_start_x + basket_width
basket_start_y2 = basket_start_y + basket_height

basket = c.create_arc(basket_start_x, basket_start_y, basket_start_x2, basket_start_y2, start=200, extent=140,
                      style='arc', outline=basket_color, width=10)
game_font = font.nametofont('TkFixedFont')
game_font.config(size=18)

score = 0
score_text = c.create_text(10, 10, anchor='nw', font=game_font, fill='dark blue', text='Score:'+str(score))

lives_remaining = 3
lives_text = c.create_text(canvas_width-1, 10, anchor='ne', font=game_font,
                           fill='dark blue', text='Lives '+str(lives_remaining))

balls = []           # empty list for adding balls


def create_ball():
    x = randrange(10, 940)
    y = 40
    new_ball = c.create_oval(x, y, x+ball_width, y+ball_height, fill=next(color_cycle), width=0)
    balls.append(new_ball)
    root.after(ball_interval, create_ball)


def move_balls():
    for ball in balls:
        (ball_x, ball_y, ball_x2, ball_y2) = c.coords(ball)
        c.move(ball, 0, 10)
        if ball_y2 > canvas_height:
            ball_dropped(ball)
    root.after(ball_speed, move_balls)


def ball_dropped(ball):
    balls.remove(ball)
    c.delete(ball)
    splash_sound.play()

    lose_a_life()
    if lives_remaining == 0:
        game_over_sound.play()
        end_time = my_timer()
        duration = end_time - start_time
        c.destroy()
        after_loss_life(duration)


def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text='Lives: '+str(lives_remaining))


def check_catch():
    (basket_x, basket_y, basket_x2, basket_y2) = c.coords(basket)
    for ball in balls:
        (ball_x, ball_y, ball_x2, ball_y2) = c.coords(ball)
        if basket_x < ball_x and ball_x2 < basket_x2 and basket_y2 - ball_y2 < 40:
            ball_drop_sound.play()

            balls.remove(ball)
            c.delete(ball)
            increase_score(ball_score)
    root.after(100, check_catch)


def after_loss_life(duration):

    file = open("Player data.txt", 'a')
    file.write("Duration:" + str(duration) + "sec")
    file.write("\n")
    file.write("Score:" + str(score))
    file.write("\n")
    file.write("-"*80)
    file.write("\n")
    file.close()
    messagebox.showinfo('Game Over!', 'Final Score: '+str(score)+"\nDuration:"+str(round(duration, 2))+"sec")
    root.destroy()


def increase_score(points):
    global score, ball_speed, ball_interval
    score += points
    ball_speed = int(ball_speed * difficulty_factor)
    ball_interval = int(ball_interval * difficulty_factor)
    c.itemconfigure(score_text, text='Score: '+str(score))


def move_left(events):
    (x1, y1, x2, y2) = c.coords(basket)
    if x1 > 0:
        c.move(basket, -20, 0)


def move_right(events):
    (x1, y1, x2, y2) = c.coords(basket)
    if x2 < canvas_width:
        c.move(basket, 20, 0)


c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.focus_set()

root.after(1000, create_ball)
root.after(1000, move_balls)
root.after(1000, check_catch)

root.title("Ball basket Game")
root.mainloop()
