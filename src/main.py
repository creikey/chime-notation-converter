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

target_tracks = argv[2:]

track_name_to_track = {}
for track in midi.tracks:
    track_name_to_track[track.name] = track

for track in target_tracks:
    if not track in track_name_to_track.keys():
        print(f"Unable to find track '{track}' in midi file")
        exit(1)
