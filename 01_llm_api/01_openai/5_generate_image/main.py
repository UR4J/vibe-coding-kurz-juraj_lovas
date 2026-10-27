import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# dall-e-2 and dall-e-3 were shut down on 2026-05-12, gpt-image-1 on 2026-10-23.
# Current models: gpt-image-2.5-flare (fast, everyday) or gpt-image-2.5-sunburst (precise edits).
# Override in .env with IMAGE_MODEL=... when OpenAI renames models again.
IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "gpt-image-2.5-flare")

result = client.images.generate(
    model=IMAGE_MODEL,
    prompt="""{ "id": 6, "name": "Good, Weaver and Hill Tennis Racket", "description": "Unleash your potential with Good, Weaver & Hill's Tennis Racket! Crafted from durable mesh material, this racket caters to beginners, offering an ideal balance of power and control for every swing. Choose from multiple size options, ensuring a perfect fit for all players. Start your tennis journey on the right court with our training rackets - versatile, reliable, and ready to help you weave through the competition!", "category": "Sports", "price": 648.08, "stock_quantity": 75, "brand": "Good, Weaver and Hill", "sku": "SPO-000006", "weight": 3.04, "dimensions": { "length": 42.1, "width": 46.8, "height": 7.1 }, "rating": 4.4, "review_count": 218, "is_active": true, "features": { "material": "Mesh", "size_range": "Multiple sizes available", "performance": "Beginner suitable", "sport": "Training" }, "created_at": "2025-06-02 22:09:34.446510", "updated_at": "2024-12-25 08:34:12.910385" },""",
)

# GPT image models return the picture as base64, not as a URL
image_bytes = base64.b64decode(result.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)
print(f"{IMAGE_MODEL}: image saved to output.png ({len(image_bytes) // 1024} KB)")
