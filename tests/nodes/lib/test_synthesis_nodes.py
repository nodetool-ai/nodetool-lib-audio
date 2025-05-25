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
