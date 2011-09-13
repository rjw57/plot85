from pi.graphics import *
from pi.maths import *
from math import *

def draw_polygon(sides):
	w, h = screen_size()

	centre_x = w / 2
	centre_y = h / 2

	radius = min(w, h) * 0.4

	angle_per_side = 360.0 / sides
	move(centre_x, centre_y + radius)
	for side in range(1, sides + 2):
		deg_angle = angle_per_side * side
		angle = 2.0 * 3.14159 * deg_angle / 360.0
		move(centre_x, centre_y)
		foreground(randomint(0,255), randomint(0,255), randomint(0,255))
		triangle(centre_x + radius * sin(angle), centre_y + radius * cos(angle))
	
foreground(255,255,0)
while True:
	clear()
	sides = int(gettext("Number of sides: "))
	clear()
	if sides < 2:
		write("Must be more than one side")
	else:
		draw_polygon(sides)
	save_screen("polygon")
	foreground(255,255,0)
	write("Press any key")
	getkey()
