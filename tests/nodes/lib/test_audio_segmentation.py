import pytest
import numpy as np
import tempfile
from pydub import AudioSegment
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.metadata.types import AudioRef, NPArray
from nodetool.nodes.lib.librosa.segmentation import (
    DetectOnsets,
    SegmentAudioByOnsets,
)

# Create a dummy AudioRef for testing
tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
AudioSegment.silent(duration=5000, frame_rate=44100).export(tmp.name, format="wav")
tmp.close()
dummy_audio = AudioRef(uri=tmp.name)

# Create a dummy Tensor for onsets
dummy_onsets = NPArray.from_numpy(np.array([0.5, 1.0, 1.5, 2.0]))


@pytest.fixture
def context():
    return ProcessingContext(user_id="test", auth_token="test")


@pytest.mark.asyncio
async def test_detect_onsets(context: ProcessingContext):
    node = DetectOnsets(audio=dummy_audio)
    result = await node.process(context)

    assert isinstance(result, NPArray)


@pytest.mark.asyncio
async def test_segment_audio_by_onsets(context: ProcessingContext):
    node = SegmentAudioByOnsets(audio=dummy_audio, onsets=dummy_onsets)
    result = await node.process(context)

    assert isinstance(result, list)
    assert all(isinstance(segment, AudioRef) for segment in result)
    assert len(result) > 0
