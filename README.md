# Audio Time Shift Detector

Analyse time shift between .wav files.
Returns time shift in sample points & milliseconds.

## Use-cases

- Time align Loudspeakers (e.g. Sub & Satellite)
- Time align audio tracks (e.g. multi mic setup to avoid phase issues)
- Anything else you can think of

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
