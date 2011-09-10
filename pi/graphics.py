import atexit
import pygame
import threading
import traceback
import os
import sys

class EventThread(threading.Thread):
	def _handle_event(self, e):
		if e.type == pygame.KEYDOWN:
			if e.dict['unicode'] == u'\x1b' or e.dict['unicode'] == u'\x03':
				os._exit(0)
			elif self.key_handler is not None:
				self.key_handler(e)

	def run(self):
		self.escape_pressed = False
		self.carry_on = True
		self.key_handler = None
		while self.carry_on:
			try:
				self._handle_event(pygame.event.wait())
			except:
				print traceback.format_exc()

class Graphics(object):
	def __init__(self):
		pygame.init()

		#self._screen = pygame.display.set_mode((720, 576))
		self._screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

		self._forecol = pygame.Color(255,255,0)
		self._backcol = pygame.Color(0, 0, 127)
		
		self._sys_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), 'sysfont.ttf'), 20)
		self._text_cursor = (0, 0)
		self._sys_lh = self._sys_font.get_linesize()
		self._sys_em = self._sys_font.size('m')[0]

		self._cursor_save = pygame.Surface((self._sys_em, self._sys_lh))

		self._event_thread = EventThread()
		self._event_thread.daemon = True
		self._event_thread.start()

		self.options = { }

		self.clear()

	def _flip(self):
		pygame.display.flip()
		if self._event_thread.escape_pressed:
			sys.exit(0)
	
	def _draw_cursor(self):
		tc_rect = (self._text_cursor[0], self._text_cursor[1], self._sys_em, self._sys_lh)
		self._cursor_save.blit(self._screen, (0,0), tc_rect)
		self._screen.fill(self._forecol, tc_rect)
	
	def _undraw_cursor(self):
		self._screen.blit(self._cursor_save, self._text_cursor)

	def _scroll_text_if_necessary(self):
		tc = self._text_cursor
		lh = self._sys_lh

		# Scroll the screen if necessary
		while tc[1] + lh> self._screen.get_height():
			self._screen.scroll(0, -lh)
			self._screen.fill(self._backcol, (0, self._screen.get_height()-lh, self._screen.get_width(), lh))
			self._text_cursor = (tc[0], tc[1] - lh)
			return True

		return False

	def _reverse_one_em(self):
		self._undraw_cursor()
		tc = (self._text_cursor[0] - self._sys_em, self._text_cursor[1])
		if tc[0] < 0:
			remainder = self._screen.get_width() % self._sys_em
			tc = (self._screen.get_width() - remainder - self._sys_em, tc[1] - self._sys_lh)
			if tc[1] < 0:
				tc = (0, 0)
		self._text_cursor = tc
		self._draw_cursor()
	
	def _put_char(self, c):
		self._undraw_cursor()

		# Blit the character
		f = self._sys_font
		ts = f.render(c, False, self._forecol, self._backcol)
		self._screen.blit(ts, self._text_cursor)

		# Advance the text cursor
		lh = self._sys_lh; em = self._sys_em
		tc = (self._text_cursor[0] + self._sys_em, self._text_cursor[1])

		# Will the next char be off to the right?
		if tc[0] + em > self._screen.get_width():
			tc = (0, tc[1] + lh)
		self._text_cursor = tc

		# Scroll the screen if necessary
		self._scroll_text_if_necessary()
		
		self._draw_cursor()
	
	def _new_line(self):
		self._undraw_cursor()
		self._text_cursor = (0, self._text_cursor[1] + self._sys_lh)
		self._scroll_text_if_necessary()
		self._draw_cursor()

	def foreground(self, r, g, b):
		self._undraw_cursor()
		self._forecol = pygame.Color(r, g, b)
		self._draw_cursor()
		self._flip()

	def background(self, r, g, b):
		self._backcol = pygame.Color(r, g, b)
	
	def clear(self):
		self._screen.fill(self._backcol)
		self._flip()

	def rectangle(self, x, y, w, h, width=0):
		pygame.draw.rect(self._screen, self._forecol, pygame.Rect(x, y, w, h), width)
		self._flip()

	def line(self, x1, y1, x2, y2, width=1):
		pygame.draw.line(self._screen, self._forecol, (x1, y1), (x2, y2), width)
		self._flip()

	def write(self, s, no_line_break = False):
		for l in s.split('\n'):
			for c in l:
				self._put_char(c)
			if not no_line_break:
				self._new_line()
		self._flip()
	
	def _getkey(self):
		cv = threading.Condition()
		s = { "event": None, "have_event": False }

		def kh(e):
			cv.acquire()
			s["event"] = e
			s["have_event"] = True
			cv.notify()
			cv.release()

		self._event_thread.key_handler = kh

		# Wait for input
		cv.acquire()
		while not s["have_event"]:
			cv.wait()
		cv.release()

		self._event_thread.key_handler = None

		return s["event"].dict
	
	def gettext(self, prompt = None):
		if prompt is not None:
			self.write(prompt, True)

		done = False
		line = ""
		while not done:
			e = self._getkey()

			if e["unicode"] == u'\x08':
				if len(line) > 0:
					self._reverse_one_em()
					self._put_char(" ")
					self._reverse_one_em()
					line = line[:-1]
					self._flip()
			elif e["unicode"] == u'\r':
				done = True
				self._new_line()
				self._flip()
			elif len(e["unicode"]) > 0:
				line += e["unicode"]
				self._put_char(e["unicode"])
				self._flip()

		return line

__g = Graphics()

def __atexit():
	write("Press any key to exit.")
	__g._getkey()
atexit.register(__atexit)

def foreground(r, g, b):
	global __g
	__g.foreground(r, g, b)

def background(r, g, b):
	global __g
	__g.background(r, g, b)

def rectangle(x, y, w, h, width=0):
	global __g
	__g.rectangle(x, y, w, h, width)

def line(x1, y1, x2, y2, width=1):
	global __g
	__g.line(x1, y1, x2, y2, width)

def clear():
	global __g
	__g.clear()
	
def write(s, no_line_break = False):
	global __g
	__g.write(s, no_line_break)

def gettext(prompt = None):
	global __g
	return __g.gettext(prompt)

def setoption(opt, val):
	global __g
	__g.options[opt] = val

def getoption(opt, val):
	global __g
	return __g.options[opt]
