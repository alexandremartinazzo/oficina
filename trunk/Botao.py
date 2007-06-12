import pygtk
pygtk.require('2.0')
import gtk
from gtk import gdk


class Botao:
	def __init__(self, area):
		self.area = area
		self.botoes = []
		self.id = 0
		self.desenha = False
		self.local = 0,0
		self.tooltip = gtk.Tooltips()
		
	def adicionaBotao(self, archive, tipo, x, y, mousedown, tooltip_):
		img = gtk.Image()
		img.set_from_file("./images/" + archive)
		
		eventbox = gtk.EventBox()
		eventbox.add(img)	
		#eventbox.set_visible_window(False)
		#eventbox.set
		eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))

		eventbox.set_events(gtk.gdk.POINTER_MOTION_MASK |
				gtk.gdk.POINTER_MOTION_HINT_MASK |
				gtk.gdk.BUTTON_PRESS_MASK |
				gtk.gdk.BUTTON_RELEASE_MASK)	
			    
		eventbox.connect("motion_notify_event", self.mousemove,self.id)
		eventbox.connect("button_release_event", self.mouseup)
		eventbox.connect("button_press_event", self.mousedown, self.id)
		eventbox.connect("button_press_event", mousedown, tipo)
		# Drag'n'drop
		self.area.put(eventbox, x, y)
		self.botoes.append(eventbox)
		self.id += 1	
		
		self.tooltip.set_tip(eventbox, tooltip_, None)
		#self.tooltip.enable()
		
	def mousedown(self,widget,event, id): 		
		self.desenha = True
		ex = event.x
		ey = event.y 
		self.local = ex, ey	
	
	def mouseup(self,widget,event): 		
		self.desenha = False

	def mousemove(self,widget,event, id): 		
		x , y, state = self.area.window.get_pointer()	
		ex, ey = self.local
		x_ = int(x - ex) 
		y_ = int(y - ey) 		
		if state & gtk.gdk.BUTTON1_MASK and self.desenha:
			self.area.move(self.botoes[id], x_, y_)

			

