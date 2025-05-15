from huggingface_hub import InferenceClient
from PIL import Image # Import Image type hint
import sys
import os

# Add the project root to the Python path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import HF_TOKEN # Import the token from config

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN, # Use the token from config
)

def generate_image_from_prompt(prompt: str) -> Image.Image:
    """
    Generates an image based on the provided text prompt using the InferenceClient.

    Args:
        prompt: The text prompt to generate the image from.

    Returns:
        A PIL.Image object representing the generated image.
    """
    # output is a PIL.Image object
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev",
    )
    return image

