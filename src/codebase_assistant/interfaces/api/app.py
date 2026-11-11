from fastapi import FastAPI

from codebase_assistant.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name,
    }
