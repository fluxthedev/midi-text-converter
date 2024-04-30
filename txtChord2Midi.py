import pretty_midi
import os

def chord_symbol_to_note_numbers(chord_symbol):
    # Define a dictionary mapping note names to MIDI note numbers
    note_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    # Extract the root note from the chord symbol
    root_note = chord_symbol[0]
    
    # Get the MIDI note number for the root note
    root_midi_note = note_map[root_note]

    # Determine the chord type and additional notes
    if 'm' in chord_symbol:
        # Minor chord
        notes = [root_midi_note, root_midi_note + 3, root_midi_note + 7]
    else:
        # Major chord
        notes = [root_midi_note, root_midi_note + 4, root_midi_note + 7]

    # Check for additional notes
    if '7' in chord_symbol:
        notes.append(root_midi_note + 10)
    if '9' in chord_symbol:
        notes.append(root_midi_note + 14)
    if '6' in chord_symbol:
        notes.append(root_midi_note + 9)

    # Adjust the octave
    notes = [note + 60 for note in notes]

    return notes

def text_to_midi_chords(input_file):
    # Create a PrettyMIDI object
    midi_data = pretty_midi.PrettyMIDI()

    # Create an instrument (piano)
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)

    # Set the tempo (e.g., 120 beats per minute)
    tempo = 120

    # Set the duration of each chord (in seconds)
    chord_duration = 60 / tempo * 4  # 4 beats per measure

    # Open the input file for reading
    with open(input_file, 'r') as file:
        lines = file.readlines()

        # Set the start time for the first chord
        start_time = 0

        for line in lines:
            chords = line.strip().split('|')[1:-1]  # Exclude the first and last empty elements

            for chord_symbol in chords:
                chord_symbol = chord_symbol.strip()

                if chord_symbol:
                    # Convert the chord symbol to MIDI notes
                    notes = chord_symbol_to_note_numbers(chord_symbol)

                    # Create Note objects for each note in the chord
                    for note_number in notes:
                        note = pretty_midi.Note(
                            velocity=100,  # Default velocity (loudness)
                            pitch=note_number,
                            start=start_time,
                            end=start_time + chord_duration
                        )
                        piano.notes.append(note)

                    # Update the start time for the next chord
                    start_time += chord_duration

    # Add the piano instrument to the PrettyMIDI object
    midi_data.instruments.append(piano)

    # Get the current directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the output file path
    output_file = os.path.join(current_dir, 'chord_progression.mid')

    # Write the MIDI data to the output file
    midi_data.write(output_file)

    print(f"Text file converted to MIDI. Output saved as '{output_file}'.")

# Specify the input text file
input_file = 'chord.txt'

# Call the function to convert text to MIDI
text_to_midi_chords(input_file)