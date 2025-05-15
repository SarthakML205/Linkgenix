import streamlit as st
import requests
import io
import os
import sys
from PIL import Image

# Add project root to sys.path to access modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import required prompts from the project
try:
    from src.core.prompts.planner_prompt import planning_prompt
    import config
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.error("Please make sure you're running this app from the project root.")
    st.stop()  # Stop execution if imports fail

# Set up the API URL
API_URL = "http://localhost:8000"  # Update this URL if your API is hosted elsewhere

def reset_session():
    """Clears relevant session state variables to start over."""
    keys_to_reset = [
        'user_query', 'pdf_analysis', 'generated_content',
        'formatted_content', 'seo_content', 'generated_image',
        'current_step'
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.current_step = 1

def main():
    st.set_page_config(
        page_title="LinkGenix - LinkedIn Content Generator",
        page_icon="🔗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state variables if they don't exist
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'user_query' not in st.session_state:
        st.session_state.user_query = ""
    if 'pdf_analysis' not in st.session_state:
        st.session_state.pdf_analysis = ""
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = ""
    if 'formatted_content' not in st.session_state:
        st.session_state.formatted_content = ""
    if 'seo_content' not in st.session_state:
        st.session_state.seo_content = ""

    # Sidebar for app info and progress tracking
    with st.sidebar:
        st.title("🔗 LinkGenix")
        st.markdown("AI-Powered LinkedIn Content Generation")
        st.divider()

        st.subheader("Workflow Progress")
        step1_done = bool(st.session_state.user_query)
        step2_done = bool(st.session_state.formatted_content)
        step3_done = bool(st.session_state.seo_content)

        step1_status = "✅" if st.session_state.current_step > 1 and step1_done else "🔄" if st.session_state.current_step == 1 else "⏱️"
        step2_status = "✅" if st.session_state.current_step > 2 and step2_done else "🔄" if st.session_state.current_step == 2 else "⏱️"
        step3_status = "✅" if st.session_state.current_step == 3 and step3_done else "🔄" if st.session_state.current_step == 3 else "⏱️"

        st.markdown(f"{step1_status} **Step 1:** Input & Analysis")
        st.markdown(f"{step2_status} **Step 2:** Generate & Format")
        st.markdown(f"{step3_status} **Step 3:** Optimize & Finalize")
        st.divider()

        # Reset button
        if st.button("🔄 Start Over", use_container_width=True):
            reset_session()
            st.rerun()

    # Main content area
    st.title("LinkedIn Content Generator")

    # Step 1: Input & PDF Analysis
    if st.session_state.current_step == 1:
        step1_input_and_analysis()

    # Step 2: Content Generation & Formatting
    elif st.session_state.current_step == 2:
        step2_generate_and_format()

    # Step 3: SEO Optimization & Finalization
    elif st.session_state.current_step == 3:
        step3_optimize_and_finalize()

def step1_input_and_analysis():
    st.header("Step 1: Input & Analysis")
    st.markdown("Provide your core idea and optionally upload a PDF for context.")

    # User query input
    st.subheader("🎯 What do you want to post about?")
    user_query = st.text_area(
        "Enter your topic, question, or draft idea:",
        value=st.session_state.user_query,
        height=100,
        placeholder="e.g., 'The future of AI in software development', 'Key takeaways from the latest tech conference', 'Tips for effective remote team management'"
    )
    st.session_state.user_query = user_query

    st.divider()

    # PDF upload
    st.subheader("📄 Upload Reference Document (Optional)")
    uploaded_file = st.file_uploader(
        "Upload a PDF containing relevant information (e.g., article, report, notes)",
        type="pdf"
    )

    col1, col2 = st.columns([1, 3])  # Adjust column ratio

    with col1:
        analyze_disabled = uploaded_file is None
        analyze_help = "Upload a PDF file first" if analyze_disabled else "Analyze the uploaded PDF for context"
        if st.button("🔍 Analyze PDF", disabled=analyze_disabled, help=analyze_help, use_container_width=True):
            if uploaded_file is not None:
                with st.spinner("Analyzing PDF... Please wait."):
                    try:
                        files = {"file": uploaded_file}
                        response = requests.post(f"{API_URL}/analyze-pdf/", files=files)

                        if response.status_code == 200:
                            pdf_analysis = response.json().get("analysis", "")
                            st.session_state.pdf_analysis = pdf_analysis
                            st.success("PDF analyzed successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error analyzing PDF: {response.status_code} - {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error during PDF analysis: {str(e)}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred during PDF analysis: {str(e)}")

    # Display analysis result if available
    if st.session_state.pdf_analysis:
        with st.expander("View PDF Analysis Result", expanded=True):
            st.text_area("Analysis:", value=st.session_state.pdf_analysis, height=200, disabled=True)

    st.divider()

    # Next step button
    next_disabled = not st.session_state.user_query
    next_help = "Please enter your post idea above before proceeding" if next_disabled else "Proceed to content generation"

    if st.button("➡️ Proceed to Generate Content", type="primary", disabled=next_disabled, help=next_help):
        st.session_state.current_step = 2
        st.rerun()

def step2_generate_and_format():
    st.header("Step 2: Generate & Format Content")
    st.markdown("Generate the initial post content based on your input and format it for LinkedIn.")

    col_back, col_title = st.columns([1, 6])
    with col_back:
        if st.button("⬅️ Back"):
            st.session_state.current_step = 1
            st.rerun()

    # Display user query and PDF analysis summary
    with st.expander("Review Input", expanded=False):
        st.info(f"**Your Query:** {st.session_state.user_query}")
        if st.session_state.pdf_analysis:
            st.success("**PDF Analysis Context:** Included")
        else:
            st.warning("**PDF Analysis Context:** Not provided or not analyzed.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        # Generate & Format Button
        generate_button_label = "✨ Generate & Format Content" if not st.session_state.formatted_content else "🔄 Regenerate & Format Content"
        if st.button(generate_button_label, use_container_width=True, type="primary"):
            with st.spinner("Generating and formatting content... This may take a moment."):
                try:
                    # 1. Generate Content
                    combined_input = f"User Intent:\n{st.session_state.user_query}\n\nReference Content:\n{st.session_state.pdf_analysis}"
                    gen_response = requests.post(
                        f"{API_URL}/generate-content/",
                        data=combined_input.encode('utf-8'),
                        headers={"Content-Type": "text/plain; charset=utf-8"}
                    )
                    gen_response.raise_for_status()

                    generated_content = gen_response.json().get("generated_content", "")
                    st.session_state.generated_content = generated_content

                    if not generated_content:
                        st.warning("Content generation resulted in empty output. Please try refining your query.")
                        st.stop()

                    # 2. Format Content
                    format_response = requests.post(
                        f"{API_URL}/format-content/",
                        data=generated_content.encode('utf-8'),
                        headers={"Content-Type": "text/plain; charset=utf-8"}
                    )
                    format_response.raise_for_status()

                    formatted_content = format_response.json().get("formatted_content", "")
                    st.session_state.formatted_content = formatted_content

                    st.success("Content generated and formatted successfully!")
                    st.rerun()

                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {str(e)}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    # Display formatted content in an editable text area
    if st.session_state.formatted_content:
        st.subheader("Formatted Content (Editable)")
        edited_formatted = st.text_area(
            "Review and edit the formatted content below:",
            value=st.session_state.formatted_content,
            height=350
        )
        if edited_formatted != st.session_state.formatted_content:
            st.session_state.formatted_content = edited_formatted

        st.divider()

        # Next step button (only if formatted content exists)
        with col2:
            if st.button("➡️ Proceed to SEO Optimization", use_container_width=True):
                if 'seo_content' in st.session_state:
                    del st.session_state.seo_content
                st.session_state.current_step = 3
                st.rerun()
    elif not st.session_state.generated_content:
        st.info("Click 'Generate & Format Content' to create your LinkedIn post.")

def step3_optimize_and_finalize():
    st.header("Step 3: Optimize & Finalize")
    st.markdown("Optimize your content for SEO (hashtags, keywords) and generate a complementary image.")

    col_back, col_title = st.columns([1, 6])
    with col_back:
        if st.button("⬅️ Back"):
            st.session_state.current_step = 2
            st.rerun()

    # Automatically trigger SEO optimization if not already done
    if not st.session_state.seo_content and st.session_state.formatted_content:
        with st.spinner("Optimizing content for SEO..."):
            try:
                response = requests.post(
                    f"{API_URL}/optimize-seo/",
                    data=st.session_state.formatted_content.encode('utf-8'),
                    headers={"Content-Type": "text/plain; charset=utf-8"}
                )
                response.raise_for_status()

                seo_content = response.json().get("seo_suggestions", "")
                st.session_state.seo_content = seo_content
                st.success("Content optimized for SEO!")
                st.rerun()

            except requests.exceptions.RequestException as e:
                st.error(f"Connection error during SEO optimization: {str(e)}")
                st.session_state.seo_content = st.session_state.formatted_content
                st.warning("Could not optimize for SEO. Displaying formatted content.")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred during SEO optimization: {str(e)}")
                st.session_state.seo_content = st.session_state.formatted_content
                st.warning("Could not optimize for SEO. Displaying formatted content.")
                st.rerun()

    # Display SEO optimized content
    if st.session_state.seo_content:
        st.subheader("🚀 SEO Optimized Content (Editable)")
        edited_seo = st.text_area(
            "Final review and edits for the optimized post:",
            value=st.session_state.seo_content,
            height=350
        )
        if edited_seo != st.session_state.seo_content:
            st.session_state.seo_content = edited_seo

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Re-optimize SEO", use_container_width=True):
                st.session_state.seo_content = ""
                st.rerun()

        with col2:
            st.download_button(
                label="📄 Download Post Text",
                data=st.session_state.seo_content,
                file_name="linkedin_post.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.divider()

        # Image generation section
        st.subheader("🖼️ Generate Complementary Image (Optional)")

        if 'generated_image' in st.session_state and st.session_state.generated_image:
            st.success("Image previously generated:")
            img_col1, img_col2 = st.columns([3, 1])
            with img_col1:
                try:
                    image = Image.open(io.BytesIO(st.session_state.generated_image))
                    st.image(image, caption="AI-Generated Image", use_column_width=True)
                except Exception as img_err:
                    st.error(f"Error displaying image: {img_err}")
            with img_col2:
                st.download_button(
                    label="📥 Download Image",
                    data=st.session_state.generated_image,
                    file_name="linkedin_post_image.png",
                    mime="image/png",
                    use_container_width=True
                )
                if st.button("🔄 Regenerate Image", use_container_width=True):
                    del st.session_state.generated_image
                    st.rerun()

        else:
            generate_image_button = st.button("🎨 Generate Image", help="Generate an image based on the post content")

            if generate_image_button:
                with st.spinner("Generating image... This can take some time."):
                    try:
                        combined_content = f"Original Query: {st.session_state.user_query}\n\nPost Content: {st.session_state.seo_content}"

                        image_response = requests.post(
                            f"{API_URL}/generate-image/",
                            data=combined_content.encode('utf-8'),
                            headers={"Content-Type": "text/plain; charset=utf-8"},
                            timeout=120
                        )
                        image_response.raise_for_status()

                        if image_response.content and image_response.headers.get('content-type', '').startswith('image/'):
                            st.session_state.generated_image = image_response.content
                            st.success("Image generated successfully!")
                            st.rerun()
                        else:
                            st.error(f"Image generation failed. Server response: {image_response.text}")

                    except requests.exceptions.Timeout:
                        st.error("Image generation timed out. The process took too long.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error during image generation: {str(e)}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred during image generation: {str(e)}")

        st.divider()
        st.success("🎉 Your LinkedIn post is ready!")
        st.info("You can download the text and image (if generated) using the buttons above.")

        if st.button("🚀 Start New Post", type="primary"):
            reset_session()
            st.rerun()

    elif st.session_state.formatted_content:
        st.info("Optimizing content for SEO...")
    else:
        st.warning("Formatted content not available. Please go back to Step 2.")

if __name__ == "__main__":
    main()
