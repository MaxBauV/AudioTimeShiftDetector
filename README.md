# Audio Time Shift Detector

Analyse time shift between several .wav files.
Returns time shift in sample points & milliseconds between all given .wav files.

The time shift is precisly calculated by utilizing a special measurement file and the usage of cross-corellation.

## Table Of Content

- [Audio Time Shift Detector](#audio-time-shift-detector)
  - [Table Of Content](#table-of-content)
  - [Usage ](#usage-)
    - [Supported File Types ](#supported-file-types-)
    - [Script Execution ](#script-execution-)
  - [Measurement File ](#measurement-file-)
  - [Use-cases / Application Examples ](#use-cases--application-examples-)
    - [Time align audio tracks (e.g. multi mic setup to avoid phase issues) ](#time-align-audio-tracks-eg-multi-mic-setup-to-avoid-phase-issues-)
    - [Time shift measurement to time align multi speaker setups ](#time-shift-measurement-to-time-align-multi-speaker-setups-)
      - [Example:](#example)
  - [Testing](#testing)
  - [License](#license)

## Usage <div id='usage'/>

Provide audio files in the .wav format within a folder.
Make sure that the the sample rate of all audio files match.

### Supported File Types <div id='file_types'/>

This script supports a wide range of file types.

Tested file types:
- Sample Rate of:
    - 8000, 11025, 16000, 22050, 32000, 44100, 48000, 88200, 96000, 176400, 192000
- Bit Depth of:
    - PCM: 8, 12, 24, 32
    - FP: 32, 64

The script supports mono and stereo files. In case you want to use stereo files, make sure that both channels have the same content, otherwise the results may be wrong and therefore, in that case, an error is thrown.

### Script Execution <div id='script_execution' />

```atsDetect.py '/path/to/folder'```

In ```dist``` you can find a compiled version for MacOS. It was compiled using pyinstaller. Execute it as follows:

```atsDetects '/path/to/folder'```

Compiled versions for Linux & Windows are not planned.

## Measurement File <div id='meas_file' />

Sometimes Dirac impulses are used for time-alignment mesurements.
Alterations in the frequency spectrum, however, causes signals to get smeared. 
A high-passed Dirac impulse, for example, is highly alterated and therefore not usable for many cenarios.

Utilizing sine wave sweeps is another possibility. However, in a scenario where we want to measure the time alignment between a subwoofer and a tweeter, it could happen that there is no frequency overlap in both signals.

White noise contains all frequencies and therefore seems optimal for this usage. For better results the white noise signal is pulsed. A short sequence of noise is followed by short sequence of silence. The resulting sequence of noise and subsequent silence is repeated 6 times and, in total, forms the test signal. The length of the noise increases logarithmically, while the length of the silence decreases logarithmically for each of the 6 intervals, allowing a better correlation between the control signal and the measured signal.

The measurement file ```pulsedNoise.wav``` can be found in ```ressources```.

The script which was used to generate it ```TestFileGenerator``` can also be found in the same directory in case it is needed to be modified for certain apllications (Please let me know in that case)

## Use-cases / Application Examples <div id='use-cases' />

### Time align audio tracks (e.g. multi mic setup to avoid phase issues) <div id='time-align' />

Example:

A snare drum is recorded with 2 microphones. Both microphone recordings shall be time-aligned (phase-aligned).

1) Check that the phase is not inverted
2) Analyze both records with the script
3) Adjust the timing of one of the tracks inside your DAW.

### Time shift measurement to time align multi speaker setups <div id='multi_speaker' />

In this example we are using the Audio Time Shift Detector to time-align a multi speaker setup.

This can be useful in a setup where a delay for each individual speaker can be set (e.g. via DSP).

To measure the time delay between the speakers it is crucial to have a measurement reference.

The reference is an analog loopback. The measuremnt file is played to each speaker at a time. Both the measurement microphone signal (which is optimally placed at the listeners position) and the reference signal (loopback) are recorded at each run.

#### Example:

![alt text](img/Multi-Way.drawio.png "Title")

1) Tweeter:
    - Play the measurement file to the tweeter (Out Channel 1) and the loopback (Out Channel 4)
    - Record the analog loopback as well as the Microphone (In Channels 1 & 2)
    - Run the script on thos two files, note the time shift.

2) Mid Range
    - Play the measurement file to the midrange seaker (Out Channel 2) and the loopback (Out Channel 4).
    - Record the analog loopback as well as the Microphone (In Channels 1 & 2)
    - Run the script on thos two files, note the time shift.

3) Analyse
    - Calculate the difference between Tweeter and Midrange

## Testing

In the ```testing``` directory you can find the Reaper project I have used for testing & verification.

Track 1 contains the unchanged test file.
Track 2 & track 3 contain copies of that file but with apllied filters which mimic a frequency response change (e.g. to mimic a crossover of a speaker system). If the reaFIR filter's edit mode is set to ```precise``` it does not influence the phase.
You can play around with other EQs and filters to see that the resuklting phase shift creates an additional time shift.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
