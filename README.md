# MIDI Text Converter

This repository contains Python scripts for converting between MIDI files and text format, making it easier to manipulate MIDI data in a human-readable form. 
This also allows me to leverage generative AI feedback for music theory by converting midi to a readable text format with track information.

## Script Overview

### **midi2Text.py**
- **Purpose:** Converts MIDI files to a text representation.
- **Description:** This script loads a MIDI file and extracts notes from the first instrument track (typically piano). It outputs the note name, position, duration, and pitch direction (up, down, or same as the previous note) to a text file.

### text2Midi.py
- **Purpose:** Converts text files describing melody back to MIDI format.
- **Description:** Reads a text file which lists musical notes with attributes like tempo, time signature, and velocity. It processes this information to generate a MIDI file with corresponding MIDI events.

### txtChord2Midi.py
- **Purpose:** Converts chord symbols from a text file into MIDI.
- **Description:** The script reads chord symbols (like C, Em, G7) from a text file, determines the MIDI note numbers for these chords, and creates a MIDI file with these chords laid out over time.

## Usage

To use these scripts, you need Python and relevant music libraries installed. Ensure you have pretty_midi and mido installed in your Python environment to handle MIDI operations.

Each script can be run individually, with specific input files that they process as defined in their respective usage sections within the script. Modify the paths and parameters as necessary for your specific needs.

## Contributing

Contributions to enhance the functionality or the efficiency of these scripts are welcome. Please follow the standard pull request process to propose your changes.

## License

The repository is typically under an open source license, which allows for modification and distribution with attribution.
