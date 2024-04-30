from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

def parse_melody_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    melody_data = []
    tempo = 120  # Default tempo
    time_signature = None

    for line in lines:
        line = line.strip()
        if line.startswith('Tempo:'):
            tempo = int(line.split(':')[1].strip().split(' ')[0])
        elif line.startswith('Time Signature:'):
            time_signature = line.split(':')[1].strip()
        elif line.startswith('Note:'):
            note_data = {}
            note_data['Note'] = line.split(':')[1].strip()
        elif line.startswith('Position:'):
            note_data['Position'] = line.split(':')[1].strip()
        elif line.startswith('Duration:'):
            duration = line.split(':')[1].strip().split(' ')[0]
            note_data['Duration'] = float(duration)
        elif line.startswith('Velocity:'):
            note_data['Velocity'] = int(line.split(':')[1].strip())
        elif line.startswith('Pitch Direction:'):
            if 'Note' in note_data:
                melody_data.append(note_data)
                note_data = {}

    if 'Note' in note_data:
        melody_data.append(note_data)

    return tempo, time_signature, melody_data

def create_midi_file(melody_data, tempo, output_file):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    tempo_bpm = bpm2tempo(tempo)
    track.append(MetaMessage('set_tempo', tempo=tempo_bpm))

    for note in melody_data:
        note_name = note['Note']
        position = note['Position']
        duration = note['Duration']
        velocity = note['Velocity']

        note_number = {
            'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
            'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
            'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11, 'Cb': 11
        }[note_name[:-1]]
        octave = int(note_name[-1])
        note_number += octave * 12

        track.append(Message('note_on', note=note_number, velocity=velocity, time=0))
        track.append(Message('note_off', note=note_number, velocity=0, time=int(duration * 480)))

    mid.save(output_file)

# Usage
melody_file = 'melody.txt'
output_file = 'melody.mid'

tempo, time_signature, melody_data = parse_melody_data(melody_file)
create_midi_file(melody_data, tempo, output_file)
print(f"MIDI file '{output_file}' created successfully.")