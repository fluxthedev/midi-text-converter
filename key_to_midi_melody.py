import mido
from mido import Message, MidiFile, MidiTrack
import random

# ... (rest of the code remains the same)

def generate_rhythm(scale, length):
    """Generate a random rhythm pattern for each note."""
    rhythm = []
    for _ in range(length):
        note_duration = random.choice([0.25, 0.5, 0.75, 1.0])  # quarter, half, three-quarters, whole note
        rhythm.append({'duration': note_duration, 'rest': random.choice([True, False])})
    return rhythm

def generate_chord_progression(key, scale_type, length):
    """Generate a chord progression based on the key and scale type."""
    chords = []
    if scale_type == 'major':
        chord_intervals = [4, 3, 2, 2, 1, 1, 4]
    elif scale_type == 'minor':
        chord_intervals = [3, 2, 2, 1, 1, 4, 3]
    else:
        raise ValueError("scale_type must be 'major' or 'minor'")

    start_note = note_numbers[key] + 12 * 4
    for i in range(length):
        chord_root = start_note + sum(chord_intervals[:i])
        chord_type = random.choice(['major', 'minor', 'diminished', 'augmented'])
        chords.append({'root': chord_root, 'type': chord_type})
    return chords

def add_pitch_bending(melody, probability=0.2):
    """Add random pitch bending to certain notes."""
    for note_info in melody:
        if random.random() < probability:
            bend_amount = random.uniform(-1, 1)  # +/- 1 semitone
            note_info['bend'] = bend_amount
    return melody

def add_dynamic_markings(melody, probability=0.5):
    """Add random dynamic markings to the melody."""
    dynamics = ['ff', 'f', 'mf', 'mp', 'p']
    for note_info in melody:
        if random.random() < probability:
            note_info['dynamic'] = random.choice(dynamics)
    return melody

def generate_multiple_melodies(scale, length, num_melodies):
    """Generate multiple melodies."""
    melodies = []
    for _ in range(num_melodies):
        melody = generate_melody(scale, length)
        melodies.append(melody)
    return melodies

# ... (rest of the code remains the same)

# User inputs
key = input("Enter the key (e.g., C, D#, F): ").strip()
scale_type = input("Enter the scale type ('major' or 'minor'): ").strip()
length = int(input("Enter the length of the melody (number of notes): "))
tempo_bpm = int(input("Enter the tempo in BPM (e.g., 120): "))
filename = input("Enter the output MIDI filename (e.g., 'melody.mid'): ").strip()
num_melodies = int(input("Enter the number of melodies to generate: "))

# ... (rest of the code remains the same)

# Generate multiple melodies
melodies = generate_multiple_melodies(scale, length, num_melodies)

for i, melody in enumerate(melodies):
    # Add rhythm variation
    rhythm = generate_rhythm(scale, length)
    for note_info, rhythm_info in zip(melody, rhythm):
        note_info['duration'] = rhythm_info['duration']
        note_info['rest'] = rhythm_info['rest']

    # Add chord progression
    chords = generate_chord_progression(key, scale_type, length)
    for note_info, chord in zip(melody, chords):
        note_info['chord'] = chord

    # Add pitch bending
    melody = add_pitch_bending(melody)

    # Add dynamic markings
    melody = add_dynamic_markings(melody)

    # Save to MIDI
    filename_base, _ = filename.rsplit('.', 1)
    midi_filename = f"{filename_base}_{i+1}.mid"
    save_melody_to_midi(melody, midi_filename, tempo)

print(f"Generated {num_melodies} melodies and saved to {filename_base}*.mid")
