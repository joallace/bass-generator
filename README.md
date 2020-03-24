# bass-generator
A bass tab generator using a LSTM approach

## Contents
- [Motivation](#Motivation)
- [Dependencies](#Dependencies)
- [Data](#Data)
- [Scripts](#Scripts)

## Motivation

The purpose of this Artificial Intelligence project is to create bass riffs based on playing patterns from different bands and musics from the *funk rock* genre.

## Dependencies
This software depends on the following third party libraries to be executed:
- **[TensorFlow](https://www.tensorflow.org/)**: version 2.0 or later
```shell
$ pip install tensorflow
```
- **[PyGuitarPro](https://github.com/Perlence/PyGuitarPro)**: version 0.6 or later
```shell
$ pip install PyGuitarPro
```

## Scripts
First of all, I would like to point out that when referring to the **. gpx ** format, I am actually referring to the Guitar Pro .gp3, .gp4 and .gp5 formats\
The execution of the scripts is done exclusively in the terminal. Below are their descriptions.

### bass_ripper.py

This script makes it possible to *rip* the bass track from .gpx files in a certain directory.

```bash
python bass_ripper.py [input dir] [output dir]
```
**ALWAYS** perform the *rip* of the bass tracks before converting any file.

### converter.py
This script, as its name suggests, will be responsible for converting files. There are two execution methods, from .gpx to .txt and from .txt to .gpx.

**Conversion to .txt:**

Specifying an output file is optional, the default output is "output.txt".
```bash
python converter.py [-t or --txt] [input dir] [output file]
```
The generated file will be written as follows: (see [PyGuitarPro docs](https://pyguitarpro.readthedocs.io) for better understanding)

1. Beat

```bash
b D OT NM
```
A line that represents a beat will always start with a **b**, and will have the five following parameters:
 - D: duration of the beat
 - O: specifies if the note is dotted
 - T: type of the beat 
 - E: tuplet enters
 - M: tuplet tempo


2. Note

```bash
n S N THL
```
A line that represents a note will always start with a **n**, and will have the five following parameters:
 - S: bass string
 - N: played note
 - T: note type
 - H: presence of hammer-on
 - L: presence of slide

**Conversion to .gpx:**

Specifying an output file is optional, the default output is "output.gp5". Note that it is preferable to generate files with the **.gp5** extension

```bash
python converter.py [-g or --gpx] [input file] [output file]
```
