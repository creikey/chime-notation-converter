#!/usr/bin/env python

import sys
from mido import MidiFile

if len(sys.argv) <= 1:
    print("First argument must be path to midi file")
    exit(1)

midi = MidiFile('christmas-is-you.mid')

track_names = []

for i, track in enumerate(midi.tracks):
    track_names.append(track.name)

print("Available tracks: ",end='')
