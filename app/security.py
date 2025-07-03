import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

# This line loads the environment variables from your .env file
load_dotenv()

# Define the header we expect to receive from RapidAPI
api_key_header = APIKeyHeader(name="X-RapidAPI-Proxy-Secret", auto_error=False)

# Get our secret key from the environment variables
RAPIDAPI_PROXY_SECRET = os.getenv("RAPIDAPI_PROXY_SECRET")

async def verify_rapidapi_secret(api_key: str = Security(api_key_header)):
    """
    This is the dependency that will be used to protect the endpoints.
    It checks if the incoming request has the correct secret key.
    """
    # First, check if the secret is even configured on our server.
    # If not, it's a server error.
    if not RAPIDAPI_PROXY_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API secret not configured on the server."
        )

    # Check if the header was provided and if it matches our secret.
    # If not, the request is forbidden.
    if not api_key or api_key != RAPIDAPI_PROXY_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API secret."
        )
    
    # If the key is valid, the request is allowed to proceed.
    return True