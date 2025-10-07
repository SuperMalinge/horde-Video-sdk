#!/usr/bin/env python3
"""
Image-to-video generation example.
"""

import asyncio
import base64
from pathlib import Path
from horde_video_sdk import (
    VideoHordeAPIClient,
    ImageToVideoRequest,
    VideoGenerationParams,
    VideoResolution,
)


def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


async def main():
    """Generate a video from a source image."""
    
    # Path to your source image
    image_path = "path/to/your/image.jpg"  # Replace with actual path
    
    # Check if image exists
    if not Path(image_path).exists():
        print(f"Image not found: {image_path}")
        print("Please provide a valid image path or use a URL instead.")
        return
    
    # Initialize client
    async with VideoHordeAPIClient(api_token="your_api_key_here") as client:
        
        # Encode image to base64
        print("Encoding image...")
        image_base64 = encode_image_to_base64(image_path)
        
        # Create video generation parameters
        params = VideoGenerationParams(
            duration=3.0,  # 3 seconds
            fps=24,
            resolution=VideoResolution.HD_1024_576,
            motion_scale=0.8,  # Subtle motion for image animation
        )
        
        # Create the request
        request = ImageToVideoRequest(
            source_image=image_base64,
            prompt="gentle movement, natural animation, smooth transitions",
            model="stable-video-diffusion-1.1",
            params=params,
            motion_scale=0.8,
        )
        
        print("Submitting image-to-video generation request...")
        
        # Submit the request
        response = await client.generate_video_from_image(request)
        print(f"Request submitted! Job ID: {response.id}")
        
        # Use the simple wait method
        print("Waiting for video generation to complete...")
        final_status = await client.wait_for_video_generation(
            response.id,
            poll_interval=15,  # Check every 15 seconds for longer processes
        )
        
        # Check results
        if final_status.generations:
            generation = final_status.generations[0]
            print(f"\nVideo generated successfully!")
            print(f"Video URL: {generation.video_url}")
            print(f"Duration: {generation.duration}s")
            print(f"Resolution: {generation.resolution}")
        else:
            print("No video was generated.")


if __name__ == "__main__":
    asyncio.run(main())