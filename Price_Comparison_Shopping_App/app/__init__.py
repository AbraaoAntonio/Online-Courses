from flask import Flask, render_template, request

from app.config import ALLOWED_IMAGE_MIME_TYPES, MAX_UPLOAD_SIZE_BYTES
from app.services import vision
from app.services.search import cheapest, compare_prices


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE_BYTES

    @app.template_filter("brl")
    def format_brl(value):
        if value is None:
            return "—"
        return f"R$ {value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

    @app.get("/")
    def index():
        return render_template("index.html", vision_enabled=vision.is_configured())

    @app.post("/buscar")
    def buscar():
        description = (request.form.get("description") or "").strip()
        image = request.files.get("image")
        image_note = None

        if image and image.filename:
            if image.mimetype not in ALLOWED_IMAGE_MIME_TYPES:
                return render_template(
                    "index.html",
                    vision_enabled=vision.is_configured(),
                    error="Formato de imagem não suportado. Envie JPEG, PNG ou WebP.",
                )
            image_bytes = image.read()
            image_description = vision.describe_product_image(image_bytes, image.mimetype)
            if image_description:
                description = f"{description} {image_description}".strip()
                image_note = f'A imagem foi interpretada como: "{image_description}"'
            elif not description:
                return render_template(
                    "index.html",
                    vision_enabled=vision.is_configured(),
                    error=(
                        "Não consegui interpretar a imagem automaticamente "
                        "(nenhuma chave de IA de visão configurada, ou a "
                        "leitura falhou). Escreva uma breve descrição do "
                        "produto junto com a imagem."
                    ),
                )

        if not description:
            return render_template(
                "index.html",
                vision_enabled=vision.is_configured(),
                error="Descreva o produto ou envie uma imagem com descrição.",
            )

        results = compare_prices(description)
        return render_template(
            "results.html",
            query=description,
            image_note=image_note,
            results=results,
            best=cheapest(results),
        )

    return app
