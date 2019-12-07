from mido import MidiFile

midi = MidiFile('christmas-is-you.mid')

for i, track in enumerate(midi.tracks):
    print(f"Track {i}: {track.name}")
    for msg in track:
        print(msg)
