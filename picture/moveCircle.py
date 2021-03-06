from tkinter import *

class GUI(Frame):
    def __init__(self, param):
        Frame.__init__(self, None)
        self.grid()

        global canvas
        # Check if parameter is the right type, because we can't
        # overload functions
        if isinstance(param, tuple) and len(param) == 2:
            canvas = Canvas(self, width=param[0], height=param[1], background="white")
            canvas.grid()
        elif isinstance(param, str):
            self.image = PhotoImage(file=param)
            canvas = Canvas(self, width=self.image.width(), height=self.image.height())
            canvas.grid()
            canvas.create_image(0, 0, image=self.image, anchor=NW)
        else:
            raise TypeError('Parameter to GUI() should be a string of a .gif/pgm/ppm file name or 2-tuple!')

        global penColor
        penColor = "black"

        global penWidth
        penWidth = 1

    def drawCircle(self, x, y, r):
        circle = Circle(x, y, r)
        return circle

class Shape:
    def __init__(self, vertices):
        self.vertices = vertices
        self.my_shape = None

    def getLocation(self):
        return (self.vertices[0][0], self.vertices[0][1])

class Circle(Shape):
    def __init__(self, x, y, r):
        Shape.__init__(self, [[x-r,y-x], [x+r, y+r]])
        self.my_shape = canvas.create_oval(x-r, y-r, x+r, y+r, fill=penColor)

def moveby(shape, dx, dy):
    canvas.move(shape.my_shape, dx, dy)
    for point in shape.vertices:
        point[0] = point[0] + dx
        point[1] = point[1] + dy

def moveto(shape, x, y):
    [a, b] = shape.vertices[0]
    dx = x - a
    dy = y - b
    moveby(shape, dx, dy)

def display():
    canvas.update()

def delay(millisecond):
    canvas.after(millisecond)

#Show circles at initial position for 2 secs, then move diagonally. 
def main():
    window = GUI((500, 500))
    circle1 = window.drawCircle(20, 20, 10)
    circle2 = window.drawCircle(480, 20, 10)
    display()
    delay(2000)
    for x in range(0, 470):
        moveby(circle1, 1, 1)
        moveto(circle2, circle2.getLocation()[0]-1, circle2.getLocation()[1]+1)
        display()
        delay(20)
    window.mainloop()

main()
