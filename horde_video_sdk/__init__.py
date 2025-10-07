"""
horde-video-sdk: A Python library for AI-Horde video generation APIs.
"""

__version__ = "0.1.0"
__author__ = "SuperMalinge"
__license__ = "AGPL-3.0"

from horde_video_sdk.client import VideoHordeAPIClient, VideoHordeAPIError
from horde_video_sdk.models import (
    VideoGenerateAsyncRequest,
    VideoGenerateAsyncResponse,
    VideoGenerateStatusRequest,
    VideoGenerateStatusResponse,
    ImageToVideoRequest,
    VideoToVideoRequest,
    VideoGenerationParams,
    VideoGeneration,
    VideoModelsResponse,
    VideoStatsResponse,
)
from horde_video_sdk.video_config import (
    VideoResolution,
    VideoCodec,
    VideoFormat,
    VideoFPS,
    VideoQuality,
    SUPPORTED_VIDEO_MODELS,
    DEFAULT_VIDEO_PARAMS,
)

__all__ = [
    "VideoHordeAPIClient",
    "VideoHordeAPIError",
    "VideoGenerateAsyncRequest",
    "VideoGenerateAsyncResponse",
    "VideoGenerateStatusRequest",
    "VideoGenerateStatusResponse",
    "ImageToVideoRequest",
    "VideoToVideoRequest",
    "VideoGenerationParams",
    "VideoGeneration",
    "VideoModelsResponse",
    "VideoStatsResponse",
    "VideoResolution",
    "VideoCodec",
    "VideoFormat",
    "VideoFPS",
    "VideoQuality",
    "SUPPORTED_VIDEO_MODELS",
    "DEFAULT_VIDEO_PARAMS",
]