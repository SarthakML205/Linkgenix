# LinkGenix User Guide

Welcome to LinkGenix! This guide will help you set up and use the application to generate engaging LinkedIn content.

## 1. Introduction

LinkGenix is an AI-powered tool designed to assist users in creating professional and engaging LinkedIn posts. It leverages AI models to analyze input (text or PDF documents), generate content drafts, format them for LinkedIn, optimize them with relevant keywords and hashtags, and even generate complementary images.

## 2. Getting Started

### Prerequisites

*   Python 3.8 or higher installed.
*   `pip` (Python package installer).
*   Git (for cloning the repository).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd LinkGenix
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure API Keys:**
    *   Rename the `.env.example` file (if provided) to `.env` or create a new `.env` file in the project root (`d:\LinkGenix`).
    *   Add your API keys to the `.env` file:
        ```
        GOOGLE_API_KEY=your_google_api_key_here
        HF_TOKEN=your_huggingface_token_here
        ```
    *   Ensure the `config.py` file correctly loads these keys.

### Running the Application

LinkGenix consists of a backend API and a frontend web application. You need to run both.

1.  **Run the Backend API:**
    Open a terminal in the project root (`d:\LinkGenix`) and run:
    ```bash
    python src/api/server.py
    ```
    The API will start, usually at `http://localhost:8000`. Keep this terminal running.

2.  **Run the Frontend Application:**
    Open a *second* terminal in the project root (`d:\LinkGenix`) and run:
    ```bash
    streamlit run frontend/app.py
    ```
    This will open the LinkGenix web interface in your browser, usually at `http://localhost:8501`.

## 3. Using the LinkGenix Web App

The Streamlit application guides you through a step-by-step process to create your LinkedIn post.

### Sidebar

*   **Workflow Progress:** Tracks your current step in the content creation process.
*   **Start Over:** Resets the application state, allowing you to begin a new post from scratch.

### Step 1: Input & Analysis

1.  **What do you want to post about?:** Enter your core idea, topic, question, or even a rough draft in the text area. This is the primary input for content generation.
2.  **Upload Reference Document (Optional):** You can upload a PDF file (e.g., an article, report, notes) that contains relevant background information.
3.  **Analyze PDF:** If you uploaded a PDF, click this button. The backend API will process the PDF, extract text content from each page using AI vision, and display a summary in the "View PDF Analysis Result" expander. This analysis provides context for the content generation step.
4.  **Proceed to Generate Content:** Once you've entered your query (and optionally analyzed a PDF), click this button to move to the next step.

### Step 2: Generate & Format Content

1.  **Review Input:** You can expand this section to see the query and PDF analysis context being used.
2.  **Generate & Format Content:** Click this button. The application sends your query and the PDF analysis (if available) to the backend.
    *   The backend first generates an initial draft of the LinkedIn post using the `content_creation_prompt`.
    *   Then, it formats this draft according to the `formatting_prompt` (adding structure, emojis, placeholders).
3.  **Formatted Content (Editable):** The generated and formatted post appears in a text area. You can review and make any necessary edits here.
4.  **Proceed to SEO Optimization:** After reviewing/editing the formatted content, click this button.

### Step 3: Optimize & Finalize

1.  **SEO Optimization:** The application automatically sends the formatted content to the backend to be optimized based on the `seo_prompt`. This usually involves refining keywords, checking structure, and adding relevant hashtags.
2.  **SEO Optimized Content (Editable):** The final, optimized version of your post is displayed. You can make final edits here.
3.  **Re-optimize SEO:** If you make significant changes, you can click this button to run the SEO optimization process again on the edited text.
4.  **Download Post Text:** Save the final post content as a text file.
5.  **Generate Complementary Image (Optional):**
    *   Click **Generate Image**. The application sends the post content to the backend.
    *   The backend first generates a suitable *prompt* for an image generation model based on your post content using `image_prompt`.
    *   It then uses this generated prompt to create an image using the configured image generation service (Hugging Face Inference API in this setup).
    *   The generated image will be displayed.
    *   **Download Image:** Save the generated image as a PNG file.
    *   **Regenerate Image:** If you're not satisfied, you can generate a new image.
6.  **Start New Post:** Once finished, click this button to reset the app and start creating another post.

## 4. API Usage

LinkGenix also exposes its functionalities through a REST API. Developers can interact with the API endpoints directly for more custom integrations. For detailed information on the available endpoints, request/response formats, and usage examples, please refer to the [API Documentation](./api_docs.md).

## 5. Configuration

Key configuration settings, such as API keys and default model names, are managed in the `config.py` file and loaded from the `.env` file located in the project root (`d:\LinkGenix`). Ensure your API keys are correctly set in the `.env` file for the application to function properly.
