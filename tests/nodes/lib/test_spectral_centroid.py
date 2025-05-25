import tempfile
import pytest
from pydub import AudioSegment
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.metadata.types import AudioRef, NPArray
from nodetool.nodes.lib.librosa.analysis import SpectralCentroid

_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
AudioSegment.silent(duration=5000, frame_rate=44100).export(_tmp.name, format="wav")
_tmp.close()
dummy_audio = AudioRef(uri=_tmp.name)


@pytest.fixture
def context():
    return ProcessingContext(user_id="test", auth_token="test")


@pytest.mark.asyncio
async def test_spectral_centroid_node(context: ProcessingContext):
    node = SpectralCentroid(audio=dummy_audio)
    result = await node.process(context)
    assert isinstance(result, NPArray)
    assert result.to_numpy().size > 0
