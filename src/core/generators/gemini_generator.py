import google.generativeai as genai
import PIL.Image
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

import config

def ask_gemini_about_image(image_path: str, text_prompt: str, model_name: str = config.DEFAULT_GEMINI_FLASH_MODEL):
    """
    Sends an image and a text prompt to the specified Gemini model.

    Args:
        image_path: Path to the image file.
        text_prompt: The question or instruction related to the image.
        model_name: The Gemini model to use (defaults to config.DEFAULT_GEMINI_FLASH_MODEL).

    Returns:
        The text response from the model, or None if an error occurs.
    """
    if not config.GOOGLE_API_KEY:
        raise ValueError("API key not found. Please check your .env file and config.py.")

    genai.configure(api_key=config.GOOGLE_API_KEY)

    print(f"Loading image from: {image_path}")
    print(f"Using model: {model_name}")
    print(f"Sending prompt: {text_prompt}")

    try:
        img = PIL.Image.open(image_path)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content([text_prompt, img])

        if not response.parts:
            print("Warning: Received an empty response. This might be due to safety filters.")
            print(f"Prompt Feedback: {response.prompt_feedback}")
            return None
        if response.candidates and response.candidates[0].finish_reason.name != "STOP":
            print(f"Warning: Generation finished unexpectedly. Reason: {response.candidates[0].finish_reason.name}")

        return response.text

    except FileNotFoundError:
        print(f"Error: Image file not found at '{image_path}'")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None