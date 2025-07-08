import turtle
t = turtle.Turtle()
screen = turtle.Screen()
i = 0
nome = 0
raio = 0
nome = "Flor"
raio = 60
screen.bgcolor("white")
t.pencolor("magenta")
t.pensize(2)
t.goto(0, 0)
turtle.time.sleep(1)
for _ in range(6):
    for _ in range(36):
        t.forward(10)
        t.left(10)
    t.left(60)
    turtle.time.sleep(1)
t.pencolor("cyan")
t.right(90)
t.penup()
t.forward(110)
t.pendown()
t.forward(120)
t.penup()
t.forward(20)
t.pendown()
t.write(nome)
t.penup()
t.backward(250)
turtle.time.sleep(10)
t.clear()
turtle.done()
