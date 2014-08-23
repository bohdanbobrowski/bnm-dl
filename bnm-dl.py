#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bnm-dl - Proste pobieranie pobieranie filmów z cyklu "Było... nie minęło. Kronika zwiadowców historii"
# wersja 0.1
# Autor: Bohdan Bobrowski bohdan@bobrowski.com.pl

import os
import json
import re
import sys
import pycurl
import urllib2
import pygtk
pygtk.require('2.0')
import gtk


class PobierzStrone:
    def __init__(self):
        self.contents = ''
    def body_callback(self, buf):
        self.contents = self.contents + buf
# sys.stderr.write("Testing %s\n" % pycurl.version)

def get_resource_path(rel_path):
    dir_of_py_file = os.path.dirname(__file__)
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource

"""
www = PobierzStrone()
c = pycurl.Curl()
c.setopt(c.URL, 'http://regionalna.tvp.pl/14261059/bylo-nie-minelo-kronika-zwiadowcow-historii')
c.setopt(c.WRITEFUNCTION, www.body_callback)
c.perform()
c.close()
"""

www = PobierzStrone()
c = pycurl.Curl()
c.setopt(c.URL, 'http://www.tvp.pl/historia/magazyny-historyczne/bylo-nie-minelo')
c.setopt(c.WRITEFUNCTION, www.body_callback)
c.perform()
c.close()

class WczytajFilmy:

    def pobierzWybrany(self, widget, data=None):
        if self.combobox_quality.get_active() >= 0:
            self.quality = str(self.combobox_quality.get_active() + 1)
            print "Wybrana jakość: "+self.quality
        if self.combobox.get_active() >= 0:
            BNMfilelist = 'http://regionalna.tvp.pl/sess/html5player_iframe.php?object_id=' + self.BNMlinks[self.combobox.get_active()] + "&width=100%&height=100%&autoplay=true&mobile=true/html5player_iframe.html"
            tytul_odcinka = self.BNMtitles[self.combobox.get_active()]
            print "Pobieramy listę plików: "+BNMfilelist
            BNMjson = PobierzStrone()
            BNMcurl = pycurl.Curl()
            BNMcurl.setopt(c.URL, BNMfilelist)
            BNMcurl.setopt(c.WRITEFUNCTION, BNMjson.body_callback)
            BNMcurl.perform()
            BNMcurl.close()
            BNMjsonOBJ = json.loads(BNMjson.contents)
            url = ''
            for format in BNMjsonOBJ[u'token'][u'formats']:
                if format[u'url'].find('video-'+self.quality+'.mp4')>=0:
                    url = format[u'url']
            # bylo-nie-minelo-YYYYMMDD.mp4 
            fn = re.findall('([0-9]{2})\.([0-9]{2})\.([0-9]{4})', tytul_odcinka)
            file_name = 'bylo-nie-minelo-'+fn[0][2]+fn[0][1]+fn[0][0]+'.mp4'
            u = urllib2.urlopen(url)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Tytuł odcinka: "+tytul_odcinka
            print("Pobieranie: {0} Rozmiar: {1}".format(url, file_size))            
            self.pbar.set_text('Pobieranie: "'+tytul_odcinka+'"')
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
                p = float(file_size_dl) / file_size
                status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
                status = status + chr(8)*(len(status)+1)                
                sys.stdout.write(status)
                self.pbar.set_fraction(p)
                while gtk.events_pending():
                    gtk.main_iteration()
            f.close()
            print "\nKoniec!"
            self.pbar.set_text('Zakończono pobieranie pliku '+file_name)
            return True

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("bnm-dl")
        self.window.set_icon_from_file(get_resource_path("icon.png"))
        self.label = gtk.Label("<b>Było... nie minęło. Kronika zwiadowców historii</b>")
        self.label.set_use_markup(True)
        self.hbox = gtk.VBox(homogeneous=True, spacing=10)
        self.window.add(self.hbox)
        self.hbox.pack_start(self.label)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(5)

        # self.BNMlinks = [] + re.findall('<a href="/([0-9]{8})/[0-9]{8}">[\s]*<span class="image border-radius-5">', www.contents)      
        # self.BNMtitles = [] + re.findall('<span class="title">[\s]*([^>^<]*)[\s]*</span>', www.contents)
       
        self.BNMlinks = [] + re.findall('<a class="th mb10" href="http://www.tvp.pl/vod/audycje/historia/bylo-nie-minelo/wideo/[^/]*/([0-9]{6,10})">', www.contents)    
        self.BNMtitles = [] + re.findall('<a class="th mb10" href="http://www.tvp.pl/vod/audycje/historia/bylo-nie-minelo/wideo/[^"]*">([^<^>]*)', www.contents)

        if self.BNMlinks and len(self.BNMlinks) == len(self.BNMtitles):
            self.combobox_quality = gtk.combo_box_new_text()
            self.combobox_quality.insert_text(0, 'Jakość 1 - 320x180px')
            self.combobox_quality.insert_text(1, 'Jakość 2 - 398x224px')
            self.combobox_quality.insert_text(2, 'Jakość 3 - 480x270px')
            self.combobox_quality.insert_text(3, 'Jakość 4 - 640x360px')
            self.combobox_quality.insert_text(4, 'Jakość 5 - 800x450px')
            self.combobox_quality.insert_text(5, 'Jakość 6 - 960x540px')
            self.combobox_quality.set_active(5)
            self.quality = str(6)
            self.combobox = gtk.combo_box_new_text()
            for (i,title) in enumerate(self.BNMtitles):
                self.BNMtitles[i] = title.strip()
                self.combobox.insert_text(i, title.strip())
                # http://regionalna.tvp.pl/sess/html5player_iframe.php?object_id=14410596&width=100%&height=100%&autoplay=true&mobile=true/html5player_iframe.html
                # /14410596/16032014
                # http://46.28.242.12/token/video/vod/14410596/20140316/1440581241/17119a4d-4944-443f-a4c1-3e3a199dd624/video-6.mp4
            self.combobox.set_active(0)
            self.hbox.pack_start(self.combobox_quality)
            self.hbox.pack_start(self.combobox)
            self.button = gtk.Button("Pobierz wybrany odcinek")
        else:
            self.button = gtk.Button("Nie znaleziono żadnych filmów!")

        self.pbar = gtk.ProgressBar()
        self.hbox.pack_start(self.pbar)
        self.pbar.set_text('')
        self.pbar.show()

        self.button.connect("clicked", self.pobierzWybrany, None)
        # self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.hbox.pack_start(self.button)        
        self.button.show()        
       
        self.window.show_all()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    hello = WczytajFilmy()
    hello.main()
