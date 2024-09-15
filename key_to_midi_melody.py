import mido
from mido import Message, MidiFile, MidiTrack
import random

# Define scales
major_scale_intervals = [2, 2, 1, 2, 2, 2, 1]
minor_scale_intervals = [2, 1, 2, 2, 1, 2, 2]

# MIDI note numbers for C0 to B8
note_numbers = {
    'C': 0, 'C#': 1, 'D': 2, 'D#':3, 'E':4, 'F':5, 'F#':6,
    'G':7, 'G#':8, 'A':9, 'A#':10, 'B':11
}

def build_scale(key='C', scale_type='major'):
    """Build a list of MIDI note numbers for the given key and scale type."""
    if scale_type == 'major':
        intervals = major_scale_intervals
    elif scale_type == 'minor':
        intervals = minor_scale_intervals
    else:
        raise ValueError("scale_type must be 'major' or 'minor'")

    # Starting note number for the key (assuming octave 4)
    start_note = note_numbers[key] + 12 * 4

    scale = [start_note]
    current_note = start_note
    for interval in intervals:
        current_note += interval
        scale.append(current_note)
    return scale

def generate_melody(scale, length=16):
    """Generate a random melody from the given scale."""
    melody = []
    for _ in range(length):
        # Choose a note from the scale
        note = random.choice(scale)
        # Randomly decide whether to add an embellishment
        embellish = random.choice([True, False])
        if embellish:
            # Add a grace note (a quick neighboring note)
            grace_note = note + random.choice([-1, 1])
            melody.append({'note': grace_note, 'duration': 0.1})
        # Main note
        melody.append({'note': note, 'duration': 0.5})
    return melody

def save_melody_to_midi(melody, filename='melody.mid', tempo=500000):
    """Save the melody to a MIDI file."""
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set tempo
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    # Time in ticks
    time = 0
    for note_info in melody:
        note = note_info['note']
        duration = note_info['duration']
        # Convert duration to ticks
        ticks = int(mido.second2tick(duration, mid.ticks_per_beat, tempo))
        # Note on
        track.append(Message('note_on', note=note, velocity=64, time=time))
        # Note off
        track.append(Message('note_off', note=note, velocity=64, time=ticks))
        time = 0  # Reset time after first note

    mid.save(filename)
    print(f"Melody saved to {filename}")

if name == 'main':
    # User inputs
    key = input("Enter the key (e.g., C, D#, F): ").strip()
    scale_type = input("Enter the scale type ('major' or 'minor'): ").strip()
    length = int(input("Enter the length of the melody (number of notes): "))
    tempo_bpm = int(input("Enter the tempo in BPM (e.g., 120): "))
    filename = input("Enter the output MIDI filename (e.g., 'melody.mid'): ").strip()

    # Convert BPM to microseconds per beat for MIDI tempo
    tempo = mido.bpm2tempo(tempo_bpm)

    # Build scale
    scale = build_scale(key, scale_type)

    # Generate melody
    melody = generate_melody(scale, length)

    # Save to MIDI
    save_melody_to_midi(melody, filename, tempo)