#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import pycurl
from download import download

class PobierzStrone:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf


class BnmDl(object):
    def getin(self):
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

    def separator(self, sign='-'):
        rows, columns = os.popen('stty size', 'r').read().split()
        columns = int(columns)
        separator = ''
        for x in range(0, columns):
            separator = separator + sign
        print separator

    def klawisz(self, answer):
        if (answer == 1):
            return 1
        else:
            print "Czy zapisać odcinek? ([t]ak / [n]ie / [z]akoncz)"
            key = self.getin()
            if key == 'z' or key == 'Z':
                self.separator('#')
                exit()
            if key == 't' or key == 'T':
                return 1
            else:
                return 0

    def pobierzOdcinek(self, title, link):
        www_filmu = PobierzStrone()
        c = pycurl.Curl()
        c.setopt(c.URL, 'www.tvp.pl/sess/tvplayer.php?object_id=' + link[2])
        c.setopt(c.HEADER, 1);
        c.setopt(c.HTTPHEADER, ['Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language: pl,en-us;q=0.7,en;q=0.3',
                                'Accept-Charset: ISO-8859-2,utf-8;q=0.7,*;q=0.7',
                                'Content-Type: application/x-www-form-urlencoded'])
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.USERAGENT, 'Mozilla/5.0 (X11; U; Linux i686; pl; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3')
        c.setopt(c.REFERER, 'www.tvp.pl/sess/tvplayer.php?object_id=' + link[2])
        c.setopt(c.WRITEFUNCTION, www_filmu.body_callback)
        c.perform()
        c.close()
        url = re.findall("{src:'([^']*)', type: 'video/mp4'}", www_filmu.contents)[0]
        url = url.replace('video-4.mp4', 'video-6.mp4')
        file_name = link[2] + '-' + title + '.mp4'.replace(' ', '_');
        wrong_characters = [' ', ':', '/', '\\']
        for c in wrong_characters:
            file_name = file_name.replace(c, '_')
        if (os.path.isfile(file_name)):
            print '[!] Plik o tej nazwie istnieje w katalogu docelowym'
        else:
            print url
            print file_name
            path = download(url, './'+file_name)
            print path
        return True

    def get_resource_path(self, rel_path):
        dir_of_py_file = os.path.dirname(__file__)
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource
