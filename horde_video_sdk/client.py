"""
Async API client for video generation with AI-Horde.
"""
from __future__ import annotations

import asyncio
import aiohttp
import time
from typing import Optional, Dict, Any, Union
from loguru import logger

from horde_video_sdk.models import (
    VideoGenerateAsyncRequest,
    VideoGenerateAsyncResponse,
    VideoGenerateStatusRequest,
    VideoGenerateStatusResponse,
    ImageToVideoRequest,
    VideoToVideoRequest,
    VideoModelsResponse,
    VideoStatsResponse,
)
from horde_video_sdk.video_config import (
    VIDEO_API_BASE,
    VIDEO_ENDPOINTS,
    DEFAULT_TIMEOUT,
)


class VideoHordeAPIError(Exception):
    """Exception raised for API errors."""
    pass


class VideoHordeAPIClient:
    """Async client for AI-Horde video generation API."""

    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: str = VIDEO_API_BASE,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        Initialize the video API client.
        
        Args:
            api_token: Optional API token for authenticated requests
            base_url: Base URL for the API
            timeout: Request timeout in seconds
        """
        self.api_token = api_token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "VideoHordeAPIClient":
        """Async context manager entry."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()

    async def _ensure_session(self) -> None:
        """Ensure aiohttp session is created."""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "horde-video-sdk/0.1.0",
        }
        if self.api_token:
            headers["apikey"] = self.api_token
        return headers

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request data
            
        Returns:
            Response data as dictionary
            
        Raises:
            VideoHordeAPIError: If the request fails
        """
        await self._ensure_session()
        
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            async with self._session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
            ) as response:
                response_data = await response.json()
                
                if response.status >= 400:
                    error_msg = response_data.get("message", f"HTTP {response.status}")
                    logger.error(f"API error {response.status}: {error_msg}")
                    raise VideoHordeAPIError(f"API error {response.status}: {error_msg}")
                
                logger.debug(f"Request successful: {response.status}")
                return response_data
                
        except aiohttp.ClientError as e:
            logger.error(f"Request failed: {e}")
            raise VideoHordeAPIError(f"Request failed: {e}")

    async def generate_video_async(
        self,
        request: VideoGenerateAsyncRequest,
    ) -> VideoGenerateAsyncResponse:
        """
        Submit an asynchronous video generation request.
        
        Args:
            request: Video generation request
            
        Returns:
            Response with job ID for tracking
        """
        # Set API key if provided in client but not in request
        if self.api_token and not request.api_key:
            request.api_key = self.api_token
            
        data = request.dict(exclude_none=True)
        response_data = await self._make_request(
            "POST",
            VIDEO_ENDPOINTS["generate_async"],
            data,
        )
        
        return VideoGenerateAsyncResponse(**response_data)

    async def check_video_status(
        self,
        job_id: str,
    ) -> VideoGenerateStatusResponse:
        """
        Check the status of a video generation request.
        
        Args:
            job_id: ID of the video generation job
            
        Returns:
            Status response with generation progress and results
        """
        endpoint = VIDEO_ENDPOINTS["generate_status"].format(id=job_id)
        response_data = await self._make_request("GET", endpoint)
        
        return VideoGenerateStatusResponse(**response_data)

    async def cancel_video_generation(
        self,
        job_id: str,
    ) -> VideoGenerateStatusResponse:
        """
        Cancel a pending video generation request.
        
        Args:
            job_id: ID of the video generation job to cancel
            
        Returns:
            Final status response
        """
        endpoint = VIDEO_ENDPOINTS["generate_cancel"].format(id=job_id)
        response_data = await self._make_request("DELETE", endpoint)
        
        return VideoGenerateStatusResponse(**response_data)

    async def wait_for_video_generation(
        self,
        job_id: str,
        poll_interval: int = 10,
        max_wait_time: Optional[int] = None,
        progress_callback: Optional[callable] = None,
    ) -> VideoGenerateStatusResponse:
        """
        Wait for a video generation to complete with polling.
        
        Args:
            job_id: ID of the video generation job
            poll_interval: Seconds between status checks
            max_wait_time: Maximum time to wait in seconds
            progress_callback: Optional callback for progress updates
            
        Returns:
            Final status response with generated videos
        """
        start_time = time.time()
        
        while True:
            status = await self.check_video_status(job_id)
            
            if progress_callback:
                progress_callback(status)
            
            if status.done:
                logger.info(f"Video generation {job_id} completed successfully")
                return status
            
            if status.faulted:
                logger.error(f"Video generation {job_id} failed")
                raise VideoHordeAPIError(f"Video generation {job_id} failed")
            
            # Check if we've exceeded max wait time
            if max_wait_time and (time.time() - start_time) > max_wait_time:
                logger.error(f"Video generation {job_id} timed out after {max_wait_time}s")
                raise VideoHordeAPIError(f"Video generation timed out after {max_wait_time}s")
            
            logger.debug(
                f"Video generation {job_id} in progress. "
                f"Queue position: {status.queue_position}, "
                f"Wait time: {status.wait_time}s"
            )
            
            await asyncio.sleep(poll_interval)

    async def generate_video_from_image(
        self,
        request: ImageToVideoRequest,
    ) -> VideoGenerateAsyncResponse:
        """
        Generate a video from a source image.
        
        Args:
            request: Image-to-video generation request
            
        Returns:
            Response with job ID for tracking
        """
        # Set API key if provided in client but not in request
        if self.api_token and not request.api_key:
            request.api_key = self.api_token
            
        data = request.dict(exclude_none=True)
        response_data = await self._make_request(
            "POST",
            VIDEO_ENDPOINTS["generate_async"],  # Same endpoint, different parameters
            data,
        )
        
        return VideoGenerateAsyncResponse(**response_data)

    async def transform_video(
        self,
        request: VideoToVideoRequest,
    ) -> VideoGenerateAsyncResponse:
        """
        Transform an existing video using a text prompt.
        
        Args:
            request: Video-to-video transformation request
            
        Returns:
            Response with job ID for tracking
        """
        # Set API key if provided in client but not in request
        if self.api_token and not request.api_key:
            request.api_key = self.api_token
            
        data = request.dict(exclude_none=True)
        response_data = await self._make_request(
            "POST",
            VIDEO_ENDPOINTS["generate_async"],  # Same endpoint, different parameters
            data,
        )
        
        return VideoGenerateAsyncResponse(**response_data)

    async def get_available_models(self) -> VideoModelsResponse:
        """
        Get list of available video generation models.
        
        Returns:
            Response with available models
        """
        response_data = await self._make_request("GET", VIDEO_ENDPOINTS["models"])
        
        return VideoModelsResponse(**response_data)

    async def get_video_stats(self) -> VideoStatsResponse:
        """
        Get video generation statistics.
        
        Returns:
            Response with current statistics
        """
        # Note: This endpoint might not exist yet in actual API
        # This is a placeholder for future implementation
        response_data = await self._make_request("GET", "/v2/status/video/stats")
        
        return VideoStatsResponse(**response_data)

    # Convenience methods for common workflows
    
    async def generate_video_simple(
        self,
        prompt: str,
        duration: float = 3.0,
        fps: int = 24,
        resolution: str = "1024x576",
        model: str = "stable-video-diffusion-1.1",
        wait_for_completion: bool = True,
        progress_callback: Optional[callable] = None,
    ) -> Union[VideoGenerateAsyncResponse, VideoGenerateStatusResponse]:
        """
        Simple video generation with common parameters.
        
        Args:
            prompt: Text prompt for video generation
            duration: Video duration in seconds
            fps: Frames per second
            resolution: Video resolution
            model: Model to use for generation
            wait_for_completion: Whether to wait for completion
            progress_callback: Optional progress callback
            
        Returns:
            Either async response (if not waiting) or final status (if waiting)
        """
        from horde_video_sdk.models import VideoGenerationParams
        
        params = VideoGenerationParams(
            duration=duration,
            fps=fps,
            resolution=resolution,
        )
        
        request = VideoGenerateAsyncRequest(
            prompt=prompt,
            model=model,
            params=params,
        )
        
        response = await self.generate_video_async(request)
        
        if wait_for_completion:
            return await self.wait_for_video_generation(
                response.id,
                progress_callback=progress_callback,
            )
        
        return response
