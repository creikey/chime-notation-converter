#!/usr/bin/env python

from sys import argv
from mido import MidiFile

if len(argv) <= 1:
    print("First argument must be path to midi file")
    exit(1)

midi = MidiFile(argv[1])

if len(argv) <= 2:
    print("Remaining arguments must be midi track names to add to chime notation output")

    print("\nAvailable tracks: ",end='')

    for i, track in enumerate(midi.tracks):
        print(track.name + ", ", end='')
    print()
