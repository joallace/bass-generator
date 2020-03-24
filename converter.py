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
    for measure in track.measures:
        if measure.voices[0].beats[0].status == gp.models.BeatStatus.empty:
            continue
        for voice in measure.voices:
            for beat in voice.beats:
                if beat.status.value == 0:
                    continue
                file.write("%s" % 'b ' + str(beat.duration.value) + ' ' + str(int(beat.duration.isDotted)) + str(beat.status.value) + ' ' + str(beat.duration.tuplet.enters)  + str(beat.duration.tuplet.times)  + '\n')
                for note in beat.notes:
                    file.write("%s" % 'n ' + str(note.string) + ' ' +  str(note.value) + ' ' + str(note.type.value) + str(int(note.effect.hammer)) + str(note.effect.slides[0].value+3 if len(note.effect.slides) > 0 else '0') + '\n')
                    
def toGpx(file, track):   
    measure_header = gp.models.MeasureHeader()
    measure = gp.models.Measure(track, measure_header)
    
    measures = [measure]
    beats = []
    notes = []
    
    for i, line in enumerate(file):
        if line[:2] == 'b ':      # Beat
            if beats:
                beats[-1].notes = notes
                notes = []
                
                beat_sum = 0
                for b in beats:
                    if b.status.value == 0:
                        continue
                    beat_sum += b.duration.tuplet.times * (1/b.duration.value + (1/(2*b.duration.value))*b.duration.isDotted) / b.duration.tuplet.enters
                
                if beat_sum > 1:
                    new_beat = beats.pop(-1)
                    beats.append(gp.models.Beat(measures[-1].voices[0], status=gp.models.BeatStatus.empty))
                    
                    measure_header = gp.models.MeasureHeader()
                    measure = gp.models.Measure(track, measure_header)
                    measures.append(measure)
                    measures[-1].voices[0].beats = beats
                    
                    beats = [new_beat]
                
            parser = line.find(' ', 3)
            try:
                duration_value = int(line[2 : parser])
                duration_isDotted = bool(int(line[parser+1 : parser+2]))
                
                tuplet_enters = int(line[parser+4 : parser+5])
                tuplet_times = int(line[parser+5 : parser+6])
                duration_tuplet = gp.models.Tuplet(tuplet_enters, tuplet_times)
                
                beat_duration = gp.models.Duration(value=duration_value, isDotted=duration_isDotted, tuplet= duration_tuplet)
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
        
    beats[-1].notes = notes
    beats.append(gp.models.Beat(measures[-1].voices[0], status=gp.models.BeatStatus.empty))
    
    measure_header = gp.models.MeasureHeader()
    measure = gp.models.Measure(track, measure_header)
    measures.append(measure)
    measures[-1].voices[0].beats = beats
    track.measures = measures
    
    file.close()
    return track


if len(sys.argv) < 3:
    print('### Missing directory path or execution mode!\n### python converter.py --[txt/gpx] [input dir/input file] [output file]')
    sys.exit()
elif len(sys.argv) > 4:
    print('### Too many parameters!')
    sys.exit()

exec_mode = sys.argv[1]



if exec_mode ==  '--txt' or  exec_mode ==  '-t':
    if len(sys.argv) == 3:
        output_file = 'output.txt'
    else:
        output_file = sys.argv[3]
        
    src_path = sys.argv[2]
    output_file = open(output_file, 'w')
    
    for file in os.listdir(src_path):
        gpx_file = gp.parse(os.path.join(src_path, file))
        toTxt(output_file, gpx_file.tracks[0], os.path.splitext(file)[1])
        
    output_file.close()
    
elif exec_mode ==  '--gpx' or exec_mode ==  '-g':
    if len(sys.argv) == 3:
        output_file_name = 'output.gp5'
    else:
        output_file_name = sys.argv[3]
        
    input_file = open(sys.argv[2], 'r')
    output_file = gp.parse('input/reference.gp5') # Getting a blank .gp5 file for reference
    
    output_file.tracks[0] = toGpx(input_file, output_file.tracks[0])
    input_file.close()
    
    output_file.artist = 'JW'
    output_file.title = 'Funky Bass'
    gp.write(output_file, output_file_name)
    
else:
    print('### Invalid execution mode!')
