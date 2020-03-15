#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 13:58:42 2020

@author: j-wallace
"""

import sys
import os
import fnmatch

import guitarpro as gp

supportedExtensions = '*.gp[345]'

if len(sys.argv) < 2:
    print('###Missing directory path!')
    sys.exit()
elif len(sys.argv) > 3:
    print('###Too many parameters!')
    sys.exit()
    
if len(sys.argv) == 3:
    outpath = sys.argv[2]
else:
    outpath = 'out'
    try:  
        os.mkdir(outpath)
    except OSError as error: 
        print(error)
    
srcpath = sys.argv[1]
    
print('Parsing files...')
for root, dirs, files in os.walk(srcpath):
    for file in fnmatch.filter(files, supportedExtensions):
        try:
            song = gp.parse(os.path.join(srcpath, file))
        except gp.GPException as exception:
            print('###This is not a supported GuitarPro file:', song, ':', exception)
        for track in song.tracks:
            if not track.isPercussionTrack:
                if len(track.strings) == 4 or len(track.strings) == 5:
                    print(file)
                    song.tracks.clear()
                    song.tracks.append(track)
                    gp.write(song, os.path.join(outpath, os.path.splitext(file)[0] + ' - ' + track.name + '.gp5'))
