#!/usr/bin/env python3
"""
Test MCP server stdio communication
Simulates what Claude Desktop does when connecting to the MCP server
"""

import json
import subprocess
import sys

def test_mcp_server():
    """Test MCP server by sending initialization and list_tools requests"""

    # Path to the MCP server
    server_path = "/home/techwills/techwills/beatport-scraper/src/mcp/fastmcp_server.py"
    python_path = "/home/techwills/techwills/beatport-scraper/venv/bin/python3"

    print("Starting MCP server...")
    print(f"Command: {python_path} {server_path}\n")

    # Start the MCP server as a subprocess
    proc = subprocess.Popen(
        [python_path, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )

    try:
        # Send initialization request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        print("Sending initialize request...")
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()

        # Read response
        response_line = proc.stdout.readline()
        if response_line:
            print(f"Initialize response: {response_line.strip()}\n")

        # Send list tools request
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        print("Sending tools/list request...")
        proc.stdin.write(json.dumps(list_tools_request) + "\n")
        proc.stdin.flush()

        # Read response
        response_line = proc.stdout.readline()
        if response_line:
            print(f"Tools list response: {response_line.strip()}\n")
            response = json.loads(response_line)

            if "result" in response and "tools" in response["result"]:
                tools = response["result"]["tools"]
                print(f"✓ Found {len(tools)} tool(s):")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool.get('description', 'No description')}")
            else:
                print("✗ No tools found in response")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Clean up
        proc.terminate()
        proc.wait(timeout=5)

        # Print any stderr output
        stderr = proc.stderr.read()
        if stderr:
            print(f"\nServer stderr:\n{stderr}")


if __name__ == "__main__":
    test_mcp_server()
