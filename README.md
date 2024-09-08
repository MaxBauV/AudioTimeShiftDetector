# Audio Time Shift Detector

Analyse time shift between .wav files.
Returns time shift in sample points & milliseconds.

## Use-cases / Application Examples

### Time align audio tracks (e.g. multi mic setup to avoid phase issues)

You, for example, record a snare drum with 2 microphones.

1) Check that the phase is not inverted
2) Analyze both records with the script
3) Adjust the timing of one of the tracks inside your DAW

### Time align Multi-way Loudspeaker systems (e.g. bi-amped speaker, sub & satellite, surround systems, etc.)

In this example we are using the Audio Time Shift Detector to time-align a Multi-Way Multi-Amped Soundsystem.

Therefore we want to measure the time shift between a  reference and each speaker.

![alt text](img/Multi-Way.drawio.png "Title")

The reference is an analog loopback. The test file is played to each speaker at a time. Both the measurement microphone signal (which is optimally placed at the listeners position) and the reference signal (loopback) are recorded at each run.

Example:
1) Tweeter:
    - Play the test file to the tweeter (Out Channel 1) and the loopback (Out Channel 4)
    - Record the analog loopback as well as the Microphone (In Channels 1 & 2)
    - Run the script on thos two files, note the time shift.
2) Mid Range
    - Play the test file to the midrange seaker (Out Channel 2) and the loopback (Out Channel 4).
    - Record the analog loopback as well as the Microphone (In Channels 1 & 2)
    - Run the script on thos two files, note the time shift.
3) Analyse
    - Calculate the difference between Tweeter and Midrange


## Usage

Export the audio files and put them into a folder.
Make sure that the the sample rate of all audio files match.

This script supports a wide range of file types.

Tested file types:
- Sample Rate of:
    - 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 176400, 192000
- Bit Depth of:
    - PCM: 8, 12, 24, 32
    - FP: 32, 64

The script supports mono and stereo files. In case you want to use stereo files, make sure that both channels have the same content, otherwise the results may be wrong and therefore an error is thrown.

### Script Execution

```atsDetect.py '/path/to/folder'```

In ```dist``` you can find a compiled version for MacOS. It was compiled using pyinstaller. Execute it as follows:

```atsDetects '/path/to/folder'```

Compiled versions for Linux & Windows are not planned.

## Testing

In the ```testing``` directory you can find the Reaper project I have used for testing & verification.

Track 1 contains the unchanged test file.
Track 2 & track 3 contain copies of that file but with apllied filters which mimic a frequency response change (e.g. to mimic a crossover of a speaker system). If the reaFIR filter's edit mode is set to ```precise``` it does not influence the phase.
You can play around with other EQs and filters to see that the resuklting phase shift creates an additional time shift.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
