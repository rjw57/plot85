from pi.graphics import *

(w, h) = screen_size()

# The starting corners of the squares

x1 = 0
y1 = 0

x2 = w-1
y2 = 0

x3 = w-1
y3 = h-1

x4 = 0
y4 = h-1

twist = 0.05

for i in range(0, 200):
	# Draw the current square
	move(x1, y1)
	line(x2, y2)
	line(x3, y3)
	line(x4, y4)
	line(x1, y1)

	# Work out the new co-ordinates
	new_x1 = twist * x2 + (1 - twist) * x1
	new_y1 = twist * y2 + (1 - twist) * y1
	new_x2 = twist * x3 + (1 - twist) * x2
	new_y2 = twist * y3 + (1 - twist) * y2
	new_x3 = twist * x4 + (1 - twist) * x3
	new_y3 = twist * y4 + (1 - twist) * y3
	new_x4 = twist * x1 + (1 - twist) * x4
	new_y4 = twist * y1 + (1 - twist) * y4

	# Make use of the new co-ordinates
	x1 = new_x1
	y1 = new_y1
	x2 = new_x2
	y2 = new_y2
	x3 = new_x3
	y3 = new_y3
	x4 = new_x4
	y4 = new_y4

save_screen("tunnel")
