# -*- coding: utf-8 -*-
#!/usr/bin/python
import  pygtk
pygtk.require('2.0')
import sys,gtk,gobject,random,socket,select
import threading
import math
import pango
from gtk import gdk

from Oficina import Oficina

def main():
	oficina = Oficina()
	gtk.main()	

if __name__ == "__main__":
	main()

