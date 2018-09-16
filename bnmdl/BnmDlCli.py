#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BnmDl.py-cli
# Autor: Bohdan Bobrowski bohdan@bobrowski.com.pl

from lxml import etree
import pycurl
import sys

from bnmdl.BnmDl import BnmDl, PobierzStrone

def main():
    SAVE_ALL = 0
    if '-t' in sys.argv or '-T' in sys.argv:
        SAVE_ALL = 1

    www = PobierzStrone()
    c = pycurl.Curl()
    bnm_url = 'https://vod.tvp.pl/website/bylo-nie-minelo,356/video'
    if '-o' in sys.argv or '-O' in sys.argv:
        bnm_url += '?order=oldest&sezon=0'
    c.setopt(c.REFERER, bnm_url)
    c.setopt(c.URL, bnm_url)
    c.setopt(c.HEADER, 1);
    c.setopt(c.HTTPHEADER, ['Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language: pl,en-us;q=0.7,en;q=0.3','Accept-Charset: ISO-8859-2,utf-8;q=0.7,*;q=0.7','Content-Type: application/x-www-form-urlencoded'])
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.USERAGENT,'Mozilla/5.0 (X11; U; Linux i686; pl; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3')
    c.setopt(c.WRITEFUNCTION, www.body_callback)
    c.perform()
    c.close()

    tree = etree.HTML(www.contents)
    chapters = tree.xpath("//div[contains(@class, 'strefa-abo__item')]")

    bnmdl = BnmDl()

    for chapter in chapters:
        link = next(iter(chapter.xpath('a') or []), None)
        print link
        if link is not None:
            link = link.attrib['href'].split(',')
        title = next(chapter.iter("h4")).text.strip()
        if len(link) > 2:
            bnmdl.separator('-')
            print title, '-', link[2]
            if(bnmdl.klawisz(SAVE_ALL) == 1):
                bnmdl.pobierzOdcinek(title, link)
