import pytest
import tempfile
from pydub import AudioSegment
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.metadata.types import AudioRef, FolderRef
from nodetool.nodes.lib.librosa.segmentation import SaveAudioSegments
from nodetool.nodes.lib.synthesis import Oscillator, PitchEnvelopeCurve

# Create a dummy AudioRef for testing
tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
AudioSegment.silent(duration=5000, frame_rate=44100).export(tmp.name, format="wav")
tmp.close()
dummy_audio = AudioRef(uri=tmp.name)


@pytest.fixture
def context():
    return ProcessingContext(user_id="test", auth_token="test")


@pytest.mark.asyncio
async def test_save_audio_segments_node_creation():
    """Test the SaveAudioSegments node instantiation and basic validation."""
    # Create some test audio segments
    segments = [dummy_audio, dummy_audio, dummy_audio]

    # Create a test folder reference
    test_folder = FolderRef()

    node = SaveAudioSegments(
        segments=segments, output_folder=test_folder, name_prefix="test_segment"
    )

    # Verify node is created with correct parameters
    assert node.segments == segments
    assert node.output_folder.asset_id == test_folder.asset_id
    assert node.name_prefix == "test_segment"


@pytest.mark.asyncio
async def test_save_audio_segments_empty_list():
    """Test SaveAudioSegments with an empty segment list."""
    test_folder = FolderRef()

    node = SaveAudioSegments(
        segments=[], output_folder=test_folder, name_prefix="empty"
    )

    # Verify node is created with correct parameters
    assert node.segments == []
    assert node.output_folder.asset_id == test_folder.asset_id
    assert node.name_prefix == "empty"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pitch_curve,pitch_amount",
    [
        (PitchEnvelopeCurve.LINEAR, 0.0),
        (PitchEnvelopeCurve.LINEAR, 12.0),
        (PitchEnvelopeCurve.LINEAR, -12.0),
        (PitchEnvelopeCurve.EXPONENTIAL, 0.0),
        (PitchEnvelopeCurve.EXPONENTIAL, 12.0),
        (PitchEnvelopeCurve.EXPONENTIAL, -12.0),
    ],
)
async def test_oscillator_pitch_envelope_curves(
    context: ProcessingContext, pitch_curve, pitch_amount
):
    """Test Oscillator node with different pitch envelope curves and amounts."""
    node = Oscillator(
        duration=0.1,
        pitch_envelope_curve=pitch_curve,
        pitch_envelope_amount=pitch_amount,
        pitch_envelope_time=0.05,
    )

    result = await node.process(context)

    assert isinstance(result, AudioRef)
    assert result.data is not None
    assert len(result.data) > 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "waveform,pitch_curve",
    [
        (Oscillator.OscillatorWaveform.SINE, PitchEnvelopeCurve.LINEAR),
        (Oscillator.OscillatorWaveform.SQUARE, PitchEnvelopeCurve.LINEAR),
        (Oscillator.OscillatorWaveform.SAWTOOTH, PitchEnvelopeCurve.EXPONENTIAL),
        (Oscillator.OscillatorWaveform.TRIANGLE, PitchEnvelopeCurve.EXPONENTIAL),
    ],
)
async def test_oscillator_waveforms_with_pitch_envelope(
    context: ProcessingContext, waveform, pitch_curve
):
    """Test different waveforms with pitch envelope modulation."""
    node = Oscillator(
        duration=0.1,
        waveform=waveform,
        pitch_envelope_curve=pitch_curve,
        pitch_envelope_amount=6.0,  # Half octave up
        pitch_envelope_time=0.08,
    )

    result = await node.process(context)

    assert isinstance(result, AudioRef)
    assert result.data is not None
    assert len(result.data) > 0
