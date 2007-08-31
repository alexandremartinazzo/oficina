# -*- coding: utf-8 -*-
"""
OficinaActivity.py

Create Oficina Activity


Copyright 2007, NATE-LSI-EPUSP

Oficina is developed in Brazil at Escola Politécnica of 
Universidade de São Paulo. NATE is part of LSI (Integrable
Systems Laboratory) and stands for Learning, Work and Entertainment
Research Group. Visit our web page: 
www.lsi.usp.br/nate
Suggestions, bugs and doubts, please email oficina@lsi.usp.br

Oficina is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation version 2 of 
the License.

Oficina is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with Oficina; if not, write to the
Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, 
Boston, MA  02110-1301  USA.
The copy of the GNU General Public License is found in the 
COPYING file included in the source distribution.


Authors:

Joyce Alessandra Saul               (joycealess@gmail.com)
Andre Mossinato                     (andremossinato@gmail.com)
Nathalia Sautchuk Patrício          (nathalia.sautchuk@gmail.com)
Pedro Kayatt                        (pekayatt@gmail.com)
Rafael Barbolo Lopes                (barbolo@gmail.com)
Alexandre A. Gonçalves Martinazzo   (alexandremartinazzo@gmail.com)

Colaborators:
Bruno Gola                          (brunogola@gmail.com)

Group Manager:
Irene Karaguilla Ficheman           (irene@lsi.usp.br)

Cientific Coordinator:
Roseli de Deus Lopes                (roseli@lsi.usp.br)

"""


import os
from gettext import gettext as _

import gtk

from sugar.activity import activity

from toolbox import Toolbox
from Area import Area
import logging

class OficinaActivity(activity.Activity):
    def oficina(self, widget, data=None):
        logging.info('Oficina')
         
    def __init__(self, handle):
        """Initialize the OficinaActivity object.

            @param  self
            @param  handle

        """
        activity.Activity.__init__(self, handle)
        
        logging.debug('Starting Paint activity (Oficina)')

        os.chdir(activity.get_bundle_path())
        #print activity.get_bundle_path()
        
        self._fixed = gtk.Fixed()   
        self._area = Area(self) 
        
        toolbox = Toolbox(self)
        self.set_toolbox(toolbox)
        toolbox.show()       
  

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        
        color = gtk.gdk.color_parse("white")
        self._fixed.modify_bg(gtk.STATE_NORMAL, color)

        self.bg = gtk.Image()
        self.bg.set_from_file('./icons/bg.svg')
        self._fixed.put(self.bg, 200, 100)
        self.bg.show()

        #FIXME: use a textview instead of an Entry
        self._textview = gtk.TextView()
        # If we use this, text viewer will have constant size, we don't want that
        #self._textview.set_size_request(100,100)
        #self._textview = gtk.Entry()
        
        self._fixed.put(self._area, 200 , 100)
        # Area size increased
        #self._fixed.put(self._area, 0 , 0)
        
        sw.add_with_viewport(self._fixed)
        self._area.show()
        self._fixed.show()


        self._fixed.put(self._textview, 0, 0)
        self._textview.hide()
        sw.show()

        # setting scrolledwindow as activity canvas...
        self.set_canvas(sw)


    def read_file(self, file_path):
        '''Read file from Sugar Journal.

            @param  self
            @param  file_path 

        '''
        logging.debug('reading file %s', file_path)
#         logging.debug(file_path)
        
        self._area.loadImage(file_path, self._area, False)
        
        # Does this work?
#         self._area.undo_times = 1
#         self._area.redo_times = 0


    def write_file(self, file_path):
        '''Save file on Sugar Journal.

            @param  self 
            @param  file_path 

        '''
        logging.debug('saving as PNG')
        logging.debug('writting file %s', file_path)
        
        width, height = self._area.window.get_size()
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
        pixbuf.get_from_drawable(self._area.pixmap, gtk.gdk.colormap_get_system(), 0, 0, 0, 0, -1, -1)
        self.metadata['mime_type'] = 'image/png'
        pixbuf.save(file_path, 'png', {})   

