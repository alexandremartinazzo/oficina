import os
from gettext import gettext as _

import gtk

from sugar.activity import activity

#from Oficina import Oficina
from toolbox import Toolbox
from Area import Area
from Cursors import Cursors

# DRAW_WIDTH  = 1195
# DRAW_HEIGHT = 800

class OficinaActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        os.chdir(activity.get_bundle_path())
        #print activity.get_bundle_path()
        
        toolbox = Toolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()       
  

        # cursors
        #self._pencil_cursor = Cursors('lapis_cursor.png')
        #self._circle_cursor = Cursors('circulo_cursor.png')
        #self._rubber_cursor = Cursors('borracha_cursor.png')
        #self._square_cursor = Cursors('quadrado_cursor.png')
        #self._line_cursor = Cursors('linha_cursor.png')
        #self._letter_cursor = Cursors('letra_cursor.png')		
        #self._selection_cursor = Cursors('selecao_cursor.png')	
        #self._polygon_cursor = Cursors('poligono_cursor.png')	
        #self._move_cursor = Cursors('move_cursor.png')

        # addind a textview widget
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self._fixed = gtk.Fixed()	
        self._area = Area(self)	
        color = gtk.gdk.color_parse("white")
        self._fixed.modify_bg(gtk.STATE_NORMAL, color)
        #FIXME: use a textview instead of a Entry
        #self._textview = gtk.TextView()
        self._textview = gtk.Entry()
        self._area.tool = 2
        self._fixed.put(self._area, 0 , 0)

        sw.add_with_viewport(self._fixed)
        self._area.show()
        self._fixed.show()


        self._fixed.put(self._textview, 0, 0)
        self._textview.hide()
        sw.show()

        # setting scrolledwindow as activity canvas...
        self.set_canvas(sw)


    def read_file(self, file_path):
        '''
        Method to read file from Sugar Journal
        '''
        print file_path
        #self._area.d.limpatudo()
        self._area.d.clear()
        self._area.d.loadImage(file_path)


    def write_file(self, file_path):
        '''
        Method to save file on Sugar Journal
        '''
        print file_path
        width, height = self._area.window.get_size()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
        pixbuf.get_from_drawable(self._area.pixmap, gtk.gdk.colormap_get_system(), 0, 0, 0, 0, -1, -1)
        pixbuf.save(file_path, 'png', {})	

