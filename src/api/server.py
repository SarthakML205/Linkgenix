import os
import sys
import shutil
import tempfile
import fitz  # PyMuPDF
import uvicorn
import io  # Add io for image streaming
from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse, StreamingResponse  # Add StreamingResponse
from PIL import Image  # Add PIL Image

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from src.core.generators.gemini_generator import ask_gemini_about_image
    from src.core.generators.text_generator import generate_text_response
    from src.core.generators.image_generator import generate_image_from_prompt  # Add image generator import
    from src.core.prompts.content_creation_prompt import content_prompt
    from src.core.prompts.formatter_prompt import formatting_prompt
    from src.core.prompts.seo_prompt import seo_prompt
    from src.core.prompts.image_prompt import image_prompt  # Add image prompt import
    import config
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

app = FastAPI(
    title="LinkGenix API",
    description="API for processing documents and generating insights.",
    version="0.1.0"
)

@app.post("/analyze-pdf/")
async def analyze_pdf(file: UploadFile = File(...)):
    """
    Accepts a PDF file, converts each page to an image,
    analyzes each image using Gemini, and returns the combined description.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, file.filename)
        images_dir = os.path.join(temp_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        try:
            with open(pdf_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {e}")
        finally:
            await file.close()

        all_descriptions = []
        page_count = 0

        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)

            if page_count == 0:
                 raise HTTPException(status_code=400, detail="The uploaded PDF has no pages.")

            for i, page in enumerate(doc):
                image_path = os.path.join(images_dir, f"page_{i+1}.png")
                pix = page.get_pixmap(dpi=150)
                pix.save(image_path)

                prompt = f"Describe the content of this document page ({i+1}/{page_count}). Focus on the main text, figures, and layout.summarize it and provide all key information."
                try:
                    description = ask_gemini_about_image(
                        image_path=image_path,
                        text_prompt=prompt,
                        model_name=config.DEFAULT_GEMINI_FLASH_MODEL
                    )
                    if description:
                        all_descriptions.append(f"--- Page {i+1} ---\n{description}\n")
                    else:
                        all_descriptions.append(f"--- Page {i+1} ---\n[No description returned from Gemini]\n")
                except Exception as gemini_error:
                    print(f"Error processing page {i+1} with Gemini: {gemini_error}")
                    all_descriptions.append(f"--- Page {i+1} ---\n[Error analyzing page: {gemini_error}]\n")
                finally:
                    pass

            doc.close()

        except fitz.fitz.FileNotFoundError:
             raise HTTPException(status_code=404, detail="Temporary PDF file not found during processing.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")

    combined_text = "\n".join(all_descriptions)

    if not combined_text:
         return JSONResponse(
             status_code=200,
             content={"message": "PDF processed, but no descriptions were generated.", "analysis": ""}
         )

    return JSONResponse(content={"analysis": combined_text})

@app.post("/generate-content/")
async def create_linkedin_post(user_input_string: str = Body(..., media_type="text/plain")):
    """
    Generates content based on a user-provided input string and a predefined system prompt.
    The input string should contain all necessary details for the content generation.
    """
    # The received string is the user prompt
    full_user_prompt = user_input_string

    # Basic validation: ensure the input string is not empty
    if not full_user_prompt:
        raise HTTPException(status_code=400, detail="Input string cannot be empty.")

    try:
        # Use the predefined content_prompt as the system prompt
        # and the received string as the user prompt
        generated_content = generate_text_response(
            system_prompt=content_prompt,
            user_prompt=full_user_prompt,
            model_name=config.DEFAULT_GEMINI_PRO_MODEL
        )

        if generated_content:
            # Return the generated content directly, perhaps in a JSON structure
            return JSONResponse(content={"generated_content": generated_content})
        else:
            # Handle cases where the generator returns None (e.g., safety filters, errors)
            raise HTTPException(status_code=500, detail="Failed to generate content. The model returned an empty response or an error occurred.")

    except ValueError as ve:
         raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        print(f"Error during content generation: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during content generation: {e}")

@app.post("/format-content/")
async def format_generated_content(raw_content: str = Body(..., media_type="text/plain")):
    """
    Formats the provided raw content string using a predefined formatting prompt
    and the text generation model.
    """
    # Basic validation: ensure the input string is not empty
    if not raw_content:
        raise HTTPException(status_code=400, detail="Input content string cannot be empty.")

    try:
        # Use the formatting_prompt as the system prompt
        # and the received raw_content as the user prompt
        formatted_content = generate_text_response(
            system_prompt=formatting_prompt,
            user_prompt=raw_content,
            model_name=config.DEFAULT_GEMINI_PRO_MODEL
        )

        if formatted_content:
            # Return the formatted content
            return JSONResponse(content={"formatted_content": formatted_content})
        else:
            # Handle cases where the generator returns None
            raise HTTPException(status_code=500, detail="Failed to format content. The model returned an empty response or an error occurred.")

    except ValueError as ve:
         raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        print(f"Error during content formatting: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during content formatting: {e}")

@app.post("/optimize-seo/")
async def optimize_content_seo(formatted_content: str = Body(..., media_type="text/plain")):
    """
    Analyzes the provided formatted content string using an SEO prompt
    and the text generation model to suggest SEO improvements.
    """
    # Basic validation: ensure the input string is not empty
    if not formatted_content:
        raise HTTPException(status_code=400, detail="Input formatted content string cannot be empty.")

    try:
        # Use the seo_prompt as the system prompt
        # and the received formatted_content as the user prompt
        seo_suggestions = generate_text_response(
            system_prompt=seo_prompt,
            user_prompt=formatted_content,
            model_name=config.DEFAULT_GEMINI_PRO_MODEL
        )

        if seo_suggestions:
            # Return the SEO suggestions
            return JSONResponse(content={"seo_suggestions": seo_suggestions})
        else:
            # Handle cases where the generator returns None
            raise HTTPException(status_code=500, detail="Failed to generate SEO suggestions. The model returned an empty response or an error occurred.")

    except ValueError as ve:
         raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        print(f"Error during SEO optimization: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during SEO optimization: {e}")

@app.post("/generate-image/")
async def generate_image_endpoint(input_text: str = Body(..., media_type="text/plain")):
    """
    Generates an image prompt based on input text and then generates an image.
    """
    if not input_text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        # 1. Generate the image prompt using the text generator
        generated_image_prompt = generate_text_response(
            system_prompt=image_prompt,
            user_prompt=input_text,
            model_name=config.DEFAULT_GEMINI_PRO_MODEL  # Or choose another suitable model
        )

        if not generated_image_prompt:
            raise HTTPException(status_code=500, detail="Failed to generate image prompt.")

        # 2. Generate the image using the generated prompt
        generated_image: Image.Image = generate_image_from_prompt(generated_image_prompt)

        if not generated_image:
             raise HTTPException(status_code=500, detail="Failed to generate image.")

        # 3. Prepare the image for response
        img_byte_arr = io.BytesIO()
        generated_image.save(img_byte_arr, format='PNG')  # Save image to buffer
        img_byte_arr.seek(0)  # Go to the start of the buffer

        return StreamingResponse(img_byte_arr, media_type="image/png")

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions directly
        raise http_exc
    except Exception as e:
        print(f"Error during image generation endpoint processing: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.get("/")
async def root():
    """Basic root endpoint."""
    return {"message": "Welcome to LinkGenix API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
