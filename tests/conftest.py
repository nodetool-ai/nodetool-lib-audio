import pytest
from io import BytesIO
from pydub import AudioSegment
from nodetool.workflows.processing_context import ProcessingContext


@pytest.fixture(autouse=True)
def patch_audio_loader(monkeypatch):
    async def audio_to_audio_segment(self, audio_ref):
        audio_bytes = await self.asset_to_io(audio_ref)
        if hasattr(audio_bytes, "seek"):
            audio_bytes.seek(0)
        return AudioSegment.from_file(audio_bytes, format="wav")

    monkeypatch.setattr(
        ProcessingContext,
        "audio_to_audio_segment",
        audio_to_audio_segment,
        raising=False,
    )

    async def audio_from_segment(
        self, audio_segment, name=None, parent_id=None, **kwargs
    ):
        buffer = BytesIO()
        audio_segment.export(buffer, format="wav")
        buffer.seek(0)
        return await self.audio_from_io(buffer, name=name, parent_id=parent_id)

    monkeypatch.setattr(
        ProcessingContext,
        "audio_from_segment",
        audio_from_segment,
        raising=False,
    )
    yield
