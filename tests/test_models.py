"""
Unit tests for video generation models.
"""
import pytest
from pydantic import ValidationError

from horde_video_sdk.models import (
    VideoGenerationParams,
    VideoGenerateAsyncRequest,
    VideoGenerateAsyncResponse,
    VideoGenerateStatusResponse,
    VideoGeneration,
    ImageToVideoRequest,
    VideoToVideoRequest,
)
from horde_video_sdk.video_config import (
    VideoResolution,
    VideoCodec,
    VideoFormat,
    VideoQuality,
)


class TestVideoGenerationParams:
    """Tests for VideoGenerationParams model."""

    def test_default_params(self):
        """Test default parameter values."""
        params = VideoGenerationParams()
        assert params.duration == 3.0
        assert params.fps == 24
        assert params.resolution == VideoResolution.HD_1024_576
        assert params.codec == VideoCodec.H264
        assert params.format == VideoFormat.MP4
        assert params.quality == VideoQuality.HIGH
        assert params.motion_scale == 1.0
        assert params.interpolation is True

    def test_frame_count_calculation(self):
        """Test automatic frame count calculation."""
        params = VideoGenerationParams(duration=2.0, fps=30)
        assert params.frame_count == 60

    def test_explicit_frame_count(self):
        """Test explicit frame count override."""
        params = VideoGenerationParams(duration=2.0, fps=30, frame_count=45)
        assert params.frame_count == 45

    def test_validation_errors(self):
        """Test parameter validation."""
        # Test duration limits
        with pytest.raises(ValidationError):
            VideoGenerationParams(duration=0.1)  # Too short
        
        with pytest.raises(ValidationError):
            VideoGenerationParams(duration=15.0)  # Too long
        
        # Test fps limits
        with pytest.raises(ValidationError):
            VideoGenerationParams(fps=5)  # Too low
        
        with pytest.raises(ValidationError):
            VideoGenerationParams(fps=120)  # Too high
        
        # Test motion scale limits
        with pytest.raises(ValidationError):
            VideoGenerationParams(motion_scale=-0.1)  # Negative
        
        with pytest.raises(ValidationError):
            VideoGenerationParams(motion_scale=3.0)  # Too high


class TestVideoGenerateAsyncRequest:
    """Tests for VideoGenerateAsyncRequest model."""

    def test_minimal_request(self):
        """Test minimal valid request."""
        request = VideoGenerateAsyncRequest(prompt="A simple test video")
        assert request.prompt == "A simple test video"
        assert request.model == "stable-video-diffusion-1.1"  # Default model
        assert request.nsfw is False
        assert request.shared is False

    def test_full_request(self):
        """Test request with all parameters."""
        params = VideoGenerationParams(duration=5.0, fps=30)
        request = VideoGenerateAsyncRequest(
            prompt="A detailed test video",
            negative_prompt="blurry, low quality",
            model="animatediff-v3",
            params=params,
            nsfw=True,
            shared=True,
            seed=12345,
            workers=["worker1", "worker2"],
            api_key="test_key",
        )
        
        assert request.prompt == "A detailed test video"
        assert request.negative_prompt == "blurry, low quality"
        assert request.model == "animatediff-v3"
        assert request.params.duration == 5.0
        assert request.params.fps == 30
        assert request.nsfw is True
        assert request.shared is True
        assert request.seed == 12345
        assert request.workers == ["worker1", "worker2"]
        assert request.api_key == "test_key"

    def test_prompt_validation(self):
        """Test prompt validation."""
        # Empty prompt should fail
        with pytest.raises(ValidationError):
            VideoGenerateAsyncRequest(prompt="")
        
        # Too long prompt should fail
        with pytest.raises(ValidationError):
            VideoGenerateAsyncRequest(prompt="x" * 1001)

    def test_model_validation(self):
        """Test model validation."""
        # Unsupported model should fail
        with pytest.raises(ValidationError):
            VideoGenerateAsyncRequest(prompt="test", model="unsupported-model")


class TestVideoGenerateAsyncResponse:
    """Tests for VideoGenerateAsyncResponse model."""

    def test_basic_response(self):
        """Test basic response creation."""
        response = VideoGenerateAsyncResponse(
            id="test-job-123",
            kudos=50.0,
            message="Request accepted",
        )
        
        assert response.id == "test-job-123"
        assert response.kudos == 50.0
        assert response.message == "Request accepted"
        assert response.warnings is None


class TestVideoGenerateStatusResponse:
    """Tests for VideoGenerateStatusResponse model."""

    def test_pending_status(self):
        """Test pending generation status."""
        status = VideoGenerateStatusResponse(
            id="test-job-123",
            done=False,
            queue_position=5,
            wait_time=120,
        )
        
        assert status.id == "test-job-123"
        assert status.done is False
        assert status.queue_position == 5
        assert status.wait_time == 120
        assert len(status.generations) == 0

    def test_completed_status(self):
        """Test completed generation status."""
        generation = VideoGeneration(
            id="gen-123",
            video_url="https://example.com/video.mp4",
            worker_name="test-worker",
            model="stable-video-diffusion-1.1",
            duration=3.0,
            fps=24,
            resolution="1024x576",
        )
        
        status = VideoGenerateStatusResponse(
            id="test-job-123",
            done=True,
            finished=1,
            generations=[generation],
        )
        
        assert status.done is True
        assert status.finished == 1
        assert len(status.generations) == 1
        assert status.generations[0].video_url == "https://example.com/video.mp4"


class TestImageToVideoRequest:
    """Tests for ImageToVideoRequest model."""

    def test_basic_request(self):
        """Test basic image-to-video request."""
        request = ImageToVideoRequest(
            source_image="base64_encoded_image_data",
            prompt="animate this image gently",
        )
        
        assert request.source_image == "base64_encoded_image_data"
        assert request.prompt == "animate this image gently"
        assert request.model == "stable-video-diffusion-1.1"
        assert request.motion_scale == 1.0


class TestVideoToVideoRequest:
    """Tests for VideoToVideoRequest model."""

    def test_basic_request(self):
        """Test basic video-to-video request."""
        request = VideoToVideoRequest(
            source_video="base64_encoded_video_data",
            prompt="transform this video into a cartoon style",
        )
        
        assert request.source_video == "base64_encoded_video_data"
        assert request.prompt == "transform this video into a cartoon style"
        assert request.model == "stable-video-diffusion-1.1"
        assert request.strength == 0.8

    def test_strength_validation(self):
        """Test strength parameter validation."""
        # Too low strength should fail
        with pytest.raises(ValidationError):
            VideoToVideoRequest(
                source_video="test",
                prompt="test",
                strength=0.05,
            )
        
        # Too high strength should fail
        with pytest.raises(ValidationError):
            VideoToVideoRequest(
                source_video="test",
                prompt="test",
                strength=1.5,
            )


if __name__ == "__main__":
    pytest.main([__file__])
