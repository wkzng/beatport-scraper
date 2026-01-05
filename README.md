# Beatport Metadata Extractor

<p align="center">
  <img src=illustrations/splash.png alt="" width="80%"/>
</p>

## Overview

This AWS Lambda function extracts metadata from Beatport track URLs, including preview audio URLs, cover artwork, and track information. It's designed to be deployed as a serverless function using the Serverless Framework with Docker containerization.

## Features

- **Track Metadata Extraction**: Retrieves comprehensive track information from Beatport URLs
- **Audio Preview URLs**: Extracts lofi/preview audio file URLs
- **Cover Artwork**: Fetches high-quality cover image URLs (500x500)
- **Serverless Architecture**: Runs on AWS Lambda with optimized performance
- **Docker-based Deployment**: Uses container images for consistent execution environment

## Example Usage

**Input:**
```
https://www.beatport.com/track/junin-shane-robinson-remix/7226500
```

**Output:**
```python
{
    'data': {
        'audio_url': 'https://geo-samples.beatport.com/track/09f9bd4d-10cd-4dbe-a084-8e91564c40d1.LOFI.mp3',
        'image_url': 'https://geo-media.beatport.com/image_size/500x500/d6e0659f-7da9-4ebc-99dd-8f7e05a16214.jpg',
        'platform': 'beatport',
        'title': 'Jelly For The Babies - Junin (Shane Robinson Remix) [PHW Elements] | Music & Downloads on Beatport',
        'url': 'https://www.beatport.com/track/junin-shane-robinson-remix/7226500'
    }
}
```

## Prerequisites

- [Node.js](https://nodejs.org/) (v14 or higher) and npm
- [Python 3.11](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Serverless Framework](https://www.serverless.com/)
- AWS Account with appropriate credentials configured
- AWS CLI configured with your credentials

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Install Dependencies

Install Node.js dependencies (Serverless plugins):
```bash
npm install
```

Install Python dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:
```bash
# Optional: Override default AWS region
AWS_REGION=us-east-1
```

### 4. Local Testing

Test the function locally without deploying:
```bash
make local
```

Or run the handler directly:
```bash
make test
```

## Deployment

### Deploy to AWS

Deploy to the development stage:
```bash
serverless deploy --stage dev
```

Deploy to production:
```bash
serverless deploy --stage prod
```

The deployment process will:
1. Build a Docker image from the Dockerfile
2. Push the image to AWS ECR
3. Create/update the Lambda function with the container image
4. Configure the function with 1024MB memory and 120s timeout

### Invocation

After successful deployment, you can invoke the deployed function by using the following command:

```bash
serverless invoke --stage dev --function beatport --path tests/events/beatport.json
```

Or using the Makefile shortcut:
```bash
make remote
```

Which should result in a response similar to:

```json
{
    "data": {
        "audio_url": "https://geo-samples.beatport.com/track/09f9bd4d-10cd-4dbe-a084-8e91564c40d1.LOFI.mp3",
        "image_url": "https://geo-media.beatport.com/image_size/500x500/d6e0659f-7da9-4ebc-99dd-8f7e05a16214.jpg",
        "platform": "beatport",
        "title": "Jelly For The Babies - Junin (Shane Robinson Remix) [PHW Elements] | Music & Downloads on Beatport",
        "url": "https://www.beatport.com/track/junin-shane-robinson-remix/7226500"
    }
}
```

### Local Development

You can invoke your function locally by using the following command:

```bash
serverless invoke local --stage dev --function beatport --path tests/events/beatport.json
```

Or using the Makefile:
```bash
make local
```

## API Endpoints

The Lambda function is exposed via HTTP API Gateway with both GET and POST support:

### POST Request
```bash
curl -X POST https://your-api-url/beatport \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.beatport.com/track/junin-shane-robinson-remix/7226500"}'
```

### GET Request
```bash
curl "https://your-api-url/beatport?url=https://www.beatport.com/track/junin-shane-robinson-remix/7226500"
```

### Testing API Locally
```bash
# Set up environment variables in .env
API_URL=https://your-api-url/beatport
TEST_URL=https://www.beatport.com/track/junin-shane-robinson-remix/7226500

# Run the API test script
python tests/invoke_api.py
```

## MCP Server (Claude Desktop Integration)

The Beatport scraper can be used as an MCP (Model Context Protocol) server, allowing Claude Desktop to extract metadata from Beatport tracks directly in conversations.

### What is MCP?

MCP (Model Context Protocol) allows Claude Desktop to interact with external tools and services. This integration exposes the Beatport scraper as a tool that Claude can automatically use when you ask about Beatport tracks.

### Quick Start

1. **Install MCP dependencies:**
   ```bash
   pip install -r mcp_requirements.txt
   ```

2. **Configure Claude Desktop:**

   **Step 1:** Locate your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

   If the file doesn't exist, create it with `{}` as the initial content.

   **Step 2:** Add the MCP server configuration:

   **For macOS/Linux:**
   ```json
   {
     "mcpServers": {
       "beatport-scraper": {
         "command": "/absolute/path/to/beatport-scraper/venv/bin/python3",
         "args": [
           "/absolute/path/to/beatport-scraper/src/mcp/server.py"
         ]
       }
     }
   }
   ```

   **For Windows with WSL:**
   ```json
   {
     "mcpServers": {
       "beatport-scraper": {
         "command": "wsl",
         "args": [
           "-e",
           "/home/username/path/to/beatport-scraper/venv/bin/python3",
           "/home/username/path/to/beatport-scraper/src/mcp/server.py"
         ]
       }
     }
   }
   ```

   **Important Notes:**
   - Replace `/absolute/path/to/beatport-scraper` with your actual project path
   - For WSL, use Linux paths (e.g., `/home/username/...`)
   - Paths must be absolute, not relative

3. **Test the configuration (optional):**

   Before restarting Claude Desktop, test that the MCP server works:

   **On macOS/Linux:**
   ```bash
   /path/to/beatport-scraper/venv/bin/python3 /path/to/beatport-scraper/src/mcp/server.py
   ```

   **On Windows with WSL:**
   ```powershell
   wsl -e /home/username/path/to/beatport-scraper/venv/bin/python3 /home/username/path/to/beatport-scraper/src/mcp/server.py
   ```

   The server should start and show a FastMCP banner. Press `Ctrl+C` to stop it.

4. **Restart Claude Desktop:**

   - **Fully quit** Claude Desktop (don't just close the window)
   - On Windows: Right-click the system tray icon and select "Quit" or use Task Manager
   - On macOS: Right-click the dock icon and select "Quit"
   - Wait a few seconds, then relaunch Claude Desktop

5. **Use it in Claude Desktop:**

   Once configured, simply ask Claude about Beatport tracks:
   - "Get metadata for this Beatport track: https://www.beatport.com/track/junin-shane-robinson-remix/7226500"
   - "Extract the audio preview URL from https://www.beatport.com/track/never-get-enough/15766697"

   Claude will automatically use the MCP server to extract track information including title, preview audio URL, and cover image.

### Testing the MCP Server

Test the MCP server independently before configuring Claude Desktop:

```bash
# Run the test suite
python tests/test_mcp.py

# Or test the MCP stdio protocol directly
python tests/test_mcp_stdio.py

# Or run the server directly (press Ctrl+C to stop)
python src/mcp/server.py
```

### Troubleshooting

**Claude Desktop doesn't see the MCP server:**
- Ensure you fully quit and restarted Claude Desktop (not just closed the window)
- Check that paths in the config are absolute and correct
- On Windows, verify WSL is working: `wsl echo "test"`
- Test the command manually before adding to Claude Desktop config

**Server fails to start:**
- Verify dependencies are installed: `pip install -r requirements_mcp.txt`
- Check Python path is correct: `which python3` (in WSL/Linux) or `where python` (Windows)
- Ensure the virtual environment is activated when testing


## Project Structure
```
.
├── Dockerfile             # Container configuration for Lambda
├── Makefile               # Common commands for testing and deployment
├── README.md              # This file
├── package.json           # Node.js dependencies (Serverless plugins)
├── requirements_prod.txt  # Python dependencies
├── requirements_mcp.txt   # MCP server dependencies
├── serverless.yml         # Serverless Framework configuration
├── src/                   # Source code
│   ├── handler.py         # Lambda handler function
│   └── mcp/               # MCP server implementations
│       └── server.py      # FastMCP server
└── tests/                 # Test files
    ├── events/
    │   └── beatport.json       # Sample event for testing
    ├── test_invoke_lambda.py   # Lambda invocation script
    ├── test_invoke_api.py      # API HTTP request script
    └── test_mcp_stdio.py       # MCP server test suite
```

## Configuration

### Lambda Function Settings

The function is configured with the following settings (defined in `serverless.yml`):

- **Runtime**: Python 3.11 (via Docker container)
- **Timeout**: 120 seconds
- **Memory**: 1024 MB
- **Ephemeral Storage**: 512 MB
- **Platform**: linux/amd64

### Serverless Plugins

- `serverless-prune-plugin`: Automatically removes old Lambda versions (keeps last 2)
- `serverless-dotenv-plugin`: Loads environment variables from .env files

## Troubleshooting

### Docker Issues

If you encounter Docker-related errors during deployment:
```bash
# Ensure Docker is running
docker ps

# Build image locally to test
docker build -t beatport-test .
```

### AWS Credentials

Ensure your AWS credentials are properly configured:
```bash
aws configure list
```

### Lambda Timeout

If tracks are timing out, increase the timeout in `serverless.yml`:
```yaml
functions:
  beatport:
    timeout: 180  # Increase from 120 to 180 seconds
```