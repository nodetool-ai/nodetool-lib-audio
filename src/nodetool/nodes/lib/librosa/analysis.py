import librosa
import numpy as np
from pydantic import Field
from nodetool.metadata.types import AudioRef, NPArray
from nodetool.workflows.base_node import BaseNode
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.common.audio_helpers import (
    convert_to_float,
)
from nodetool.metadata.types import ImageRef
from typing import Any, Optional


class AmplitudeToDB(BaseNode):
    """
    Converts an amplitude spectrogram to a dB-scaled spectrogram.
    audio, analysis, spectrogram

    This node is useful for:
    - Compressing the dynamic range of spectrograms for visualization
    - Preparing input for audio models that expect dB-scaled data
    """

    tensor: NPArray = Field(
        default=NPArray(),
        description="The amplitude tensor to be converted to dB scale.",
    )

    async def process(self, context: ProcessingContext) -> NPArray:
        db_tensor = librosa.amplitude_to_db(self.tensor.to_numpy(), ref=np.max)
        return NPArray.from_numpy(db_tensor)


class ChromaSTFT(BaseNode):
    """
    This node creates a chromagram from a waveform or power spectrogram to identify different pitch classes in an audio signal.
    audio, analysis, chromagram, pitch

    Applications:
    - Chord recognition in music
    - Music genre classification based on pitch content
    """

    audio: AudioRef = Field(
        default=AudioRef(), description="The audio file to extract chromagram from."
    )
    n_fft: int = Field(
        default=2048, ge=0, description="The number of samples per frame."
    )
    hop_length: int = Field(
        default=512, ge=0, description="The number of samples between frames."
    )

    async def process(self, context: ProcessingContext) -> NPArray:
        samples, sample_rate, num_channels = await context.audio_to_numpy(self.audio)
        samples = convert_to_float(samples)
        chromagram = librosa.feature.chroma_stft(
            y=samples, sr=sample_rate, n_fft=self.n_fft, hop_length=self.hop_length
        )
        return NPArray.from_numpy(chromagram)


class DBToAmplitude(BaseNode):
    """
    The DBToAmplitude node Converts a dB-scaled spectrogram to an amplitude spectrogram.
    audio, analysis, spectrogram
    Useful for:
    - Reversing dB scaling before audio synthesis
    - Preparing data for models that expect linear amplitude scaling
    """

    tensor: NPArray = Field(
        default=NPArray(),
        description="The dB-scaled tensor to be converted to amplitude scale.",
    )

    async def process(self, context: ProcessingContext) -> NPArray:
        amplitude_tensor = librosa.db_to_amplitude(self.tensor.to_numpy())
        return NPArray.from_numpy(amplitude_tensor)


class DBToPower(BaseNode):
    """
    This node converts a decibel (dB) spectrogram back to power scale.
    audio, analysis, spectrogram

    Useful for:
    - Reversing dB scaling for audio synthesis
    - Preparing data for models that expect power-scaled data
    """

    tensor: NPArray = Field(
        default=NPArray(), description="The tensor containing the decibel spectrogram."
    )

    async def process(self, context: ProcessingContext) -> NPArray:
        db_spec = self.tensor.to_numpy()
        return NPArray.from_numpy(librosa.db_to_power(db_spec))


class GriffinLim(BaseNode):
    """
    GriffinLim Node performs phase reconstruction on a magnitude spectrogram utilizing the Griffin-Lim algorithm.
    audio, synthesis, phase reconstruction

    Applications:
    - Audio synthesis from spectrograms
    - Phase reconstruction in audio processing pipelines
    """

    magnitude_spectrogram: NPArray = Field(
        default=NPArray(),
        description="Magnitude spectrogram input for phase reconstruction.",
    )
    n_iter: int = Field(
        default=32, description="Number of iterations for the Griffin-Lim algorithm."
    )
    hop_length: int = Field(
        default=512, description="Number of samples between successive frames."
    )
    win_length: Optional[int] = Field(
        default=None,
        description="Each frame of audio is windowed by `window()`. The window will be of length `win_length` and then padded with zeros to match `n_fft`.",
    )
    window: str = Field(
        default="hann",
        description="Type of window to use for Griffin-Lim transformation.",
    )
    center: bool = Field(
        default=True,
        description="If True, the signal `y` is padded so that frame `D[:, t]` is centered at `y[t * hop_length]`.",
    )
    length: Optional[int] = Field(
        default=None,
        description="If given, the resulting signal will be zero-padded or clipped to this length.",
    )

    async def process(self, context: ProcessingContext) -> NPArray:
        reconstructed_audio = librosa.griffinlim(
            S=self.magnitude_spectrogram.to_numpy(),
            n_iter=self.n_iter,
            hop_length=self.hop_length,
            win_length=self.win_length,
            window=self.window,
            center=self.center,
            length=self.length,
        )
        return NPArray.from_numpy(reconstructed_audio)


class MelSpectrogram(BaseNode):
    """
    MelSpecNode computes the Mel-frequency spectrogram for an audio signal.
    audio, analysis, spectrogram

    Useful for:
    - Audio feature extraction for machine learning
    - Speech and music analysis tasks
    """

    audio: AudioRef = Field(
        default=AudioRef(), description="The audio file to convert to a tensor."
    )
    n_fft: int = Field(
        default=2048, ge=0, description="The number of samples per frame."
    )
    hop_length: int = Field(
        default=512, ge=0, description="The number of samples between frames."
    )
    n_mels: int = Field(
        default=128, ge=0, description="The number of Mel bands to generate."
    )
    fmin: int = Field(default=0, ge=0, description="The lowest frequency (in Hz).")
    fmax: int = Field(default=8000, ge=0, description="The highest frequency (in Hz).")

    async def process(self, context: ProcessingContext) -> NPArray:
        samples, sample_rate, num_channels = await context.audio_to_numpy(self.audio)
        samples = convert_to_float(samples)
        melspectrogram = librosa.feature.melspectrogram(
            y=samples,
            sr=sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels,
            fmin=self.fmin,
            fmax=self.fmax,
        )
        return NPArray.from_numpy(melspectrogram)

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        return ["audio", "n_mels", "fmax"]


class MFCC(BaseNode):
    """
    MFCC Node computes the Mel-frequency cepstral coefficients (MFCCs) from an audio signal.
    audio, analysis, frequency, MFCC, MEL
    """

    audio: AudioRef = Field(
        default=AudioRef(), description="The audio file to extract MFCCs from."
    )
    n_mfcc: int = Field(default=13, ge=0, description="The number of MFCCs to extract.")
    n_fft: int = Field(
        default=2048, ge=0, description="The number of samples per frame."
    )
    hop_length: int = Field(
        default=512, ge=0, description="The number of samples between frames."
    )
    fmin: int = Field(default=0, ge=0, description="The lowest frequency (in Hz).")
    fmax: int = Field(default=8000, ge=0, description="The highest frequency (in Hz).")

    async def process(self, context: ProcessingContext) -> NPArray:
        samples, sample_rate, num_channels = await context.audio_to_numpy(self.audio)
        samples = convert_to_float(samples)
        mfccs = librosa.feature.mfcc(
            y=samples,
            sr=sample_rate,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            fmin=self.fmin,
            fmax=self.fmax,
        )
        return NPArray.from_numpy(mfccs)

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        return ["audio", "n_mfcc", "n_fft"]


class PlotSpectrogram(BaseNode):
    """
    The PlotSpectrogram node generates a visual representation of the spectrum of frequencies in an audio signal as they vary with time.
    audio, analysis, frequency, spectrogram

    #### Applications
    - Audio Analysis: Allows users to visually see the spectrum of frequencies in their data.
    - Machine Learning: Used as a preprocessing step for feeding data into image-based ML models.
    - Sound engineering: Helps in identifying specific tones or frequencies in a music piece or a sound bite.
    """

    tensor: NPArray = Field(
        default=NPArray(), description="The tensor containing the mel spectrogram."
    )
    fmax: int = Field(default=8000, ge=0, description="The highest frequency (in Hz).")

    async def process(self, context: ProcessingContext) -> ImageRef:
        import io
        from PIL import Image

        # Get the spectrogram data
        spec = self.tensor.to_numpy()

        # Normalize the spectrogram data to 0-255 range for image
        spec_normalized = spec - np.min(spec)
        if np.max(spec_normalized) > 0:
            spec_normalized = spec_normalized / np.max(spec_normalized) * 255

        # Convert to uint8 for image creation
        spec_img = spec_normalized.astype(np.uint8)

        # Create an image from the array
        # Transpose to get frequency on y-axis and time on x-axis
        img = Image.fromarray(spec_img).transpose(Image.Transpose.TRANSPOSE)

        # Save to bytes buffer
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        return await context.image_from_bytes(buf.getvalue())

    def result_for_client(self, result: dict[str, Any]) -> dict[str, Any]:
        return self.result_for_all_outputs(result)


class PowertToDB(BaseNode):
    """
    Converts a power spectrogram to decibel (dB) scale.
    audio, analysis, decibel, spectrogram
    """

    tensor: NPArray = Field(
        default=NPArray(), description="The tensor containing the power spectrogram."
    )

    async def process(self, context: ProcessingContext) -> NPArray:
        power_spec = self.tensor.to_numpy()
        return NPArray.from_numpy(librosa.power_to_db(power_spec, ref=np.max))


class SpectralContrast(BaseNode):
    """
    The spectral contrast measures the difference in amplitude between the most noticeable parts (peaks) and the less noticeable parts (valleys) in a sound spectrum.
    audio, analysis, decibel, amplitude

    #### Applications
    - Music genre classification: distinguishing between different types of music based on the color of sound.
    - Instrument recognition: recognizing different musical instruments by the difference in their spectral contrast.
    - Audio analysis: determining various characteristics of audio files.

    Useful note: The `n_fft` and `hop_length` parameters affect the resolution of the analysis. A higher `n_fft` provides better frequency resolution but worse time resolution, and vice versa for a lower `hop_length`.
    """

    audio: AudioRef = Field(
        default=AudioRef(),
        description="The audio file to extract spectral contrast from.",
    )
    n_fft: int = Field(
        default=2048, ge=0, description="The number of samples per frame."
    )
    hop_length: int = Field(
        default=512, ge=0, description="The number of samples between frames."
    )

    async def process(self, context: ProcessingContext) -> NPArray:
        samples, sample_rate, num_channels = await context.audio_to_numpy(self.audio)
        samples = convert_to_float(samples)
        spectral_contrast = librosa.feature.spectral_contrast(
            y=samples, sr=sample_rate, n_fft=self.n_fft, hop_length=self.hop_length
        )
        return NPArray.from_numpy(spectral_contrast)


class STFT(BaseNode):
    """
    This node computes the Short-Time Fourier Transform (STFT) matrix for an audio signal. The STFT matrix represents the signal in both time and frequency domains, forming the foundation for many audio processing tasks.
    audio, analysis, fourier, frequency, time
    #### Applications
    - Audio Analysis: By transforming the audio signal into a visualizable format, it helps in understanding and analyzing the audio signal.
    - Sound Processing: It plays a key foundational role in sound effects, tuning, compression, and more.
    - Audio Feature Extraction: It can be used to analyze frequency-based features for sound classification.
    - Music Information Retrieval: It helps in music transcription, rhythm and tempo analysis.
    """

    audio: AudioRef = Field(
        default=AudioRef(),
        description="The audio file to compute the STFT matrix from.",
    )
    n_fft: int = Field(
        default=2048, ge=0, description="The number of samples per frame."
    )
    hop_length: int = Field(
        default=512, ge=0, description="The number of samples between frames."
    )
    win_length: Optional[int] = Field(
        default=None, description="The window length. If None, it defaults to n_fft."
    )
    window: str = Field(default="hann", description="The type of window to use.")
    center: bool = Field(
        default=True,
        description="If True, input signal is padded so that frame D[:, t] is centered at y[t * hop_length].",
    )

    async def process(self, context: ProcessingContext) -> NPArray:
        samples, sample_rate, num_channels = await context.audio_to_numpy(self.audio)
        samples = convert_to_float(samples)
        stft_matrix = librosa.stft(
            y=samples,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            win_length=self.win_length,
            window=self.window,
            center=self.center,
        )
        return NPArray.from_numpy(np.abs(stft_matrix))

    @classmethod
    def get_basic_fields(cls) -> list[str]:
        return ["audio", "n_fft", "hop_length"]


class SpectralCentroid(BaseNode):
    """
    Computes the spectral centroid of an audio file.
    audio, analysis, spectral

    The spectral centroid indicates where the "center of mass" of the spectrum is located.
    Perceptually, it has a connection with the impression of "brightness" of a sound.

    Use cases:
    - Analyze the timbral characteristics of audio
    - Track changes in sound brightness over time
    - Feature extraction for music genre classification
    - Audio effect design and sound manipulation
    """

    audio: AudioRef = Field(
        default=AudioRef(), description="The audio file to analyze."
    )
    n_fft: int = Field(
        default=2048, ge=128, le=8192, description="The length of the FFT window."
    )
    hop_length: int = Field(
        default=512,
        ge=64,
        le=2048,
        description="Number of samples between successive frames.",
    )

    async def process(self, context: ProcessingContext) -> NPArray:
        import librosa

        # Load the audio file
        samples, sample_rate, _ = await context.audio_to_numpy(self.audio)

        # Compute the spectral centroid
        centroids = librosa.feature.spectral_centroid(
            y=samples, sr=sample_rate, n_fft=self.n_fft, hop_length=self.hop_length
        )

        # Convert to Hz and flatten
        centroids_hz = centroids[0]

        return NPArray.from_numpy(centroids_hz)
