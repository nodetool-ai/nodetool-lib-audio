import pytest
import tempfile
from pydub import AudioSegment
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.metadata.types import AudioRef
from nodetool.nodes.lib.synthesis import (
    Oscillator,
    WhiteNoise,
    PinkNoise,
    FM_Synthesis,
    Envelope,
    PitchEnvelopeCurve,
)

# Create a dummy AudioRef for Envelope tests
_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
AudioSegment.silent(duration=5000, frame_rate=44100).export(_tmp.name, format="wav")
_tmp.close()
dummy_audio = AudioRef(uri=_tmp.name)


@pytest.fixture
def context():
    return ProcessingContext(user_id="test", auth_token="test")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "node",
    [
        Oscillator(duration=0.1),
        WhiteNoise(duration=0.1),
        PinkNoise(duration=0.1),
        FM_Synthesis(duration=0.1),
        Envelope(audio=dummy_audio, attack=0.01, decay=0.01, release=0.01),
    ],
)
async def test_synthesis_nodes(context: ProcessingContext, node):
    result = await node.process(context)
    assert isinstance(result, AudioRef)
    assert result.data is not None
    assert len(result.data) > 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "waveform",
    [
        Oscillator.OscillatorWaveform.SINE,
        Oscillator.OscillatorWaveform.SQUARE,
        Oscillator.OscillatorWaveform.SAWTOOTH,
        Oscillator.OscillatorWaveform.TRIANGLE,
    ],
)
async def test_oscillator_waveforms_with_envelope(context: ProcessingContext, waveform):
    node = Oscillator(
        waveform=waveform,
        duration=0.1,
        pitch_envelope_amount=12.0,
        pitch_envelope_time=0.05,
        pitch_envelope_curve=PitchEnvelopeCurve.EXPONENTIAL,
    )
    result = await node.process(context)
    assert isinstance(result, AudioRef)
    assert result.data is not None and len(result.data) > 0


@pytest.mark.asyncio
async def test_envelope_scaling_on_stereo(context: ProcessingContext):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    AudioSegment.silent(duration=100, frame_rate=44100).set_channels(2).export(
        tmp.name, format="wav"
    )
    tmp.close()
    stereo_audio = AudioRef(uri=tmp.name)
    node = Envelope(audio=stereo_audio, attack=0.2, decay=0.2, release=0.2)
    result = await node.process(context)
    assert isinstance(result, AudioRef)
    in_samples, _, _ = await context.audio_to_numpy(stereo_audio)
    out_samples, _, _ = await context.audio_to_numpy(result)
    assert len(out_samples) == len(in_samples)
    assert result.data is not None and len(result.data) > 0
