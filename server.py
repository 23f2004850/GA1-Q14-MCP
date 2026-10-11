
import hashlib
import re

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

# Your registered exam email
EMAIL = "23f2004850@ds.study.iitm.ac.in".strip().lower()

# Create an MCP server
mcp = FastMCP("IITM Exam Challenge Server")


@mcp.tool()
def solve_challenge() -> str:
    """Solve the current exam challenge from its HTTP header."""

    # Read headers from this individual HTTP request
    headers = get_http_headers()
    challenge = headers.get("x-exam-challenge")

    # Validate the challenge format
    if not challenge or not re.fullmatch(r"[0-9a-f]{32}", challenge):
        raise ValueError("Missing or invalid X-Exam-Challenge header")

    # Combine challenge and normalized email
    message = f"{challenge}:{EMAIL}"

    # Calculate SHA-256
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()

    # Return exactly the first 16 hexadecimal characters
    return digest[:16]


# Create a public-facing Streamable HTTP MCP application
app = mcp.http_app(
    path="/mcp",
    stateless_http=True,
    json_response=True
)
