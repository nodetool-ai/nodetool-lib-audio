# Nodetool Audio Nodes

A comprehensive audio processing library for the [NodeTool](https://github.com/nodetool-ai/nodetool) platform, providing a wide range of audio manipulation, synthesis, effects, and analysis nodes. The package builds on top of [nodetool-core](https://github.com/nodetool-ai/nodetool-core), which supplies the runtime and base node implementation used throughout this repository.

## Overview

Nodetool Audio Nodes is a collection of audio processing components designed to work within the NodeTool visual development platform. This library enables users to create, manipulate, and transform audio content through an intuitive node-based interface without requiring extensive audio engineering knowledge.

## Installation

Use Nodetool's package manager to install this packages.

## Features

The library provides a rich set of audio processing capabilities organized into several categories:

### Audio Transformation

- **Basic Operations**: Concatenate, normalize, overlay, and slice audio files
- **Channel Manipulation**: Convert between mono and stereo
- **Time-Based Effects**: Reverse audio, apply fade-in/fade-out, repeat/loop audio
- **Silence Handling**: Remove or shorten silence with smooth transitions
- **Audio Mixing**: Mix multiple audio tracks with individual volume controls

### Audio Synthesis

- **Waveform Generation**: Create sine, square, sawtooth, and triangle waves
- **Noise Generation**: Generate white noise and pink noise
- **FM Synthesis**: Perform frequency modulation synthesis for complex timbres
- **Envelope Control**: Apply attack-decay-release envelopes to shape sounds

### Audio Effects (Pedalboard)

- **Dynamics Processing**: Compression, limiting, noise gate
- **Spatial Effects**: Reverb, delay
- **Frequency Manipulation**: EQ filters (low/high shelf, low/high pass, peak)
- **Modulation Effects**: Phaser
- **Distortion Effects**: Distortion, bitcrushing
- **Time/Pitch Manipulation**: Time stretching, pitch shifting
- **Volume Control**: Gain adjustment

## Usage

Nodetool Audio Nodes are designed to be used within the NodeTool visual development platform. Each node can be added to a workflow and connected to other nodes to create complex audio processing chains.

### Example: Creating a Basic Audio Processing Chain

In the NodeTool interface:

1. Add an audio source node (e.g., from a file or synthesis)
2. Connect it to processing nodes (e.g., EQ, compression)
3. Add effect nodes (e.g., reverb, delay)
4. Connect to an output node (e.g., save to file or playback)

Additional workflows can be found in the `examples` directory. The included
`Segment Audio.json` demonstrates how to detect onsets and split an audio file
into smaller clips automatically.

## Node Documentation

### Transformation Nodes

- **Concat**: Concatenates two audio files together
- **ConcatList**: Concatenates multiple audio files in sequence
- **Normalize**: Normalizes the volume of an audio file
- **OverlayAudio**: Overlays two audio files together
- **RemoveSilence**: Removes or shortens silence with smooth transitions
- **SliceAudio**: Extracts a section of an audio file
- **MonoToStereo**: Converts mono audio to stereo
- **StereoToMono**: Converts stereo audio to mono
- **Reverse**: Reverses an audio file
- **FadeIn**: Applies a fade-in effect to audio
- **FadeOut**: Applies a fade-out effect to audio
- **Repeat**: Loops an audio file a specified number of times
- **AudioMixer**: Mixes up to 5 audio tracks with individual volume controls

### Synthesis Nodes

- **Oscillator**: Generates basic waveforms (sine, square, sawtooth, triangle)
- **WhiteNoise**: Generates white noise
- **PinkNoise**: Generates pink noise (1/f noise)
- **FM_Synthesis**: Performs FM (Frequency Modulation) synthesis
- **Envelope**: Applies an ADR (Attack-Decay-Release) envelope to audio
- **Tone**: Generates a constant tone signal

### Effect Nodes (Pedalboard)

- **Reverb**: Adds spatial depth to recordings
- **Compress**: Applies dynamic range compression
- **TimeStretch**: Changes speed without altering pitch
- **PitchShift**: Shifts pitch without changing duration
- **NoiseGate**: Reduces background noise
- **LowShelfFilter**: Boosts or cuts low frequencies
- **HighShelfFilter**: Boosts or cuts high frequencies
- **HighPassFilter**: Attenuates frequencies below a cutoff point
- **LowPassFilter**: Attenuates frequencies above a cutoff point
- **PeakFilter**: Boosts or cuts a specific frequency range
- **Distortion**: Adds grit and character to audio
- **Phaser**: Creates sweeping, swooshing sounds
- **Delay**: Adds echo effects
- **Gain**: Adjusts volume
- **Limiter**: Prevents audio clipping
- **Bitcrush**: Creates lo-fi or retro-style audio effects

### Analysis Nodes

- **AmplitudeToDB**: Converts an amplitude spectrogram to decibels
- **ChromaSTFT**: Generates a chromagram to identify pitch classes
- **DBToAmplitude**: Converts a dB-scaled spectrogram back to amplitude
- **DBToPower**: Converts a dB-scaled spectrogram back to power scale
- **GriffinLim**: Reconstructs audio from a magnitude spectrogram
- **MelSpectrogram**: Computes the mel-frequency spectrogram
- **MFCC**: Calculates Mel-frequency cepstral coefficients
- **PlotSpectrogram**: Renders a spectrogram image
- **PowertToDB**: Converts a power spectrogram to decibels
- **SpectralContrast**: Measures spectral peaks and valleys
- **STFT**: Computes a short-time Fourier transform
- **SpectralCentroid**: Calculates the spectral centroid over time

### Segmentation Nodes

- **DetectOnsets**: Detects onset events in an audio signal
- **SegmentAudioByOnsets**: Splits audio using detected onset times
- **SaveAudioSegments**: Saves segments to a folder

## Dependencies

- **pydub**: Audio file manipulation
- **librosa**: Advanced audio processing
- **pedalboard**: High-quality audio effects
- **nodetool-core**: Core NodeTool functionality

## Testing

Run the unit tests with [pytest](https://docs.pytest.org/):

```bash
pytest -v
```

## Contributing

Contributions to Nodetool Audio Nodes are welcome! Please feel free to submit pull requests, create issues, or suggest new features.

## License

This project is licensed under the terms of the included LICENSE file.
