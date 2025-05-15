import google.generativeai as genai
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    import config
except ImportError:
    print("Error: config.py not found. Ensure it exists in the project root.")
    sys.exit(1)

def generate_text_response(system_prompt: str, user_prompt: str, model_name: str = config.DEFAULT_GEMINI_FLASH_MODEL):
    """
    Generates a text response using a Gemini model based on system and user prompts.

    Args:
        system_prompt: Instructions or context for the model's behavior/role.
        user_prompt: The specific query or task for the model.
        model_name: The Gemini model to use (defaults to config.DEFAULT_GEMINI_PRO_MODEL).

    Returns:
        The text response from the model, or None if an error occurs.
    """
    if not config.GOOGLE_API_KEY:
        raise ValueError("API key not found. Please check your .env file and config.py.")

    genai.configure(api_key=config.GOOGLE_API_KEY)

    print(f"Using model: {model_name}")
    print(f"System Prompt: {system_prompt}")
    print(f"User Prompt: {user_prompt}")

    try:
        model = genai.GenerativeModel(
            model_name,
            # System instruction can be set here for models that support it
            # system_instruction=system_prompt
            )
        # Combine prompts for models that don't use system_instruction directly
        # Or structure as a conversation history if needed
        full_prompt = f"{system_prompt}\n\nUser Query:\n{user_prompt}"
        response = model.generate_content(full_prompt) # Or potentially pass as a list of messages

        if not response.parts:
            print("Warning: Received an empty response. This might be due to safety filters.")
            print(f"Prompt Feedback: {response.prompt_feedback}")
            return None
        if response.candidates and response.candidates[0].finish_reason.name != "STOP":
             print(f"Warning: Generation finished unexpectedly. Reason: {response.candidates[0].finish_reason.name}")

        return response.text

    except Exception as e:
        print(f"An error occurred during text generation: {e}")
        return None
