# horde-Video-sdk

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Status: Beta](https://img.shields.io/badge/status-beta-orange)](https://github.com/SuperMalinge/horde-Video-sdk)

## Note

horde-Video-sdk is in **beta** and under active development. Everything is subject to change. This is a fork of [horde-sdk](https://github.com/Haidra-Org/horde-sdk) modified to support video generation instead of image generation.

## About

This library simplifies interfacing with AI-Horde's video generation APIs. Built on the foundation of the original horde-sdk, this fork extends functionality to support:

- **Text-to-Video Generation** (Stable Video Diffusion, AnimateDiff, CogVideoX)
- **Image-to-Video Generation** (animate static images)
- **Video-to-Video Transformation** (style transfer, enhancement)
- **Video Captioning** (understanding video content)
- **Video Quality Assessment** (rating and analysis)

From requesting your own videos to rolling your own worker software for video generation, this package aims to make AI-powered video creation accessible through AI-Horde's volunteer-driven infrastructure.

## Key Differences from horde-sdk

- **Extended Processing Times**: Video generation takes 5-15 minutes vs seconds for images
- **Larger File Sizes**: Videos require specialized storage and streaming capabilities
- **Temporal Consistency**: Additional parameters for frame-to-frame coherence
- **Video Formats**: Support for MP4, WebM, GIF with configurable codecs
- **Frame-based Workflows**: Progressive generation and partial results

## Installation

```bash
pip install horde-video-sdk
```

### Requirements

- Python >= 3.10
- FFmpeg (for video processing)
- Sufficient disk space for temporary video files

## Quick Start

### Text-to-Video Generation

```python
from horde_video_sdk import VideoHordeAPIClient
from horde_video_sdk.models import VideoGenerateAsyncRequest

# Initialize client
client = VideoHordeAPIClient(api_token="YOUR_API_KEY")

# Create video generation request
request = VideoGenerateAsyncRequest(
    prompt="A serene ocean wave at sunset, cinematic",
    duration=4.0,  # seconds
    fps=24,
    resolution="1024x576",
    motion_scale=1.2,
    model="stable-video-diffusion-1.1"
)

# Submit request
response = await client.generate_video_async(request)
print(f"Video generation started: {response.id}")

# Poll for completion
status = await client.check_video_status(response.id)
while not status.done:
    print(f"Progress: {status.wait_time}s remaining")
    await asyncio.sleep(10)
    status = await client.check_video_status(response.id)

# Download result
video_url = status.generations[0].video_url
print(f"Video ready: {video_url}")
```

## Documentation

See the complete documentation at [ReadTheDocs](https://horde-video-sdk.readthedocs.io/) (coming soon).

For deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

For contributing guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

AGPL-3.0 License - See [LICENSE](LICENSE) for details

## Credits

This project is a fork of [horde-sdk](https://github.com/Haidra-Org/horde-sdk) by the Haidra Organization. Special thanks to the AI-Horde community for building the infrastructure that makes free, distributed AI generation possible.

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/SuperMalinge/horde-Video-sdk/issues)
- AI-Horde Discord: [Join the community](https://discord.gg/aihorde)