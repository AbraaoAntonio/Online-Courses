import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
VISION_MODEL = os.environ.get("ANTHROPIC_VISION_MODEL", "claude-sonnet-5")

REQUEST_TIMEOUT_SECONDS = float(os.environ.get("SCRAPER_TIMEOUT_SECONDS", 10))
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

MAX_UPLOAD_SIZE_BYTES = 8 * 1024 * 1024
ALLOWED_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
