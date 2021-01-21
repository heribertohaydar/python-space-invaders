import turtle
from math import sqrt
from math import pow

board = turtle.Screen()
board.bgcolor("black")
board.title("Space Invaders")

#Draw border
border_pn = turtle.Turtle()
border_pn.hideturtle()
border_pn.speed(0)
border_pn.color("white")
border_pn.penup()
border_pn.setposition(-300,-300)
border_pn.pendown()
border_pn.pensize(3)

for side in range(4):
    border_pn.forward(600)
    border_pn.left(90)


#Create the player turtle
player = turtle.Turtle()
player.color("black")
player.hideturtle()
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)
player.showturtle()
player.color("blue")
playerspeed  = 15

#Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()
bulletspeed = 15
bulletstate = "ready"

#Create enemy
enemy = turtle.Turtle()
enemy.shape("circle")
enemy.color("black")
enemy.hideturtle()
enemy.speed(0)
enemy.penup()
enemy.setposition(-200,-200)
enemy.color("red")
enemy.showturtle()
enemyspeed = 1.3

#Move the player left and righ
def move_left():
    x = player.xcor()
    x = x - playerspeed
    if x > -280 : player.setx(x)

def move_right():
    x = player.xcor()
    x = x + playerspeed
    if x < 280 : player.setx(x)

def shoot_enemy():
    global bulletstate
    bulletstate = "fire"
    bullet.setposition(player.xcor(), player.ycor()+15)
    bullet.showturtle()

#https://www.mathsisfun.com/algebra/distance-2-points.html
def distance(Xa,Ya, Xb,Yb):
    return sqrt(pow(Xa-Xb,2) + pow(Ya-Yb,2))

def isCollision(t1,t2):
    return True if distance(t1.xcor(),t1.ycor(),t2.xcor(),t2.ycor()) < 15 else False

def run_game():
    #Main loop
    while True:
        global enemyspeed
        global bulletstate
        #Move the enemy
        x = enemy.xcor()
        y = enemy.ycor()
        if (x > 280 or x < -280): 
            enemyspeed *= -1
            y -= 40
            enemy.sety(y)
        #Set x position for enemy
        enemy.setx(x + enemyspeed)

        #Shoot the enemy
        #Move the bullet
        if bulletstate == "fire" :
            y = bullet.ycor()
            y += bulletspeed
            bullet.sety(y)

        #Check to see if the bullet has gone to the top
        if bullet.ycor() > 275 :
            bullet.hideturtle()
            bulletstate = "ready"

        #Check if bullet shoot the enemy
        if isCollision(enemy, bullet) :
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0,-300)
            enemy.setposition(-200,250)
            enemy.color("gray")

        #Check if enemy reach theplayer
        if isCollision(enemy, player) :
            player.hideturtle()
            enemy.hideturtle()
            pen = turtle.Turtle()
            pen.penup()
            pen.color("green")
            pen.hideturtle()            
            pen.setposition(-150, 0)
            pen.write("Game over, you suck!..¡Try again!", True, align="left", font =("Arial", 14, "bold"))

#Create keyboard bindings
board.listen()
board.onkeypress(move_left, "Left")
board.onkeypress(move_right, "Right")       
board.onkeypress(shoot_enemy, "space")       
#board.mainloop()

if __name__ == '__main__':
    run_game()