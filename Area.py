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
HEIGHT = 800

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
		
		self.tool = None
		self.desenha = False
		self.move = False
		self.connect("configure_event", self.configure_event)
		self.oldx = 0
		self.oldy = 0
		self.newx = 0
		self.newy = 0
		self.newx_ = 0
		self.newy_ = 0
		self.primeira = 1
		self.gc = None
		self.gc_line = None
		self.gc_eraser = None
		self.gc_brush = None
		self.gc_selection = None
		self.pixmap = None	
		self.pixmap_temp = None
		self.desenho = []	
		self.textos = []	
		self.color_ = 2
		self.color_line = 2
		self.estadoTexto = 0
		self.janela = janela	
		self.d = Desenho(self)
		self.line_size = 2

		colormap = self.get_colormap()
		
		self.cores = [		
		colormap.alloc_color('#000000', True, True), # black
		colormap.alloc_color('#ee33ee', True, True), # purple
		colormap.alloc_color('#f4ee56', True, True), # yellow		
		colormap.alloc_color('#45a5dc', True, True), # blue
		colormap.alloc_color('#44aa44', True, True), # green
		colormap.alloc_color('#dd5555', True, True), # red
		colormap.alloc_color('#ffaa11', True, True), # orange		
		colormap.alloc_color('#ffffff', True, True), # white	
		colormap.alloc_color('#00aa00', True, True)  # green - selection
		]
		self.font = pango.FontDescription('Sans 9')
		#self.mensagem = Mensagens(self)
		#self.mensagem.criaConexao()
		
		#start of UNDO and REDO
		self.first_undo = True
		self.undo_times = 0
		self.redo_times = 0
		self.undo_list=[]#pixmaps list to Undo func

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
		self.gc_eraser = widget.window.new_gc()		
		self.gc_eraser.set_foreground(self.cores[7])
		
		self.gc_brush = widget.window.new_gc()		
		self.gc_brush.set_foreground(self.cores[0])
				
		self.gc_line = widget.window.new_gc()	

		self.gc_selection = widget.window.new_gc()	
		self.gc_selection.set_line_attributes(1, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_ROUND)
		self.gc_selection.set_foreground(self.cores[8])
		
		return True
		
    # set the new line size
	def configure_line(self, size):
	    self.line_size = size
	    self.gc_line.set_line_attributes(size, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_ROUND)

	def expose(self, widget, event):		
		area = event.area		
		if self.desenha:
			widget.window.draw_drawable(self.gc, self.pixmap_temp, area[0], area[1], area[0], area[1], area[2], area[3])	
		else:
			widget.window.draw_drawable(self.gc, self.pixmap, area[0], area[1], area[0], area[1], area[2], area[3])		
		return False

	def mousedown(self,widget,event): 		
		# text
		if self.tool == 4:
			self.d.text(widget,event)
		if not self.move or self.tool != 26:
			self.oldx = int(event.x)
			self.oldy = int(event.y)	
			
		self.desenha = True		
		
	def mousemove(self,widget,event): 		
		x , y, state = event.window.get_pointer()	
		coords = int(x), int(y)
						
		if state & gtk.gdk.BUTTON1_MASK and self.pixmap != None:
			if self.tool == 3:
				self.d.eraser(widget, coords)
			#brush
			elif self.tool == 29:
				    self.d.brush(widget, coords, self.line_size)
			if self.desenha:
				# line
				if self.tool == 1:
					print self.oldx
					self.configure_line(self.line_size)
					self.d.line(widget, coords)	
				# pencil
				elif self.tool == 2:
				    self.configure_line(self.line_size)
				    self.d.pencil(widget, coords)		
				# circle
				elif self.tool == 5:
				    self.configure_line(self.line_size)
				    self.d.circle(widget,coords)	
				# square
				elif self.tool == 6:
				    self.configure_line(self.line_size)
				    self.d.square(widget,coords)	
				# selection
				elif self.tool == 26 and not self.move:
					self.d.selection(widget,coords)						
				# selection
				elif self.tool == 26 and self.move:
					self.d.moveSelection(widget, coords)
				#poligon	
				elif self.tool == 27:
				    self.configure_line(self.line_size)
				    self.d.polygon(widget, coords)	
		
	def mouseup(self,widget,event):	
		
		if self.desenha:
			# line
			if self.tool == 1:
				self.pixmap.draw_line(self.gc_line,self.oldx,self.oldy, int (event.x), int(event.y))				
				widget.queue_draw()
				self.enableUndo(widget)
			# circle
			elif self.tool == 5:
				self.pixmap.draw_arc(self.gc, True, self.newx, self.newy, self.newx_, self.newy_, 0, 360*64)
				self.pixmap.draw_arc(self.gc_line, False, self.newx, self.newy, self.newx_, self.newy_, 0, 360*64)

				widget.queue_draw()
				self.enableUndo(widget)
			# square
			elif self.tool == 6:	
				self.pixmap.draw_rectangle(self.gc, True, self.newx,self.newy, self.newx_,self.newy_)
				self.pixmap.draw_rectangle(self.gc_line, False, self.newx,self.newy, self.newx_,self.newy_)

				widget.queue_draw()
				self.enableUndo(widget)
			# selection
			elif self.tool == 26:
				if self.move == False:
					self.pixmap_temp.draw_drawable(self.gc,self.pixmap,  0 , 0 ,0,0, WIDTH, HEIGHT)
					self.move = True
					self.sx = int (event.x)
					self.sy = int(event.y)
					self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
				elif self.move == True:		
					self.pixmap.draw_drawable(self.gc, self.pixmap_temp, 0,0,0,0, WIDTH, HEIGHT)	
					# FIXME: Adicionar cursor formato selecao
					self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))	
					self.move = False
					self.enableUndo(widget)				
			# polygon
			elif self.tool == 27:
				if self.primeira == 1:
					self.pixmap.draw_line(self.gc_line,self.oldx,self.oldy, int (event.x), int( event.y ))
					self.antx = event.x
					self.anty = event.y
					self.px = self.oldx
					self.py = self.oldy
					self.primeira = 0
				else:
					self.dx = math.fabs(event.x - self.px)
					self.dy = math.fabs(event.y - self.py)
					if (self.dx < 20) & (self.dy < 20):
						self.pixmap.draw_line(self.gc_line,int (self.px), int (self.py), int (self.antx), int (self.anty))
						self.primeira = 1
						self.enableUndo(widget)
					else:	
						self.pixmap.draw_line(self.gc_line,int (self.antx),int (self.anty), int (event.x), int( event.y ))
					self.antx = event.x
					self.anty = event.y
				widget.queue_draw() 
			elif self.tool == 2:# or 3 or 4 check this before
				self.enableUndo(widget)
		self.desenha = False
		
		
    #this func make a basic Undo
	def undo(self):
		if self.first_undo:#if is the first time you click on UNDO
			self.undo_times -= 1
			self.redo_times = 1
		
		elif (self.first_redo) and (self.undo_times!=0):
			self.undo_times += 1
		
		print "Undo no.%d" %(self.undo_times)
		if self.undo_times >0 :	
			self.undo_times -= 1
			self.redo_times += 1
			try: #to not try paint someting wrong
				#print "Drawing undo[%d]" %(self.undo_times)
				self.pixmap.draw_drawable(self.gc, self.undo_list[self.undo_times], 0,0,0,0, WIDTH, HEIGHT)
			except:
				print "Can't draw"
				pass
			self.queue_draw()
			self.first_redo=False
		else:	
			self.undo_times = 0
			#self.redo_times = 1
			self.first_redo = True
			self.d.clear()#Undo the last action, so clear-all
		self.first_undo=False
		
		 
	def redo(self):
		#print "REDO no.%d" %(self.redo_times)
		
		if  (self.redo_times>0):
			self.redo_times -= 1
			self.undo_times += 1

			
			if self.first_redo:
				self.undo_times -=1
				self.redo_times +=1
			self.first_redo=False
			try: #to not try paint someting wrong 
				#print "Drawing undo[%d]" %(self.undo_times)
				self.pixmap.draw_drawable(self.gc, self.undo_list[self.undo_times], 0,0,0,0, WIDTH, HEIGHT)
			except:
				print "Can't draw"
				self.undo_times-=1
		self.queue_draw()
			
		   	
	def enableUndo(self,widget):
		if not self.first_undo and not self.first_redo:
			self.undo_times += 1
		
		self.undo_list.append(None)#alloc memory
		self.undo_list[self.undo_times] = gtk.gdk.Pixmap(widget.window, WIDTH, HEIGHT, -1) #define type
		self.undo_list[self.undo_times].draw_drawable(self.gc,self.pixmap,0,0,0,0, WIDTH, HEIGHT) #copy workarea
		self.undo_times += 1
		self.redo_times = 0	
		self.first_undo = True
		
		#this is the part where we can limit the steps of undo/redo		
		#if self.undo_times>=5:
		#	self.undo_list.pop(0)
		#	self.undo_times-=1
		#	print "estourou"
		
	def _set_fill_color(self, color):
		self.color_ = color		
		self.gc.set_foreground(self.cores[color])
 
 	def _set_stroke_color(self, color):
		self.color_line = color	
		self.gc_line.set_foreground(self.cores[color])
		self.gc_line.set_line_attributes(1, gtk.gdk.LINE_ON_OFF_DASH, gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_ROUND)  
		self.gc_brush.set_foreground(self.cores[color])

	def _set_grayscale(self):
		pix = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, WIDTH, HEIGHT)
		pix_ = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, WIDTH, HEIGHT)
		pix.get_from_drawable(self.pixmap, gtk.gdk.colormap_get_system(), 0, 0, 0, 0, WIDTH, HEIGHT)
		pix.saturate_and_pixelate(pix_, 0 ,0)

		self.pixmap.draw_pixbuf(self.gc, pix_, 0, 0, 0, 0, WIDTH, HEIGHT, dither=gtk.gdk.RGB_DITHER_NORMAL, x_dither=0, y_dither=0)

		self.pixmap_temp.draw_pixbuf(self.gc, pix_, 0, 0, 0, 0, WIDTH, HEIGHT, dither=gtk.gdk.RGB_DITHER_NORMAL, x_dither=0, y_dither=0)
		self.queue_draw()

	def _rotate_left(self):
		pix = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, WIDTH, HEIGHT)
		pix_ = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, WIDTH, HEIGHT)
		pix.get_from_drawable(self.pixmap, gtk.gdk.colormap_get_system(), 0, 0, 0, 0, -1, -1)
		pix_ = pix.rotate_simple(gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE)
		self.pixmap.draw_pixbuf(self.gc, pix_, 0, 0, 0, 0, width=-1, height=-1, dither=gtk.gdk.RGB_DITHER_NORMAL, x_dither=0, y_dither=0)
		self.queue_draw()
