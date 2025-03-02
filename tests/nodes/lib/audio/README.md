# Audio Node Tests

This directory contains tests for the audio transformation nodes in the `nodetool.nodes.lib.audio.transform` module.

## Running the Tests

To run the tests, use the following command from the project root:

```bash
pytest tests/nodes/lib/audio/test_transform.py -v
```

## Test Coverage

The tests cover the following audio transformation nodes:

1. `Concat` - Concatenates two audio files
2. `ConcatList` - Concatenates multiple audio files in sequence
3. `Normalize` - Normalizes the volume of an audio file
4. `OverlayAudio` - Overlays two audio files together
5. `RemoveSilence` - Removes or shortens silence in an audio file
6. `SliceAudio` - Extracts a section of an audio file
7. `Tone` - Generates a constant tone signal
8. `MonoToStereo` - Converts a mono audio signal to stereo
9. `StereoToMono` - Converts a stereo audio signal to mono
10. `Reverse` - Reverses an audio file
11. `FadeIn` - Applies a fade-in effect to an audio file
12. `FadeOut` - Applies a fade-out effect to an audio file
13. `Repeat` - Loops an audio file a specified number of times
14. `AudioMixer` - Mixes up to 5 audio tracks with individual volume controls

## Test Approach

The tests use mocking to simulate the behavior of the audio processing functions without requiring actual audio files. This approach allows for fast and reliable testing of the node logic without dependencies on external resources.

Key mocking strategies used:

- Mock `ProcessingContext` to simulate audio conversion
- Mock audio segment operations like `overlay`, `set_channels`, etc.
- Mock helper functions from `audio_helpers.py`
- Track stereo vs mono audio references using a dictionary

## Adding New Tests

When adding new audio transformation nodes, follow the existing pattern:

1. Create a new test class for the node
2. Test the main functionality
3. Test edge cases and error conditions
4. Use appropriate mocking to simulate audio operations
