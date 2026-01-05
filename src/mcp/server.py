import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastmcp import FastMCP
from src.handler import extract_audio_metadata, is_valid_beatport_url, ExecutionStatus

# Create FastMCP server instance
mcp = FastMCP("beatport-scraper")


@mcp.tool()
def get_beatport_metadata(url: str) -> dict:
    """
    Extract audio metadata from a Beatport track URL.

    Args:
        url: The Beatport track URL (e.g., https://www.beatport.com/track/track-name/123456)

    Returns:
        A dictionary containing:
        - status: "success" or "error"
        - track: Dictionary with title, url, audio_url, image_url, platform (on success)
        - message: Error message (on error)

    Examples:
        >>> get_beatport_metadata("https://www.beatport.com/track/junin-shane-robinson-remix/7226500")
        {
            "status": "success",
            "track": {
                "title": "Junin (Shane Robinson Remix)",
                "url": "https://www.beatport.com/track/junin-shane-robinson-remix/7226500",
                "audio_url": "https://geo-samples.beatport.com/.../LOFI.mp3",
                "image_url": "https://i1.sndcdn.com/.../artworks-...-large.jpg",
                "platform": "beatport"
            }
        }
    """
    # Validate URL
    if not is_valid_beatport_url(url):
        return {
            "status": "error",
            "message": "Invalid Beatport URL. Valid URLs typically start with https://www.beatport.com/track/"
        }

    # Extract metadata
    result = extract_audio_metadata(url)

    # Format response
    if result.get("status") == ExecutionStatus.SUCCESS:
        data = result.get("data", {})
        return {
            "status": "success",
            "track": {
                "title": data.get("title"),
                "url": data.get("url"),
                "audio_url": data.get("audio_url"),
                "image_url": data.get("image_url"),
                "platform": data.get("platform")
            }
        }
    else:
        return {
            "status": "error",
            "message": result.get("message", "Failed to extract metadata")
        }


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run(transport="stdio")
