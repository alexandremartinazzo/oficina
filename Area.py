# -*- coding: utf-8 -*-
import  pygtk
pygtk.require('2.0')
import gtk
import sys, gobject, socket
from gtk import gdk
import math
import pango

from Desenho import Desenho

WIDTH = 1195
HEIGHT = 895

class Area(gtk.DrawingArea):
	def __init__(self, janela):		
		gtk.DrawingArea.__init__(self)
		self.set_size_request(WIDTH, HEIGHT)
		self.set_events(gtk.gdk.POINTER_MOTION_MASK |
				gtk.gdk.POINTER_MOTION_HINT_MASK |
				gtk.gdk.BUTTON_PRESS_MASK |
				gtk.gdk.BUTTON_RELEASE_MASK|
				gtk.gdk.EXPOSURE_MASK)	
			    
		self.connect("expose_event",self.expose)
		self.connect("motion_notify_event", self.mousemove)
		self.connect("button_press_event", self.mousedown)
		self.connect("button_release_event", self.mouseup)		

		self.set_extension_events(gtk.gdk.EXTENSION_EVENTS_CURSOR)
		
		self.ferramenta = None
		self.desenha = False
		self.move = False
		self.connect("configure_event", self.configure_event)
		self.oldx = 0
		self.oldy = 0
		self.newx = 0
		self.newy = 0
		self.newx_ = 0
		self.newy_ = 0
		""""
		self.px = 0
		self.py = 0		
		self.antx = 0
		self.anty = 0
		"""
		self.primeira = 1
		self.gc = None
		self.gc_linha = None
		self.gc_borracha= None
		self.gc_selecao= None
		self.pixmap = None	
		self.pixmap_temp = None
		self.desenho = []	
		self.textos = []	
		self.cor_ = 2
		self.cor_linha = 2
		self.estadoTexto = 0
		self.janela = janela	
		self.d = Desenho(self)

		colormap = self.get_colormap()
		
		self.cores = [		
		colormap.alloc_color('#ffaaff', True, True), # purple
		colormap.alloc_color('#f4ee56', True, True), # yellow
		colormap.alloc_color('#000000', True, True), # black
		colormap.alloc_color('#45a5dc', True, True), # blue
		colormap.alloc_color('#44aa44', True, True), # green
		colormap.alloc_color('#dd5555', True, True), # red
		colormap.alloc_color('#ffaa11', True, True), # orange		
		colormap.alloc_color('#ffffff', True, True), # white	
		colormap.alloc_color('#00aa00', True, True)  # green - selection
		]
		self.font = pango.FontDescription('Sans 8')
		#self.mensagem = Mensagens(self)
		#self.mensagem.criaConexao()

	# Create a new backing pixmap of the appropriate size
	def configure_event(self, widget, event):		
		win = widget.window
		width = win.get_geometry()[2]
		height = win.get_geometry()[3]	
		
		self.pixmap = gtk.gdk.Pixmap(win, width, height, -1)
		self.pixmap.draw_rectangle(widget.get_style().white_gc, True, 0, 0, width, height)
		self.pixmap_temp = gtk.gdk.Pixmap(win, width, height, -1)
		self.pixmap_temp.draw_rectangle(widget.get_style().white_gc, True, 0, 0, width, height)
		
		self.gc = widget.window.new_gc()	
		self.gc_borracha = widget.window.new_gc()		
		self.gc_borracha.set_foreground(self.cores[7])
		
		self.gc_linha = widget.window.new_gc()	
		self.gc_linha.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_ROUND)
		
		self.gc_selecao = widget.window.new_gc()	
		self.gc_selecao.set_line_attributes(1, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_ROUND)
		self.gc_selecao.set_foreground(self.cores[8])
		
		return True

	def expose(self, widget, event):		
		area = event.area		
		if self.desenha:
			widget.window.draw_drawable(self.gc, self.pixmap_temp, area[0], area[1], area[0], area[1], area[2], area[3])	
		else:
			widget.window.draw_drawable(self.gc, self.pixmap, area[0], area[1], area[0], area[1], area[2], area[3])		
		return False

	def mousedown(self,widget,event): 		
		# text
		if self.ferramenta == 4:
			self.d.Texto(widget,event)
		if not self.move or self.ferramenta != 26:
			self.oldx = int(event.x)
			self.oldy = int(event.y)	
			
		self.desenha = True		
		
	def mousemove(self,widget,event): 		
		x , y, state = event.window.get_pointer()	
		coords = int(x), int(y)
						
		if state & gtk.gdk.BUTTON1_MASK and self.pixmap != None:
			if self.ferramenta == 3:
				self.d.desenhaBorracha(widget, coords, 30)
			if self.desenha:
				# line
				if self.ferramenta == 1:
					print self.oldx
					self.d.desenhaLinha(widget, coords)	
				# pencil
				elif self.ferramenta == 2:
					self.d.desenhaLapis(widget, coords)		
				# circle
				elif self.ferramenta == 5:
					self.d.desenhaCirculo(widget,coords)	
				# square
				elif self.ferramenta == 6:
					self.d.desenhaQuadrado(widget,coords)	
				# selection
				elif self.ferramenta == 26 and not self.move:
					self.d.desenhaSelecao(widget,coords)						
				# selection
				elif self.ferramenta == 26 and self.move:
					self.d.moveSelection(widget, coords)
				#poligon	
				elif self.ferramenta == 27:
					self.d.desenhaPoligono(widget, coords)	
		
	def mouseup(self,widget,event):	
		
		if self.desenha:
			# line
			if self.ferramenta == 1:
				self.pixmap.draw_line(self.gc_linha,self.oldx,self.oldy, int (event.x), int(event.y))				
				widget.queue_draw()
			# circle
			elif self.ferramenta == 5:
				self.pixmap.draw_arc(self.gc, True, self.newx, self.newy, self.newx_, self.newy_, 0, 360*64)
				self.pixmap.draw_arc(self.gc_linha, False, self.newx, self.newy, self.newx_, self.newy_, 0, 360*64)
				widget.queue_draw()
			# square
			elif self.ferramenta == 6:
				self.pixmap.draw_rectangle(self.gc, True, self.newx,self.newy, self.newx_,self.newy_)
				self.pixmap.draw_rectangle(self.gc_linha, False, self.newx,self.newy, self.newx_,self.newy_)
				widget.queue_draw()
			# selection
			elif self.ferramenta == 26:
				if self.move == False:
					self.pixmap_temp.draw_drawable(self.gc,self.pixmap,  0 , 0 ,0,0, WIDTH, HEIGHT)
					self.move = True
					self.sx = int (event.x)
					self.sy = int(event.y)
					self.window.set_cursor(self.janela.cursorMove.cursor())
				elif self.move == True:		
					self.pixmap.draw_drawable(self.gc, self.pixmap_temp, 0,0,0,0, WIDTH, HEIGHT)	
					self.window.set_cursor(self.janela.cursorSelecao.cursor())	
					self.move = False				
			# poligono
			elif self.ferramenta == 27:
				if self.primeira == 1:
					self.pixmap.draw_line(self.gc_linha,self.oldx,self.oldy, int (event.x), int( event.y ))
					self.antx = event.x
					self.anty = event.y
					self.px = self.oldx
					self.py = self.oldy
					self.primeira = 0
				else:
					self.dx = math.fabs(event.x - self.px)
					self.dy = math.fabs(event.y - self.py)
					if (self.dx < 20) & (self.dy < 20):
						self.pixmap.draw_line(self.gc_linha,int (self.px), int (self.py), int (self.antx), int (self.anty))
						self.primeira = 1
					else:	
						self.pixmap.draw_line(self.gc_linha,int (self.antx),int (self.anty), int (event.x), int( event.y ))
					self.antx = event.x
					self.anty = event.y
				widget.queue_draw() 
		self.desenha = False
		
	def mudacor(self, cor):
		self.cor_ = cor		
		self.gc.set_foreground(self.cores[cor])
 
 	def mudacorlinha(self, cor):
		self.cor_linha = cor	
		self.gc_linha.set_foreground(self.cores[cor])
