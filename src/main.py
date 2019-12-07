#!/usr/bin/env python

import sys
from sys import argv
from mido import MidiFile

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

beat_length = 96

if len(argv) <= 1:
    print("First argument must be path to midi file, help, or dump")
    exit(1)

if argv[1] == "help":
    print("(program name) help                                                           | prints help")
    print("(program name) dump [midi filename]                                           | dumps midi info to stdout")
    print("(program name) [midi filename] [track name(s)] -t[beat length in midi time]   | prints output chime notation to stdout")
    exit(0)

if argv[1] == "dump":
    midi = MidiFile(argv[2])
    for track in midi.tracks:
        print(f"---- track {track.name} ----")
        for msg in track:
            print(msg)
        print("\n\n")
    exit(0)

midi = MidiFile(argv[1])

if len(argv) <= 2:
    print("Remaining arguments must be midi track names to add to chime notation output")

    print("\nAvailable tracks: ",end='')

    for i, track in enumerate(midi.tracks):
        print(track.name + ", ", end='')
    print()

target_tracks = argv[2:]

for i, arg in enumerate(target_tracks):
    if arg[0:2] == "-t":
        beat_length = int(arg[2:])
        del target_tracks[i]

track_name_to_track = {}
for track in midi.tracks:
    track_name_to_track[track.name] = track

for track in target_tracks:
    if not track in track_name_to_track.keys():
        print(f"Unable to find track '{track}' in midi file")
        exit(1)

class Warning:
    def __init__(self, track_name, time, msg):
        self.track_name = track_name
        self.time = time
        self.msg = msg

track_name_to_length = {}
warning_messages = [] # list of warnings

for track_name in target_tracks:
    track = track_name_to_track[track_name]
    print(f"{track.name}: ",end='')
    cur_time = 0.0
    for msg in track:
        to_print = ""
        if msg.type == "note_on":
            to_print = "__"
        elif msg.type == "note_off":
            if msg.note < 66 or msg.note > 82:
                warning_messages.append(Warning(track.name, cur_time, f"Note {msg.note} is out of range"))
                continue # skip over bad note
            to_print = str(msg.note - 66 + 3).zfill(2)

        if msg.time % beat_length != 0:
            warning_messages.append(Warning(track.name, cur_time, f"Time {msg.time} is not a whole number of beat length {beat_length}"))
            continue # bad note, skip!

        for _ in range(int(msg.time/beat_length)):
            print(f"{to_print} ", end='')

        cur_time += msg.time
    print("\n")
    track_name_to_length[track.name] = cur_time

eprint("\n\n\n")
eprint("-- WARNINGS --")
for w in warning_messages:
    eprint(f"{w.track_name} {w.time/track_name_to_length[w.track_name]} of the way through: {w.msg}\n")
