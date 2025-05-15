import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# --- Model Names ---
DEFAULT_GEMINI_FLASH_MODEL = "gemini-1.5-flash-latest" # Changed from gemini-2.0-flash as it's more common
DEFAULT_GEMINI_PRO_MODEL = "gemini-1.5-pro-latest"

# --- File Paths ---
# Assuming 'assests' is relative to the 'src/notebooks' directory for notebooks
# Or relative to the project root for other scripts. Adjust as needed.
NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__)) # Or adjust if config.py moves
ASSETS_DIR = os.path.join(NOTEBOOKS_DIR, "src", "notebooks", "assests") # Adjust path relative to config.py location

DEFAULT_IMAGE_PATH = os.path.join(ASSETS_DIR, "website-sitemap (1).png")
DEFAULT_PDF_PATH = os.path.join(ASSETS_DIR, "MedicalAI_Chatbot.pdf")

# --- PDF Conversion ---
DEFAULT_PDF_DPI = 300

# --- Validation ---
if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")
    # You might want to raise an error here depending on your application's needs
    # raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

# You can add more configuration settings here as needed
