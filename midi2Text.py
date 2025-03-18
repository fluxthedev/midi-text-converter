import pretty_midi
import argparse
from datetime import timedelta


def format_time(seconds):
    """Convert seconds to a formatted time string (HH:MM:SS.ms)"""
    td = timedelta(seconds=seconds)
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{str(td.microseconds)[:3]}"


def get_dynamics_label(velocity):
    """Convert MIDI velocity to musical dynamics notation"""
    if velocity < 16:
        return "ppp (pianississimo)"
    elif velocity < 33:
        return "pp (pianissimo)"
    elif velocity < 49:
        return "p (piano)"
    elif velocity < 64:
        return "mp (mezzo-piano)"
    elif velocity < 80:
        return "mf (mezzo-forte)"
    elif velocity < 96:
        return "f (forte)"
    elif velocity < 112:
        return "ff (fortissimo)"
    else:
        return "fff (fortississimo)"


def midi_to_text(midi_file, output_file):
    # Load MIDI file
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    # Process each instrument in the MIDI file
    with open(output_file, 'w') as file:
        # Write global MIDI information
        file.write(f"=== MIDI File Analysis ===\n")
        file.write(f"Filename: {midi_file}\n")
        file.write(f"Resolution: {midi_data.resolution} ticks per beat\n")

        # Tempo information
        tempos = midi_data.get_tempo_changes()
        file.write(f"\nTempo Changes: {len(tempos[1])} changes\n")
        for time, tempo in zip(*tempos):
            file.write(f"  At {format_time(time)}: {tempo:.1f} BPM\n")

        # Time signature information
        file.write(f"\nTime Signature Changes: {len(midi_data.time_signature_changes)}\n")
        for ts in midi_data.time_signature_changes:
            file.write(f"  At {format_time(ts.time)}: {ts.numerator}/{ts.denominator}\n")

        # Key signature information
        file.write(f"\nKey Signature Changes: {len(midi_data.key_signature_changes)}\n")
        for ks in midi_data.key_signature_changes:
            file.write(f"  At {format_time(ks.time)}: {ks.key_number} ({ks.key_name})\n")

        file.write(f"\nTotal Duration: {format_time(midi_data.get_end_time())}\n")
        file.write(f"Total Instruments: {len(midi_data.instruments)}\n\n")

        # Statistics for all notes
        all_notes = []
        for instrument in midi_data.instruments:
            all_notes.extend(instrument.notes)

        if all_notes:
            avg_velocity = sum(note.velocity for note in all_notes) / len(all_notes)
            avg_duration = sum((note.end - note.start) for note in all_notes) / len(all_notes)
            file.write(f"Average Velocity: {avg_velocity:.1f}\n")
            file.write(f"Average Note Duration: {avg_duration:.3f} seconds\n\n")

        # Process each instrument
        for i, instrument in midi_data.instruments:
            instrument_name = pretty_midi.program_to_instrument_name(instrument.program)
            if instrument.is_drum:
                instrument_name += " (Drum Kit)"

            # Write instrument summary
            file.write(f"\n{'=' * 50}\n")
            file.write(f"Instrument {i+1}: {instrument_name}\n")
            file.write(f"{'=' * 50}\n")
            file.write(f"Total Notes: {len(instrument.notes)}\n")
            file.write(f"Program Number: {instrument.program}\n")
            file.write(f"Is Drum: {instrument.is_drum}\n")

            if instrument.notes:
                # Calculate instrument-specific statistics
                velocities = [note.velocity for note in instrument.notes]
                durations = [(note.end - note.start) for note in instrument.notes]
                pitches = [note.pitch for note in instrument.notes]

                file.write(f"\nStatistics:\n")
                file.write(f"  Pitch Range: {min(pitches)} to {max(pitches)} ")
                file.write(f"({pretty_midi.note_number_to_name(min(pitches))} to {pretty_midi.note_number_to_name(max(pitches))})\n")
                file.write(f"  Average Velocity: {sum(velocities)/len(velocities):.1f}\n")
                file.write(f"  Average Duration: {sum(durations)/len(durations):.3f} seconds\n\n")

            # Process each note in the instrument
            prev_note = None
            for note_idx, note in enumerate(instrument.notes, 1):
                note_name = pretty_midi.note_number_to_name(note.pitch)
                duration = note.end - note.start

                # Determine pitch direction and interval
                interval = "N/A"
                if prev_note is None:
                    pitch_direction = "Initial Note"
                else:
                    time_gap = note.start - prev_note.end
                    if note.pitch > prev_note.pitch:
                        pitch_direction = "Ascending"
                        interval = f"{note.pitch - prev_note.pitch} semitones"
                    elif note.pitch < prev_note.pitch:
                        pitch_direction = "Descending"
                        interval = f"{prev_note.pitch - note.pitch} semitones"
                    else:
                        pitch_direction = "Repeated Note"
                        interval = "Unison"

                # Write detailed note information
                file.write(f"Note {note_idx}:\n")
                file.write(f"  Pitch: {note_name} (MIDI {note.pitch})\n")
                file.write(f"  Start Time: {format_time(note.start)}\n")
                file.write(f"  End Time: {format_time(note.end)}\n")
                file.write(f"  Duration: {duration:.3f} seconds\n")
                file.write(f"  Velocity: {note.velocity} - {get_dynamics_label(note.velocity)}\n")
                file.write(f"  Motion: {pitch_direction}\n")
                file.write(f"  Interval: {interval}\n")
                if prev_note:
                    file.write(f"  Time Gap from Previous: {time_gap:.3f} seconds\n")
                file.write("\n")

                prev_note = note

    print(f"MIDI analysis complete. Output saved to '{output_file}'.")


# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Convert MIDI file to detailed text analysis.')
parser.add_argument('midi_file', type=str, help='Input MIDI file')
parser.add_argument('output_file', type=str, help='Output text file')
parser.add_argument('--verbose', '-v', action='store_true',
                   help='Print additional processing information')
args = parser.parse_args()

# Call the function to convert MIDI to text
midi_to_text(args.midi_file, args.output_file)
