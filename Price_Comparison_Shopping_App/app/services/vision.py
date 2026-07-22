import base64
import logging
from typing import Optional

from app.config import ANTHROPIC_API_KEY, VISION_MODEL

logger = logging.getLogger(__name__)

PROMPT = (
    "Olhe esta imagem de um produto que um cliente quer comprar. "
    "Responda apenas com um termo de busca curto e objetivo (marca, modelo e "
    "principais características), em português, pronto para ser usado numa "
    "busca em sites de e-commerce. Não escreva mais nada além do termo de busca."
)


def is_configured() -> bool:
    return bool(ANTHROPIC_API_KEY)


def describe_product_image(image_bytes: bytes, media_type: str) -> Optional[str]:
    """Uses Claude's vision capability to turn a product photo into a
    short search query. Returns None if no API key is configured or the
    call fails, so callers should fall back to asking for a text
    description."""
    if not is_configured():
        return None

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
        message = client.messages.create(
            model=VISION_MODEL,
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": PROMPT},
                    ],
                }
            ],
        )
        text_blocks = [block.text for block in message.content if block.type == "text"]
        description = " ".join(text_blocks).strip()
        return description or None
    except Exception as exc:
        logger.warning("Vision description failed: %s", exc)
        return None
