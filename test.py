from pi.graphics import *
from pi.maths import *

(w, h) = screen_size()

for i in range(0, 200):
	foreground(randomint(0, 255), randomint(0, 255), randomint(0, 255))
	line(randomint(0, w), randomint(0, h))

for i in range(0, 20):
	foreground(randomint(0, 255), randomint(0, 255), randomint(0, 255))
	circle(randomint(0, w), randomint(0, h), randomint(10, 50))

for i in range(0,5):
	write("I've eaten " + str(i) + " sandwiches.")
write("Belurgh!!!")

foreground(255,255,0)
write("Hello, what is your name?")
foreground(255,0,0)
name = gettext("> ")
foreground(255,255,0)
write("Hello, " + name)

save_screen("test")
