#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bnm-dl-cli - Proste pobieranie pobieranie filmów z cyklu "Było... nie minęło. Kronika zwiadowców historii"
# wersja 0.1 dla konsoli
# Autor: Bohdan Bobrowski bohdan@bobrowski.com.pl

import os
import json
import re
import sys
import pycurl
import urllib2

# Parametry podstawowe:
SAVE_ALL = 0
if '-t' in sys.argv or '-T' in sys.argv:
    SAVE_ALL = 1

def getin():
    if os.name == 'nt':
        from msvcrt import getch
        ch = getch()
    else:
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def Separator(sign='-'):
    rows, columns = os.popen('stty size', 'r').read().split()
    columns = int(columns)
    separator = ''
    for x in range(0, columns):
        separator = separator + sign
    print separator

def Klawisz(answer):
    if(answer == 1):
        return 1
    else:
        print "Czy zapisać odcinek? ([t]ak / [n]ie / [z]akoncz)"
        key = getin()
        if key == 'z' or key == 'Z':
            Separator('#')
            exit()
        if key == 't' or key == 'T':
            return 1
        else:
            return 0

class PobierzStrone:
    def __init__(self):
        self.contents = ''
    def body_callback(self, buf):
        self.contents = self.contents + buf
    
def pobierzOdcinek(odcinek):
    tytul_odcinka = odcinek[1]
    www_filmu = PobierzStrone()
    c = pycurl.Curl()
    c.setopt(c.URL, 'www.tvp.pl/sess/tvplayer.php?object_id='+odcinek[0])
    c.setopt(c.WRITEFUNCTION, www_filmu.body_callback)
    c.perform()
    c.close()
    url = re.findall("{src:'([^']*)', type: 'video/mp4'}",www_filmu.contents)[0]
    url = url.replace('video-4.mp4','video-6.mp4')
    fn = re.findall('token/video/vod/'+str(odcinek[0])+'/([0-9]{4})([0-9]{2})([0-9]{2})', www_filmu.contents)
    file_name = 'bylo-nie-minelo-'+fn[0][0]+fn[0][1]+fn[0][2]+'-'+tytul_odcinka+'.mp4'
    print url
    print file_name
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
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
    f.close()
    return True

def get_resource_path(rel_path):
    dir_of_py_file = os.path.dirname(__file__)
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource

www = PobierzStrone()
c = pycurl.Curl()
c.setopt(c.URL, 'http://vod.tvp.pl/shared/listing.php?parent_id=356&page=1&type=video&order=release_date_long,-1&filter={%22playable%22:true}&direct=false&template=directory/listing.html&count=12')
c.setopt(c.WRITEFUNCTION, www.body_callback)
c.perform()
c.close()

bnm = [] + re.findall('<strong[\s]+class="shortTitle">[\s]*<a[\s]+href="/([0-9]{6,10})/([^"]+)"[\s]+title="([^"]*)', www.contents)

for b in bnm:
    Separator('#')
    print b[1]
    if(Klawisz(SAVE_ALL) == 1):
        pobierzOdcinek(b)

