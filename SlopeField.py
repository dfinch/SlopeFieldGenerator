from Tkinter import *
import math
import random
import Parser
import Calculator

### Globals ###
gridlines = True
ox = 300
oy = 300
pixelscale = 30
linesize = 30
    

# Base Tk object
root = Tk()

# Base canvas object
canvas = Canvas(root, width=600, height=700, background="gray95")
canvas.pack()

# Axis tick marks
for i in range(0, 10):
    d = pixelscale*i
    if(gridlines):
        canvas.create_line(0, oy-d, 600, oy-d, fill="pink")
        canvas.create_line(0, oy+d, 600, oy+d, fill="pink")
        canvas.create_line(ox-d, 0, ox-d, 600, fill="pink")
        canvas.create_line(ox+d, 0, ox+d, 600, fill="pink")
    canvas.create_line(ox-5, oy-d, ox+5, oy-d, fill="red")
    canvas.create_line(ox-5, oy+d, ox+5, oy+d, fill="red")
    canvas.create_line(ox-d, oy-5, ox-d, oy+5, fill="red")
    canvas.create_line(ox+d, oy-5, ox+d, oy+5, fill="red")

# Axes
canvas.create_line(0, 300, 600, 300, fill="red")
canvas.create_line(300, 0, 300, 600, fill="red")

# Control region
canvas.create_rectangle(0, 600, 600, 700, fill="gray75")

print("Parsing expression...")
RPNqueue = Parser.parseMathExpression("sin((x+y)/pi)")
print("Finished parsing expression.")

validEquation = False
if RPNqueue is not None:
    validEquation = Calculator.checkValid(RPNqueue)

if validEquation:
    lineradius = linesize / 2
    for j in range(-9, 10):
        for i in range(-9, 10):
            value = Calculator.evaluate(RPNqueue, i, j)
            angle = 0
            # Ensure that the value is a number
            if not math.isnan(value):
                # If the value is infinite, set the slope to vertical
                if math.isinf(value):
                    if value > 0:
                        angle = math.pi / 2
                    else:
                        angle = 3 * math.pi / 2
                # Otherwise set the slope angle based on the value
                else:
                    angle = math.atan2(value, 1)
                    
                xoff = lineradius * math.cos(angle)
                yoff = -lineradius * math.sin(angle)
                x1 = ox + i*pixelscale - xoff
                x2 = ox + i*pixelscale + xoff
                y1 = oy - j*pixelscale - yoff
                y2 = oy - j*pixelscale + yoff
                canvas.create_line(x1, y1, x2, y2, fill="blue")
                
else:
    print("SlopeField.py: Error: Equation is invalid.")

mainloop()
