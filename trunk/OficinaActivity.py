import os
from gettext import gettext as _

import gtk

from sugar.activity import activity

#from Oficina import Oficina
from toolbox import Toolbox
from Area import Area
from Cursors import Cursors

DRAW_WIDTH  = 1195
DRAW_HEIGHT = 780

class OficinaActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        os.chdir(activity.get_bundle_path())
        #print activity.get_bundle_path()

        toolbox = Toolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()
        
        ## Commented for testing
        ## I will use a gtk.TextView to display results for events
##        oficina = Oficina(self)
##        self._area = oficina.area
##        self._area = oficina.areaFixa()
##        self.set_canvas(self._area)
##        self._area.show()
        
        #FIXME : achar local melhor pra colocar isso
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

        self._area = self.area = Area(self)
        self._area.tool = 2
        sw.add_with_viewport(self._area)
        self._area.show()

        #self.textview = gtk.TextView()
        #sw.add(self.textview)
        #self.textview.show()
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
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, DRAW_WIDTH, DRAW_HEIGHT)
        pixbuf.get_from_drawable(self._area.pixmap, gtk.gdk.colormap_get_system(), 0, 0, 0, 0, -1, -1)
        pixbuf.save(file_path, 'png', {})	

