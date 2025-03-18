import pretty_midi
import argparse


def midi_to_text(midi_file, output_file):
    # Load MIDI file
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    # Process each instrument in the MIDI file
    with open(output_file, 'w') as file:
        # Write global MIDI information
        file.write(f"MIDI File Analysis\n")
        file.write(f"Resolution: {midi_data.resolution} ticks per beat\n")
        file.write(f"Tempo Changes: {len(midi_data.get_tempo_changes()[1])} changes\n")
        file.write(f"Time Signature Changes: {len(midi_data.time_signature_changes)}\n")
        file.write(f"Total Duration: {midi_data.get_end_time():.2f} seconds\n\n")

        for instrument in midi_data.instruments:
            # Get the instrument name using the program number and whether it's a drum track
            instrument_name = pretty_midi.program_to_instrument_name(
                instrument.program)
            if instrument.is_drum:
                instrument_name += " (Drum Kit)"

            # Write instrument summary
            file.write(f"=== Instrument: {instrument_name} ===\n")
            file.write(f"Total Notes: {len(instrument.notes)}\n")
            file.write(f"Program Number: {instrument.program}\n")
            file.write(f"Is Drum: {instrument.is_drum}\n\n")

            # Process each note in the instrument
            prev_note = None
            for note in instrument.notes:
                # Get note name and octave
                note_name = pretty_midi.note_number_to_name(note.pitch)

                # Get note duration and timing
                duration = note.end - note.start
                start_time = note.start
                end_time = note.end

                # Get velocity information
                velocity = note.velocity
                velocity_str = "Soft" if velocity < 64 else "Loud"

                # Determine pitch direction and interval
                interval = "N/A"
                if prev_note is None:
                    pitch_direction = "N/A"
                else:
                    if note.pitch > prev_note.pitch:
                        pitch_direction = "Up"
                        interval = f"{note.pitch - prev_note.pitch} semitones"
                    elif note.pitch < prev_note.pitch:
                        pitch_direction = "Down"
                        interval = f"{prev_note.pitch - note.pitch} semitones"
                    else:
                        pitch_direction = "Same"
                        interval = "0 semitones"

                # Write note and instrument information to the output file
                file.write(f"Instrument: {instrument_name}\n")
                file.write(f"Note: {note_name}\n")
                file.write(f"Start Time: {start_time:.2f} seconds\n")
                file.write(f"End Time: {end_time:.2f} seconds\n")
                file.write(f"Duration: {duration:.2f} seconds\n")
                file.write(f"Velocity: {velocity} ({velocity_str})\n")
                file.write(f"Pitch Direction: {pitch_direction}\n")
                file.write(f"Interval from Previous: {interval}\n")
                file.write("\n")

                prev_note = note

    print(f"MIDI file converted to text. Output saved as '{output_file}'.")


# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Convert MIDI file to text representation.')
parser.add_argument('midi_file', type=str, help='Input MIDI file')
parser.add_argument('output_file', type=str, help='Output text file')
args = parser.parse_args()

# Call the function to convert MIDI to text
midi_to_text(args.midi_file, args.output_file)
