import turtle

def petal(t, r, angle):
    for i in range(2):
        t.circle(r, angle)
        t.left(180-angle)


def flower(t, n, r, angle):
    for i in range(n):
        petal(t, r, angle)
        t.left(360.0/n)


def move(t, lenght):
    window = turtle.Screen()
    window.bgcolor("Yellow")
    t.pu()
    t.fd(lenght)
    t.pd()


sam = turtle.Turtle()

sam.speed(11)

sam.color("green")
sam.shape("turtle")
move(sam, -150)
sam.begin_fill()
flower(sam, 7, 60.0, 60.0)
sam.end_fill()

sam.color('red')
move(sam, 150)
flower(sam, 10, 40.0, 80.0)

sam.color('blue')
move(sam, 150)
sam.begin_fill()
flower(sam, 14, 70.0, 50.0)
sam.end_fill()

turtle.done()
