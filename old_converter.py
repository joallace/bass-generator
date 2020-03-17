#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 23:54:39 2020

@author: j-wallace
"""

import os
import sys
import guitarpro as gp

def toTxt(file, track, input_format):
    insert_empty = input_format != '.gp5'
    first_line = False
    for measure in track.measures:
        if measure.voices[0].beats[0].status == gp.models.BeatStatus.empty:
            continue
        if insert_empty and first_line:
            file.write('b 4 00\n')
        file.write("%s" % 'm ' + str(measure.timeSignature.numerator) + ' ' + str(measure.timeSignature.denominator.value)+ '\n')
        first_line = True
        for voice in measure.voices:
            for beat in voice.beats:
                file.write("%s" % 'b ' + str(beat.duration.value) + ' ' + str(int(beat.duration.isDotted)) + str(beat.status.value) + '\n')
                for note in beat.notes:
                    file.write("%s" % 'n ' + str(note.string) + ' ' +  str(note.value) + ' ' + str(note.type.value) + str(int(note.effect.hammer)) + str(note.effect.slides[0].value+3 if len(note.effect.slides) > 0 else '0') + '\n')
                    
    if insert_empty:
            file.write('b 4 00\n')
                    
def toGpx(file, track):   
    measures = []
    beats = []
    notes = []
    
    for i, line in enumerate(file):
        if line[:2] == 'm ':        # Measure
            if measures:
                measures[-1].voices[0].beats = beats
                beats = []
                
            parser = line.find(' ', 3)
            try:
                sig_num = int(line[2 : parser])
                sig_dem = int(line[parser+1 : line.find('\n', parser)])
                time_signature = gp.models.TimeSignature(numerator=sig_num, denominator=gp.models.Duration(value=sig_dem))
            except ValueError:
                print('Invalid TimeSignature in line:', i+1)
                break
            
            measure_header = gp.models.MeasureHeader(timeSignature=time_signature)
            measure = gp.models.Measure(track, measure_header)
            measures.append(measure)
            
        elif line[:2] == 'b ':      # Beat
            if beats:
                beats[-1].notes = notes
                notes = []
                
            parser = line.find(' ', 3)
            try:
                duration_value = int(line[2 : parser])
                duration_isDotted = bool(int(line[parser+1 : parser+2]))
                beat_duration = gp.models.Duration(value=duration_value, isDotted = duration_isDotted)
            except ValueError:
                print('Invalid BeatDuration in line:', i+1)
                break
            
            try:
                beat_status = int(line[parser+2 : parser+3])
                beat_status = gp.models.BeatStatus(beat_status)
                beat = gp.models.Beat(measures[-1].voices[0], duration=beat_duration, status=beat_status)
            except ValueError:
                print('Invalid BeatStatus in line:', i+1)
                break
            except IndexError:
                print('Beat before a Measure in line:', i+1)
                break

            beats.append(beat)
            
        elif line[:2] == 'n ':      # Note
            parser = line.find(' ', 4)
            try:
                note_string = int(line[2:3])
                note_value = int(line[4:parser])
                
                note_type = int(line[parser+1 : parser+2])
                note_type = gp.models.NoteType(note_type)
            except ValueError:
                print('Invalid Note String, Value or Type in line:', i+1)
                break
            
            try:
                effect_hammer = bool(int(line[parser+2 : parser+3]))
                effect_slides = []
                slide = int(line[parser+3 : parser+4])-3
                if slide > 0:
                    effect_slides.append(slide)
                note_effect = gp.models.NoteEffect(hammer=effect_hammer,slides=effect_slides)
            except ValueError:
                print('Invalid NoteEffect in line:', i+1)
                break
            
            try:    
                note = gp.models.Note(beats[-1], effect=note_effect, type=note_type, string=note_string, value=note_value) 
            except ValueError:
                print('Invalid Note String, Value or Type in line:', i+1)
                break
            except IndexError:
                print('Note before a Beat in line:', i+1)
                break
                
            notes.append(note)
        
    measures[-1].voices[0].beats = beats
    track.measures = measures
    
    file.close()
    return track


if len(sys.argv) < 3:
    print('### Missing directory path or execution mode!\n### python converter.py --[txt/gpx] [input dir/output file]')
    sys.exit()
elif len(sys.argv) > 3:
    print('### Too many parameters!')
    sys.exit()

exec_mode = sys.argv[1]

if exec_mode ==  '--txt' or  exec_mode ==  '-t':
    src_path = sys.argv[2]
    output_file = open('output.txt', 'w')
    
    for file in os.listdir(src_path):
        gpx_file = gp.parse(os.path.join(src_path, file))
        toTxt(output_file, gpx_file.tracks[0], os.path.splitext(file)[1])
        
    output_file.close()
    
elif exec_mode ==  '--gpx' or exec_mode ==  '-g':
    input_file = open(sys.argv[2], 'r')
    output_file = gp.parse('reference.gp5') # Getting a blank .gp5 file for reference
    
    output_file.tracks[0] = toGpx(input_file, output_file.tracks[0])
    input_file.close()
    
    output_file.artist = 'JW'
    output_file.title = 'Funky Bass'
    gp.write(output_file, 'output.gp5')
    
else:
    print('### Invalid execution mode!')
