import atexit
import pygame
import threading
import time
import traceback
import os
import sys

pygame.init()

class State(object):
	def __init__(self):
		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.events = []

		self.fore = pygame.Color(255, 255, 0)
		self.back = pygame.Color(0, 0, 137)

		# Text support
		self._sys_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), 'sysfont.ttf'), 20)
		self._text_cursor = (0, 0)
		self._sys_lh = self._sys_font.get_linesize()
		self._sys_em = self._sys_font.size('m')[0]
		self._cursor_save = pygame.Surface((self._sys_em, self._sys_lh))

	### TEXT IO	
	
	def _draw_cursor(self):
		tc_rect = (self._text_cursor[0], self._text_cursor[1], self._sys_em, self._sys_lh)
		self._cursor_save.blit(self.screen, (0,0), tc_rect)
		self.screen.fill(self.fore, tc_rect)
	
	def _undraw_cursor(self):
		self.screen.blit(self._cursor_save, self._text_cursor)
	
	def put_char(self, c):
		self._undraw_cursor()

		if c == u'\n' or c == u'\r':
			self._text_cursor = (0, self._text_cursor[1] + self._sys_lh)
		else:
			# Blit the character
			f = self._sys_font
			ts = f.render(c, False, self.fore, self.back)
			self.screen.blit(ts, self._text_cursor)

			# Advance the text cursor
			lh = self._sys_lh; em = self._sys_em
			tc = (self._text_cursor[0] + self._sys_em, self._text_cursor[1])

			# Will the next char be off to the right?
			if tc[0] + em > self.screen.get_width():
				tc = (0, tc[1] + lh)
			self._text_cursor = tc

		# Scroll the screen if necessary
		self._scroll_text_if_necessary()
		
		self._draw_cursor()

	def back_one_char(self):
		self._undraw_cursor()

		tc = (self._text_cursor[0] - self._sys_em, self._text_cursor[1])
		if tc[0] < 0:
			remainder = self.screen.get_width() % self._sys_em
			tc = (self.screen.get_width() - remainder - self._sys_em, tc[1] - self._sys_lh)
			if tc[1] < 0:
				tc = (0, 0)
		self._text_cursor = tc

		self._draw_cursor()

	def _scroll_text_if_necessary(self):
		tc = self._text_cursor
		lh = self._sys_lh

		# Scroll the screen if necessary
		while tc[1] + lh> self.screen.get_height():
			self.screen.scroll(0, -lh)
			self.screen.fill(self.back, (0, self.screen.get_height()-lh, self.screen.get_width(), lh))
			self._text_cursor = (tc[0], tc[1] - lh)
			return True

		return False

	### EVENT HANDLING
	
	def _new_events(self, evs):
		# Check for escape
		for e in evs:
			if e.type != pygame.KEYDOWN:
				continue
			if e.unicode == u'\x03' or e.unicode == u'\x1b':
				# Escape was pressed.
				write("Escaped")
				sys.exit(0)
		self.events.extend(evs)

	def pump(self):
		evs = pygame.event.get()
		if evs is not None:
			self._new_events(evs)

	def pump_wait(self):
		ev = pygame.event.wait()
		self._new_events([ev])

	def pop_event(self):
		self.pump()
		if len(self.events) > 0:
			e = self.events[0]
			self.events = self.events[1:]
			return e
		return None

	def wait_event(self):
		while len(self.events) == 0:
			self.pump_wait()
		return self.pop_event()

_s = State()

def __atexit():
	write("Press any key to exit.")
	getkey()
atexit.register(__atexit)

def _flip():
	global _s
	pygame.display.flip()
	_s.pump()

def screen_size():
	global _s
	return (_s.screen.get_width(), _s.screen.get_height())

def save_screen(name):
	global _s
	pygame.image.save(_s.screen, "%s.png" % (name,))

### TEXT SUPPORT
	
def write(s, no_line_break = False):
	global _s
	for c in s:
		_s.put_char(c)
	if not no_line_break:
		_s.put_char("\n")
	_flip()

### KEYBOARD INPUT

def gettext(prompt = None):
	global _s
	if prompt is not None:
		write(prompt, True)

	l = u""
	c = getkey()
	while c != u'\r':
		if c == u'\x7f' or c == u'\x08':
			if len(l) > 0:
				_s.back_one_char()
				_s.put_char(u' ')
				_s.back_one_char()
				l = l[:-1]
		else:
			l += c
			_s.put_char(c)
		_flip()
		c = getkey()
	_s.put_char(u'\r')
	_flip()

	return l

def getkey():
	"""Get a key from the keyboard and return it."""
	global _s
	while True:
		e = _s.wait_event()
		if e.type == pygame.KEYDOWN and len(e.dict["unicode"]) > 0:
			return e.dict["unicode"]

### DRAWING

def clear():
	"""Clear the screen to the current background colour."""
	global _s
	_s.screen.fill(_s.back)
	_flip()

def foreground(r, g, b):
	global _s
	_s.fore = pygame.Color(r, g, b)

def background(r, g, b):
	global _s
	_s.back = pygame.Color(r, g, b)

def line(x1, y1, x2, y2, width=1):
	global _s
	pygame.draw.line(_s.screen, _s.fore, (x1, y1), (x2, y2), width)
	_flip()

def rectangle(x, y, w, h, width=0):
	global _s
	pygame.draw.rect(_s.screen, _s.fore, pygame.Rect(x, y, w, h), width)
	_flip()

def circle(x, y, r, width=0):
	global _s
	pygame.draw.circle(_s.screen, _s.fore, (x, y), r, width)
	_flip()

# Initial setup
clear()
