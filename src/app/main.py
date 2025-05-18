from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AutoDev Commander",
    description="AI-Driven Development Orchestration",
    version="0.1.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "operational",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "ollama": "operational",
            "qdrant": "operational",
            "redis": "operational",
            "n8n": "operational"
        }
    }
