from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from . import routers

# Initialize FastAPI App
app = FastAPI(
    title="DevUtility API Vault",
    description="A collection of useful developer utilities, built with FastAPI.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "url": "https://github.com/YOUR_USERNAME/dev-utility-api-vault", # Replace with your repo link
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Include the router from routers.py
app.include_router(routers.router)

# Generic Exception Handler (Step 6.2)
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handles any unexpected server errors for a clean response."""
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected server error occurred: {exc}"},
    )

# Root Endpoint (Health Check)
@app.get("/", tags=["Health Check"])
async def root():
    """A simple health check endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Welcome to DevUtility API Vault!"}