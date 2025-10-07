#!/usr/bin/env python3
"""
Simplest possible video generation example using convenience method.
"""

import asyncio
from horde_video_sdk import VideoHordeAPIClient


async def main():
    """Generate a video using the simple convenience method."""
    
    async with VideoHordeAPIClient() as client:  # No API key = anonymous
        
        print("Generating video with simple method...")
        
        def progress_update(status):
            """Simple progress callback."""
            if not status.done:
                print(f"⏳ Queue position: {status.queue_position}, "
                      f"estimated wait: {status.wait_time}s")
        
        # Use the convenience method
        result = await client.generate_video_simple(
            prompt="A cat playing with a ball of yarn, cute and playful",
            duration=3.0,
            fps=24,
            resolution="1024x576",
            wait_for_completion=True,
            progress_callback=progress_update,
        )
        
        print("\n✅ Video generation completed!")
        
        if result.generations:
            video = result.generations[0]
            print(f"🎬 Video URL: {video.video_url}")
            print(f"⏱️  Duration: {video.duration}s")
            print(f"📐 Resolution: {video.resolution}")
            print(f"🎯 Model: {video.model}")
        else:
            print("❌ No video was generated.")


if __name__ == "__main__":
    asyncio.run(main())