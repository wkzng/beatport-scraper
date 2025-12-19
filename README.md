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

## Project Structure

```
.
├── Dockerfile              # Container configuration for Lambda
├── Makefile               # Common commands for testing and deployment
├── README.md              # This file
├── package.json           # Node.js dependencies (Serverless plugins)
├── requirements.txt       # Python dependencies
├── serverless.yml         # Serverless Framework configuration
├── src/                   # Source code
│   └── handler.py         # Lambda handler function
└── tests/                 # Test files
    └── events/
        └── beatport.json  # Sample event for testing
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