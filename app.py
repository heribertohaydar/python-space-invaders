import turtle
import random
from math import sqrt
from math import pow
from playsound import playsound
import threading

#Create turtles
player = None
bullet = None
board = None
score_pen = None
start_pen = None

def getTurtles():
    global player, bullet, board, score_pen, start_pen
    player = turtle.Turtle()
    bullet = turtle.Turtle()
    board = turtle.Screen()
    score_pen = turtle.Turtle()
    start_pen = turtle.Turtle()

#Initialize global properties for components
score = 0
bulletspeed = 15
playerspeed  = 15
number_of_enemies = 30
enemyspeed = 15
enemies = []

#Move the player left and righ
def move_left():
    threading.Thread(target=move_left_thread).start()

def move_left_thread():
    global player, playerspeed
    x = player.xcor()
    x = x - playerspeed
    if x > -280 : player.setx(x)

def move_right():
    threading.Thread(target=move_right_thread).start()

def move_right_thread():
    global player, playerspeed
    x = player.xcor()
    x = x + playerspeed
    if x < 280 : player.setx(x)

def shoot_enemy():
    threading.Thread(target=bullet_Thread).start()

def sound(file):
    playsound(file)

def bullet_Thread():
    global bullet, score
    bullet.setposition(player.xcor(), player.ycor()+15)
    bullet.showturtle()
    threading.Thread(target=sound, args=("laser.wav",)).start()
    while bullet.ycor() < 275:
        bullet.sety(bullet.ycor() + bulletspeed)
        for enemy in enemies:
            if enemy.isvisible() and isCollision(enemy, bullet) :
                bullet.hideturtle()
                threading.Thread(target=sound, args=("invaderkilled.wav",)).start()
                bullet.hideturtle()
                bullet.setposition(0,300)
                score += 10
                score_pen.color("white")
                score_pen.clear()
                enemy.hideturtle()
                score_pen.write("Score : {:03d}".format(score), False, align="left", font=("Arial", 14, "bold"))
                break
    bullet.hideturtle()

def build_board():
    global board
    board.bgcolor("black")
    board.title("Space Invaders")
    board.bgpic("space.gif")
    board.register_shape("invader.gif")
    board.register_shape("player.gif")
    board.register_shape("bullet.gif")

    #Draw border
    border_pn = turtle.Turtle()
    border_pn.hideturtle()
    border_pn.speed(0)
    border_pn.penup()
    border_pn.setposition(-300,-300)
    border_pn.pendown()
    border_pn.pensize(3)

    for _ in range(4):
        border_pn.forward(600)
        border_pn.left(90)

    board.listen()
    board.onkeypress(move_left, "Left")
    board.onkeypress(move_right, "Right")       
    board.onkeypress(shoot_enemy, "space")       
    board.onkeypress(run_game, "Return")       

def build_score():
    global score_pen
    score_pen.hideturtle()
    score_pen.color("white")
    score_pen.penup()
    score_pen.setposition(-290,260)
    score_pen.speed(0)
    score_pen.write("Score : {:03d}".format(score), False, align="left", font=("Arial", 14, "bold"))

def build_player():
    global player, start_pen
    player.hideturtle()
    player.shape("player.gif")
    player.penup()
    player.speed(0)
    player.setposition(0,-250)
    player.setheading(90)
    player.showturtle()
    start_pen.penup()
    start_pen.setposition(-100,0)
    start_pen.color("white")
    start_pen.hideturtle()
    start_pen.write("Press <Enter> to start.", False, align="left", font=("Arial", 14, "bold"))

def build_bullet():
    global bullet
    bullet.hideturtle()
    bullet.shape("bullet.gif")
    bullet.penup()
    bullet.speed(0)
    bullet.setheading(90)
    bullet.shapesize(0.5, 0.5)

def build_enemy_army():
    global enemies

    #Start x,y position 
    enemy_x_pos = -240
    enemy_y_pos = 250

    for _ in range(number_of_enemies):
        enemies.append(turtle.Turtle())

    for idx, enemy in enumerate(enemies):
        enemy.hideturtle()
        enemy.speed(0)
        enemy.penup()
        if (idx % 10) == 0 :
            enemy_x_pos = -240
            enemy_y_pos -= 40
        else:
            enemy_x_pos += 50
        enemy.setposition(enemy_x_pos, enemy_y_pos)
        enemy.showturtle()
        enemy.shape("invader.gif")


#https://www.mathsisfun.com/algebra/distance-2-points.html
def distance(Xa,Ya, Xb,Yb):
    return sqrt(pow(Xa-Xb,2) + pow(Ya-Yb,2))

def isCollision(t1,t2):
    d = distance(t1.xcor(),t1.ycor(),t2.xcor(),t2.ycor())
    return True if d < 15 else False

def run_game():
    threading.Thread(target=run_game_thread).start()

def run_game_thread():
    global enemyspeed, score, bullet, player, enemy, enemyspeed, start_pen
    start_pen.hideturtle()
    start_pen.clear()
    #Main loop
    while True:
        #Move the enemy
        for enemy in enemies:
            #Move the enemy
            enemy.setx(enemy.xcor() + enemyspeed)
            #Move the enemy back and down
            if ( enemy.xcor() > 280 or enemy.xcor() < -280):
                #Change enemy direction
                enemyspeed *= -1
                #Fix position
                enemy.setx(280 if enemy.xcor() > 280 else -280)
                #Move all enemies down
                for e in enemies:
                    e.sety(e.ycor()-15)
                threading.Thread(target=sound, args=("fastinvader4.wav",)).start()
                
            if isCollision(enemy, player) :
                threading.Thread(target=sound, args=("explosion.wav",)).start()
                player.hideturtle()
                enemy.hideturtle()
                pen = turtle.Turtle()
                pen.penup()
                pen.color("white")
                pen.hideturtle()            
                pen.setposition(-80, 0)
                pen.write("Game over.", False, align="left", font =("Arial", 14, "bold"))

def game():
    global board
    getTurtles()
    build_board()
    build_score()
    build_enemy_army()
    build_player()
    build_bullet()
    board.exitonclick()

if __name__ == '__main__':
    threading.Thread(target=game).start()    