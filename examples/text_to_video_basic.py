#!/usr/bin/env python3
"""
Basic text-to-video generation example.
"""

import asyncio
from horde_video_sdk import (
    VideoHordeAPIClient,
    VideoGenerateAsyncRequest,
    VideoGenerationParams,
    VideoResolution,
    VideoFormat,
)


async def main():
    """Generate a video from text prompt."""
    
    # Initialize client (use your API key if you have one)
    async with VideoHordeAPIClient(api_token="your_api_key_here") as client:
        
        # Create video generation parameters
        params = VideoGenerationParams(
            duration=4.0,  # 4 seconds
            fps=24,
            resolution=VideoResolution.HD_1024_576,
            format=VideoFormat.MP4,
            motion_scale=1.2,  # More dynamic motion
        )
        
        # Create the request
        request = VideoGenerateAsyncRequest(
            prompt="A serene ocean wave at sunset, cinematic lighting, peaceful atmosphere",
            negative_prompt="blurry, low quality, distorted",
            model="stable-video-diffusion-1.1",
            params=params,
            nsfw=False,
        )
        
        print("Submitting video generation request...")
        
        # Submit the request
        response = await client.generate_video_async(request)
        print(f"Request submitted! Job ID: {response.id}")
        print(f"Estimated kudos cost: {response.kudos}")
        
        # Define progress callback
        def progress_callback(status):
            print(f"Progress - Queue position: {status.queue_position}, "
                  f"Wait time: {status.wait_time}s, "
                  f"Processing: {status.processing}, "
                  f"Finished: {status.finished}")
        
        # Wait for completion
        print("Waiting for video generation to complete...")
        final_status = await client.wait_for_video_generation(
            response.id,
            poll_interval=10,  # Check every 10 seconds
            progress_callback=progress_callback,
        )
        
        # Check results
        if final_status.generations:
            for i, generation in enumerate(final_status.generations):
                print(f"\nGenerated video {i + 1}:")
                print(f"  Video URL: {generation.video_url}")
                print(f"  Worker: {generation.worker_name}")
                print(f"  Model: {generation.model}")
                print(f"  Duration: {generation.duration}s")
                print(f"  Resolution: {generation.resolution}")
                print(f"  Seed: {generation.seed}")
        else:
            print("No videos were generated.")


if __name__ == "__main__":
    asyncio.run(main())