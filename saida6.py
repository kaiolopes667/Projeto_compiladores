import turtle
t = turtle.Turtle()
screen = turtle.Screen()
lado = 0
lado = 100
for _ in range(10):
    for _ in range(4):
        t.forward(lado)
        t.right(90)
    t.right(36)
turtle.done()
