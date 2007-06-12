import  pygtk
pygtk.require('2.0')
import gtk
import sys, gobject, socket
from gtk import gdk
import math
import pango


WIDTH = 1200
HEIGHT = 900

class Desenho:
	def __init__(self, d_):		
		self.d = d_
	def desenhaLinha(self, widget, coords):
		widget.queue_draw()
		self.d.pixmap_temp.draw_drawable(self.d.gc,self.d.pixmap,  0 , 0 ,0,0, WIDTH, HEIGHT)
		self.d.pixmap_temp.draw_line(self.d.gc_linha,self.d.oldx,self.d.oldy,coords[0],coords[1])
		self.d.newx = coords[0]	
		self.d.newy = coords[1]
	
	def desenhaBorracha(self, widget, coords):
		self.d.desenha = False
		self.d.pixmap.draw_arc(self.d.gc_borracha, True, coords[0], coords[1], 12, 12, 0, 360*64)
		self.d.pixmap_temp.draw_arc(self.d.gc_borracha, True, coords[0], coords[1], 12, 12, 0, 360*64)
		self.d.oldx = coords[0]
		self.d.oldy = coords[1]
		widget.queue_draw()
		
	def desenhaQuadrado(self, widget, coords):
		widget.queue_draw()		

		if coords[0] > WIDTH:
			coords0 = WIDTH
		else:
			coords0 = coords[0]
			
		if coords [1] > HEIGHT:
			coords1 = HEIGHT
		else:
			coords1 = coords[1]
			
		self.d.newx_ = coords0 - self.d.oldx
		self.d.newy_ = coords1 - self.d.oldy

		if self.d.newx_ >= 0:
			self.d.newx = self.d.oldx	
		else:	
			if coords0 > 0:
				self.d.newx = coords0
				self.d.newx_ = - self.d.newx_
			else:
				self.d.newx = 0
				self.d.newx_ = self.d.oldx
					
		if self.d.newy_ >= 0:
			self.d.newy = self.d.oldy	
		else:				
			if coords1 > 0:
				self.d.newy_ = - self.d.newy_
				self.d.newy = coords1
			else:
				self.d.newy = 0
				self.d.newy_ = self.d.oldy
				
		self.d.pixmap_temp.draw_drawable(self.d.gc,self.d.pixmap,  0 , 0 ,0,0, WIDTH, HEIGHT)
		self.d.pixmap_temp.draw_rectangle(self.d.gc, True ,self.d.newx,self.d.newy,self.d.newx_,self.d.newy_)
		self.d.pixmap_temp.draw_rectangle(self.d.gc_linha, False ,self.d.newx,self.d.newy,self.d.newx_,self.d.newy_)

	def desenhaCirculo(self, widget, coords):
		widget.queue_draw()	
		
		if coords[0] > WIDTH:
			coords0 = WIDTH
		else:
			coords0 = coords[0]
			
		if coords [1] > HEIGHT:
			coords1 = HEIGHT
		else:
			coords1 = coords[1]
			
		self.d.newx_ = coords0 - self.d.oldx
		self.d.newy_ = coords1 - self.d.oldy
		print "coords0", coords0

		if self.d.newx_ >= 0:
			self.d.newx = self.d.oldx	
		else:	
			if coords0 > 0:
				self.d.newx = coords0
				self.d.newx_ = - self.d.newx_
			else:
				self.d.newx = 0
				self.d.newx_ = self.d.oldx

		if self.d.newy_ >= 0:
			self.d.newy = self.d.oldy	
		else:	
			if coords1 > 0:				
				self.d.newy = coords1
				self.d.newy_ = - self.d.newy_
			else:
				self.d.newy = 0
				self.d.newy_ = self.d.oldy

		self.d.pixmap_temp.draw_drawable(self.d.gc,self.d.pixmap,  0 , 0 ,0,0, WIDTH, HEIGHT)		
		self.d.pixmap_temp.draw_arc(self.d.gc, True, self.d.newx, self.d.newy, self.d.newx_,self.d.newy_, 0, 360*64)
		self.d.pixmap_temp.draw_arc(self.d.gc_linha, False, self.d.newx, self.d.newy, self.d.newx_, self.d.newy_, 0, 360*64)
	
	def desenhaLapis(self, widget, coords):
		self.d.pixmap_temp.draw_drawable(self.d.gc,self.d.pixmap,  0 , 0 ,0,0, WIDTH, HEIGHT)
		self.d.pixmap.draw_line(self.d.gc_linha,self.d.oldx,self.d.oldy,coords[0],coords[1])	
		self.d.oldx = coords[0]
		self.d.oldy = coords[1]
		widget.queue_draw()

	def limpatudo(self):
		self.d.desenho = []
		self.d.textos = []		
		self.d.pixmap.draw_rectangle(self.d.get_style().white_gc, True,0, 0, WIDTH, HEIGHT)
		self.d.pixmap_temp.draw_rectangle(self.d.get_style().white_gc, True,0, 0, WIDTH, HEIGHT)
		self.d.queue_draw()	

	def Texto(self,widget,event):
			if self.d.estadoTexto == 0:
				self.d.estadoTexto = 1
				print event.x
				self.d.janela.areaFixa.move(self.d.janela.entrada, int(event.x), int(event.y))
				self.d.janela.entrada.show()
			else:	
				self.d.estadoTexto = 0
				texto = self.d.janela.entrada.get_text()
				layout = self.d.create_pango_layout(texto)
				layout.set_font_description(self.d.font)
				self.d.pixmap.draw_layout(self.d.gc, self.d.oldx, self.d.oldy, layout)
				self.d.pixmap_temp.draw_layout(self.d.gc, self.d.oldx, self.d.oldy, layout)
				self.d.janela.entrada.hide()


				widget.queue_draw()