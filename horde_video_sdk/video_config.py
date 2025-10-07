"""
Video-specific configuration constants and defaults.
"""
from enum import Enum

class VideoResolution(str, Enum):
    """Supported video resolutions."""
    SD_512 = "512x512"
    SD_WIDE = "512x288"
    HD_720 = "1280x720"
    HD_1024_576 = "1024x576"
    HD_1024_1024 = "1024x1024"

class VideoCodec(str, Enum):
    """Supported video codecs."""
    H264 = "h264"
    H265 = "h265"
    VP9 = "vp9"
    AV1 = "av1"

class VideoFormat(str, Enum):
    """Supported video output formats."""
    MP4 = "mp4"
    WEBM = "webm"
    GIF = "gif"
    MOV = "mov"

class VideoFPS(int, Enum):
    """Common frame rates."""
    FPS_8 = 8
    FPS_12 = 12
    FPS_16 = 16
    FPS_24 = 24
    FPS_30 = 30
    FPS_60 = 60

class VideoQuality(str, Enum):
    """Video quality presets."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    LOSSLESS = "lossless"

# Default video generation parameters
DEFAULT_VIDEO_PARAMS = {
    "duration": 3.0,
    "fps": 24,
    "resolution": VideoResolution.HD_1024_576,
    "codec": VideoCodec.H264,
    "format": VideoFormat.MP4,
    "quality": VideoQuality.HIGH,
    "motion_scale": 1.0,
    "interpolation": True,
}

# Video model definitions
SUPPORTED_VIDEO_MODELS = [
    "stable-video-diffusion-1.1",
    "animatediff-v3",
    "cogvideox-5b",
    "zeroscope-v2-xl",
    "modelscope-text2video",
]

# Processing limits
MAX_VIDEO_DURATION = 10.0
MAX_VIDEO_SIZE_MB = 500
MAX_CONCURRENT_GENERATIONS = 3
DEFAULT_TIMEOUT = 900

# Temporary file settings
TEMP_FILE_PREFIX = "horde_video_"
TEMP_FILE_CLEANUP_DELAY = 3600

# API endpoints
VIDEO_API_BASE = "https://aihorde.net/api"
VIDEO_ENDPOINTS = {
    "generate_async": "/v2/generate/video/async",
    "generate_check": "/v2/generate/video/check/{id}",
    "generate_status": "/v2/generate/video/status/{id}",
    "generate_cancel": "/v2/generate/video/status/{id}",
    "models": "/v2/status/video/models",
}