# LinkGenix API Documentation

This document provides details about the available API endpoints for LinkGenix.

## Endpoints

### 1. Analyze PDF

*   **Method:** `POST`
*   **Path:** `/analyze-pdf/`
*   **Description:** Accepts a PDF file, converts each page into an image, analyzes the content of each page image using a multimodal AI model (Gemini Flash), and returns a combined textual description of the entire document.
*   **Input:**
    *   `file`: A PDF file uploaded as form data (`multipart/form-data`).
*   **Output:**
    *   **Success (200 OK):** JSON object containing the analysis.
        ```json
        {
          "analysis": "--- Page 1 ---\n[Description of page 1]...\n--- Page 2 ---\n[Description of page 2]...\n"
        }
        ```
    *   **Success (200 OK - No description):** JSON object indicating processing but no content generated.
        ```json
        {
          "message": "PDF processed, but no descriptions were generated.",
          "analysis": ""
        }
        ```
    *   **Error (400 Bad Request):** If the PDF has no pages or the file is invalid.
    *   **Error (404 Not Found):** If the temporary file is lost during processing.
    *   **Error (500 Internal Server Error):** If there's an issue saving the file, processing the PDF, or communicating with the AI model.
*   **Example Usage (curl):**
    ```bash
    curl -X POST "http://localhost:8000/analyze-pdf/" -F "file=@/path/to/your/document.pdf"
    ```

### 2. Generate Content

*   **Method:** `POST`
*   **Path:** `/generate-content/`
*   **Description:** Generates textual content (e.g., a LinkedIn post) based on a user-provided input string and a predefined system prompt (`content_prompt`). Uses a text generation model (Gemini Pro).
*   **Input:**
    *   Request Body: Plain text (`text/plain`) containing the user's prompt or instructions for content generation.
*   **Output:**
    *   **Success (200 OK):** JSON object containing the generated content.
        ```json
        {
          "generated_content": "This is the generated text based on your input..."
        }
        ```
    *   **Error (400 Bad Request):** If the input string is empty.
    *   **Error (500 Internal Server Error):** If the AI model fails to generate content or an unexpected error occurs.
*   **Example Usage (curl):**
    ```bash
    curl -X POST "http://localhost:8000/generate-content/" \
         -H "Content-Type: text/plain" \
         --data-binary "Create a LinkedIn post about the benefits of using AI for content creation."
    ```

### 3. Format Content

*   **Method:** `POST`
*   **Path:** `/format-content/`
*   **Description:** Takes raw text content and formats it according to a predefined formatting prompt (`formatting_prompt`) using a text generation model (Gemini Pro). This is useful for adding structure, markdown, or specific styling.
*   **Input:**
    *   Request Body: Plain text (`text/plain`) containing the raw content to be formatted.
*   **Output:**
    *   **Success (200 OK):** JSON object containing the formatted content.
        ```json
        {
          "formatted_content": "**Formatted Content**\n\n*   List item 1\n*   List item 2\n"
        }
        ```
    *   **Error (400 Bad Request):** If the input content string is empty.
    *   **Error (500 Internal Server Error):** If the AI model fails to format the content or an unexpected error occurs.
*   **Example Usage (curl):**
    ```bash
    curl -X POST "http://localhost:8000/format-content/" \
         -H "Content-Type: text/plain" \
         --data-binary "Here is some raw text that needs formatting. Add bullet points and bolding."
    ```

### 4. Optimize SEO

*   **Method:** `POST`
*   **Path:** `/optimize-seo/`
*   **Description:** Analyzes formatted text content and provides SEO (Search Engine Optimization) suggestions based on a predefined SEO prompt (`seo_prompt`) using a text generation model (Gemini Pro).
*   **Input:**
    *   Request Body: Plain text (`text/plain`) containing the formatted content to be analyzed for SEO.
*   **Output:**
    *   **Success (200 OK):** JSON object containing SEO suggestions.
        ```json
        {
          "seo_suggestions": "Suggestions:\n- Include keyword 'XYZ'.\n- Improve readability score.\n- Add relevant hashtags: #AI #ContentMarketing"
        }
        ```
    *   **Error (400 Bad Request):** If the input formatted content string is empty.
    *   **Error (500 Internal Server Error):** If the AI model fails to generate suggestions or an unexpected error occurs.
*   **Example Usage (curl):**
    ```bash
    curl -X POST "http://localhost:8000/optimize-seo/" \
         -H "Content-Type: text/plain" \
         --data-binary "**Formatted Post Title**\n\nThis is the body of the post..."
    ```

### 5. Generate Image

*   **Method:** `POST`
*   **Path:** `/generate-image/`
*   **Description:** First, generates an image generation prompt based on the input text using a text model (Gemini Pro) and a specific image prompt (`image_prompt`). Then, uses the generated prompt to create an image using an image generation model.
*   **Input:**
    *   Request Body: Plain text (`text/plain`) describing the desired image content or theme.
*   **Output:**
    *   **Success (200 OK):** A PNG image file streamed directly in the response body (`image/png`).
    *   **Error (400 Bad Request):** If the input text is empty.
    *   **Error (500 Internal Server Error):** If the image prompt generation fails, the image generation fails, or an unexpected error occurs.
*   **Example Usage (curl):**
    ```bash
    curl -X POST "http://localhost:8000/generate-image/" \
         -H "Content-Type: text/plain" \
         --data-binary "A futuristic cityscape at sunset with flying cars" \
         --output generated_image.png
    ```

### 6. Root

*   **Method:** `GET`
*   **Path:** `/`
*   **Description:** A simple root endpoint to check if the API is running.
*   **Input:** None
*   **Output:**
    *   **Success (200 OK):** JSON object with a welcome message.
        ```json
        {
          "message": "Welcome to LinkGenix API"
        }
        ```
*   **Example Usage (curl):**
    ```bash
    curl "http://localhost:8000/"
    ```
