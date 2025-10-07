"""
Pydantic models for video generation requests and responses.
"""
from __future__ import annotations

from typing import Optional, List, Union
from enum import Enum
from pydantic import BaseModel, Field, validator

from horde_video_sdk.video_config import (
    VideoResolution,
    VideoCodec,
    VideoFormat,
    VideoFPS,
    VideoQuality,
    DEFAULT_VIDEO_PARAMS,
    MAX_VIDEO_DURATION,
    SUPPORTED_VIDEO_MODELS,
)


class VideoGenerationParams(BaseModel):
    """Parameters for video generation."""
    
    duration: float = Field(
        default=DEFAULT_VIDEO_PARAMS["duration"],
        ge=0.5,
        le=MAX_VIDEO_DURATION,
        description="Duration of the video in seconds"
    )
    fps: int = Field(
        default=DEFAULT_VIDEO_PARAMS["fps"],
        ge=8,
        le=60,
        description="Frames per second"
    )
    resolution: VideoResolution = Field(
        default=DEFAULT_VIDEO_PARAMS["resolution"],
        description="Video resolution"
    )
    codec: VideoCodec = Field(
        default=DEFAULT_VIDEO_PARAMS["codec"],
        description="Video codec"
    )
    format: VideoFormat = Field(
        default=DEFAULT_VIDEO_PARAMS["format"],
        description="Video output format"
    )
    quality: VideoQuality = Field(
        default=DEFAULT_VIDEO_PARAMS["quality"],
        description="Video quality preset"
    )
    motion_scale: float = Field(
        default=DEFAULT_VIDEO_PARAMS["motion_scale"],
        ge=0.0,
        le=2.0,
        description="Controls the amount of motion in the video"
    )
    interpolation: bool = Field(
        default=DEFAULT_VIDEO_PARAMS["interpolation"],
        description="Enable frame interpolation for smoother motion"
    )
    frame_count: Optional[int] = Field(
        default=None,
        ge=8,
        le=300,
        description="Explicit frame count (calculated from duration and fps if not provided)"
    )
    
    @validator('frame_count', always=True)
    def calculate_frame_count(cls, v, values):
        """Calculate frame count from duration and fps if not provided."""
        if v is None:
            duration = values.get('duration', DEFAULT_VIDEO_PARAMS["duration"])
            fps = values.get('fps', DEFAULT_VIDEO_PARAMS["fps"])
            return int(duration * fps)
        return v


class VideoGenerateAsyncRequest(BaseModel):
    """Request model for asynchronous video generation."""
    
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Text prompt for video generation"
    )
    negative_prompt: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Negative prompt to guide what not to include"
    )
    model: str = Field(
        default=SUPPORTED_VIDEO_MODELS[0],
        description="Video generation model to use"
    )
    params: Optional[VideoGenerationParams] = Field(
        default_factory=VideoGenerationParams,
        description="Video generation parameters"
    )
    nsfw: bool = Field(
        default=False,
        description="Whether the content is NSFW"
    )
    shared: bool = Field(
        default=False,
        description="Whether to share the video for improving datasets"
    )
    seed: Optional[int] = Field(
        default=None,
        description="Random seed for reproducible generation"
    )
    workers: Optional[List[str]] = Field(
        default=None,
        description="Specific workers to use for generation"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API key for authenticated requests"
    )
    
    @validator('model')
    def validate_model(cls, v):
        """Validate that the model is supported."""
        if v not in SUPPORTED_VIDEO_MODELS:
            raise ValueError(f"Model {v} not supported. Supported models: {SUPPORTED_VIDEO_MODELS}")
        return v


class VideoGeneration(BaseModel):
    """Represents a single generated video."""
    
    id: str = Field(..., description="Unique ID for this video generation")
    video_url: Optional[str] = Field(default=None, description="URL to download the generated video")
    video_base64: Optional[str] = Field(default=None, description="Base64 encoded video data")
    worker_id: Optional[str] = Field(default=None, description="ID of the worker that generated this video")
    worker_name: Optional[str] = Field(default=None, description="Name of the worker that generated this video")
    model: Optional[str] = Field(default=None, description="Model used for generation")
    seed: Optional[int] = Field(default=None, description="Seed used for generation")
    censored: bool = Field(default=False, description="Whether the video was censored")
    duration: Optional[float] = Field(default=None, description="Actual duration of the generated video")
    fps: Optional[int] = Field(default=None, description="Actual fps of the generated video")
    resolution: Optional[str] = Field(default=None, description="Actual resolution of the generated video")


class VideoGenerateAsyncResponse(BaseModel):
    """Response model for asynchronous video generation request."""
    
    id: str = Field(..., description="Unique ID for tracking this generation request")
    kudos: float = Field(default=0.0, description="Kudos cost for this generation")
    message: Optional[str] = Field(default=None, description="Additional message from the server")
    warnings: Optional[List[str]] = Field(default=None, description="Any warnings from the server")


class VideoGenerateStatusRequest(BaseModel):
    """Request model for checking video generation status."""
    
    id: str = Field(..., description="ID of the generation request to check")


class VideoGenerateStatusResponse(BaseModel):
    """Response model for video generation status."""
    
    id: str = Field(..., description="ID of the generation request")
    done: bool = Field(default=False, description="Whether the generation is complete")
    faulted: bool = Field(default=False, description="Whether the generation failed")
    finished: int = Field(default=0, description="Number of videos finished")
    processing: int = Field(default=0, description="Number of videos currently processing")
    restarted: int = Field(default=0, description="Number of times generation was restarted")
    waiting: int = Field(default=0, description="Number of videos waiting in queue")
    queue_position: int = Field(default=0, description="Position in the generation queue")
    wait_time: int = Field(default=0, description="Estimated wait time in seconds")
    kudos: float = Field(default=0.0, description="Total kudos consumed")
    is_possible: bool = Field(default=True, description="Whether generation is possible")
    generations: List[VideoGeneration] = Field(default_factory=list, description="List of generated videos")


class ImageToVideoRequest(BaseModel):
    """Request model for image-to-video generation."""
    
    source_image: str = Field(
        ...,
        description="Base64 encoded source image or URL"
    )
    prompt: Optional[str] = Field(
        default="",
        max_length=1000,
        description="Text prompt to guide the animation"
    )
    model: str = Field(
        default="stable-video-diffusion-1.1",
        description="Video generation model to use"
    )
    params: Optional[VideoGenerationParams] = Field(
        default_factory=VideoGenerationParams,
        description="Video generation parameters"
    )
    motion_scale: float = Field(
        default=1.0,
        ge=0.0,
        le=2.0,
        description="Controls the amount of motion in the video"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API key for authenticated requests"
    )


class VideoToVideoRequest(BaseModel):
    """Request model for video-to-video transformation."""
    
    source_video: str = Field(
        ...,
        description="Base64 encoded source video or URL"
    )
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Text prompt for video transformation"
    )
    model: str = Field(
        default="stable-video-diffusion-1.1",
        description="Video generation model to use"
    )
    strength: float = Field(
        default=0.8,
        ge=0.1,
        le=1.0,
        description="Transformation strength (0.1 = subtle, 1.0 = complete transformation)"
    )
    params: Optional[VideoGenerationParams] = Field(
        default_factory=VideoGenerationParams,
        description="Video generation parameters"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API key for authenticated requests"
    )


class VideoModelsResponse(BaseModel):
    """Response model for available video models."""
    
    models: List[str] = Field(..., description="List of available video generation models")


class VideoStatsResponse(BaseModel):
    """Response model for video generation statistics."""
    
    total_videos_generated: int = Field(default=0, description="Total videos generated")
    active_workers: int = Field(default=0, description="Number of active video workers")
    queue_length: int = Field(default=0, description="Current queue length")
    average_wait_time: float = Field(default=0.0, description="Average wait time in seconds")
