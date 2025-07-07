import turtle
t = turtle.Turtle()
screen = turtle.Screen()
lado = 0
cor = 0
lado = 5
screen.bgcolor("black")
t.pensize(2)
t.goto(0, 0)
for _ in range(50):
    t.pencolor("cyan")
    t.forward(lado)
    t.right(90)
    lado = (lado + 5)
turtle.done()
