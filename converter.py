#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 23:54:39 2020

@author: j-wallace
"""

import os
import sys
import guitarpro as gp

def toTxt(file, track):
    for measure in track.measures:
        file.write("%s" % 'm:' + str(measure.timeSignature.numerator) + ',' + str(measure.timeSignature.denominator.value)+ '\n')
        for voice in measure.voices:
            for beat in voice.beats:
                file.write("%s" % 'b:' + str(beat.duration.value) + ',' + str(int(beat.duration.isDotted)) + ',' + str(beat.status.value) + '\n')
                for note in beat.notes:
                    file.write("%s" % 'n:' + str(note.string) + ',' + str(note.value) + ' ' + str(note.type.value) + ',' + str(int(note.effect.hammer)) + '\n')
                    
def toGpx(file, track):
    measures = []
    beats = []
    notes = []

    
    for line in file:
        if line[:2] == 'm:':        # Measure
            if measures:
                finish_beat = gp.models.Beat(measures[-1].voices[0], status=gp.models.BeatStatus.empty)
                
                if beats[-1].status != gp.models.BeatStatus.empty:
                    beats.append(finish_beat)
                    
                measures[-1].voices[0].beats = beats
                beats = []
                
            parser = line.find(',')
            sig_num = int(line[2 : parser])
            sig_dem = int(line[parser+1 : line.find('\n', parser)])
            time_signature = gp.models.TimeSignature(numerator=sig_num, denominator=gp.models.Duration(value=sig_dem))
            
            measure_header = gp.models.MeasureHeader(timeSignature=time_signature)
            measure = gp.models.Measure(track, measure_header)
            measures.append(measure)
            
        elif line[:2] == 'b:':      # Beat
            if beats:
                beats[-1].notes = notes
                notes = []
                
            parser = line.find(',')
            duration_value = int(line[2 : parser])
            duration_isDotted = bool(int(line[parser+1 : parser+2]))
            beat_duration = gp.models.Duration(value=duration_value, isDotted = duration_isDotted)
            
            parser = line.find(',', parser+1)
            beat_status = int(line[parser+1 : parser+2])
            beat_status = gp.models.BeatStatus(beat_status)

            beat = gp.models.Beat(measures[-1].voices[0], duration=beat_duration, status=beat_status)
            beats.append(beat)
            
        elif line[:2] == 'n:':      # Note
            parser = line.find(' ')
            note_string = int(line[2:3])
            note_value = int(line[4:parser])
            
            note_type = int(line[parser+1 : line.find(',', parser)])
            note_type = gp.models.NoteType(note_type)
            
            parser = line.find(',', parser)
            effect_hammer = bool(int(line[parser+1 : parser+2]))
            note_effect = gp.models.NoteEffect(hammer=effect_hammer)
                
            note = gp.models.Note(beats[-1], effect=note_effect, type=note_type, string=note_string, value=note_value) 
            notes.append(note)
    
    measures[-1].voices[0].beats = beats

    track.measures = measures
    
    return track


if len(sys.argv) < 3:
    print('### Missing directory path or execution mode!\n### converter.py -[txt/gpx] [input dir/output file]')
    sys.exit()
elif len(sys.argv) > 3:
    print('### Too many parameters!')
    sys.exit()

exec_mode = sys.argv[1]

if exec_mode ==  '--txt' or  exec_mode ==  '-t':
    src_path = sys.argv[2]
    output_file = open('output.txt', 'w')
    
    for gpx_file in os.listdir(src_path):
        src_file = gp.parse(os.path.join(src_path, gpx_file))
        toTxt(output_file, src_file.tracks[0])
        # output_file.write('\n\n\n\n')
        
    output_file.close()
    
elif exec_mode ==  '--gpx' or exec_mode ==  '-g':
    input_file = open('output.txt', 'r')
    output_file = gp.parse('reference.gp5') # Getting a blank .gp5 file for reference

    for measure in output_file.tracks[0].measures:  # Cleaning file
        for voice in measure.voices:
            for beat in voice.beats:
                beat.notes = []
    
    output_file.tracks[0] = toGpx(input_file, output_file.tracks[0])
    input_file.close()
    
    output_file.artist = 'JW'
    output_file.title = 'Funky Bass'
    gp.write(output_file, sys.argv[2])
    
else:
    print('### Invalid execution mode!')