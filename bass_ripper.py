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
    print('### Missing directory path!')
    sys.exit()
elif len(sys.argv) > 3:
    print('### Too many parameters!')
    sys.exit()
    
if len(sys.argv) == 3:
    out_path = sys.argv[2]
else:
    out_path = 'out'
    try:  
        os.mkdir(out_path)
    except OSError as error: 
        print(error)
    
src_path = sys.argv[1]
    
print('Parsing files...')
for root, dirs, files in os.walk(src_path):
    for file in fnmatch.filter(files, supportedExtensions):
        try:
            song = gp.parse(os.path.join(src_path, file))
        except gp.GPException as exception:
            print('### This is not a supported GuitarPro file:', song, ':', exception)
        file_split = os.path.splitext(file)
        for track in song.tracks:
            if not track.isPercussionTrack:
                if len(track.strings) == 4 or len(track.strings) == 5:
                    print(file)
                    song.tracks.clear()
                    song.tracks.append(track)
                    gp.write(song, os.path.join(out_path, file_split[0] + ' - ' + track.name + file_split[1]))
                    break
