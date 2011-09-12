from pi.graphics import *
from pi.maths import *

last = (0, 0)
for i in range(0, 200):
	new = (randomint(0, 720), randomint(0, 576))
	foreground(randomint(0, 255), randomint(0, 255), randomint(0, 255))
	line(last[0], last[1], new[0], new[1])
	last = new

for i in range(0, 200):
	new = (randomint(0, 720), randomint(0, 576))
	foreground(randomint(0, 255), randomint(0, 255), randomint(0, 255))
	rectangle(last[0], last[1], new[0], new[1])
	last = new

for i in range(0, 20):
	foreground(randomint(0, 255), randomint(0, 255), randomint(0, 255))
	circle(randomint(0, 720), randomint(0, 576), randomint(10, 50))

for i in range(0,5):
	write("I've eaten " + str(i) + " sandwiches.")
write("Belurgh!!!")

foreground(255,255,0)
write("Hello, what is your name?")
foreground(255,0,0)
name = gettext("> ")
foreground(255,255,0)
write("Hello, " + name)
