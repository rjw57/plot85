from pi.graphics import *
from pi.maths import *

(w, h) = screen_size()

circle_centres = []
for i in range(0, 300):
	circle_centres.append((randomint(0, w), randomint(0, h)))

for r in range(100, 0, -4):
	foreground(255, 255-r, 255-r)
	for i in range(0, len(circle_centres)):
		(x, y) = circle_centres[i]
		circle(x, y, r)
		circle_centres[i] = (x + randomint(-10,10), y + randomint(-10, 10))

save_screen("tentacles")
