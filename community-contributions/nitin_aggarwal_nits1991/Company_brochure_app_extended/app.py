"""
AI-Powered Content Generator - Streamlit Application
====================================================

A flexible, customizable application for generating various types of content
using LLMs, including company brochures, job postings, and more.

Author: Nitin Aggarwal
Based on: LLM Engineering Bootcamp Week 1 Day 5
"""

import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from io import BytesIO
from datetime import datetime

# Import custom modules
from scraper import fetch_website_links, fetch_website_contents
from pdf_generator import generate_pdf
from templates import CONTENT_TEMPLATES
from s3_uploader import upload_to_s3

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Content Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2ca02c;
        margin-top: 2rem;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
if 'company_url' not in st.session_state:
    st.session_state.company_url = ""


def initialize_openai():
    """Initialize OpenAI client with API key"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error(
            "❌ OpenAI API key not found! Please set OPENAI_API_KEY in your .env file")
        st.stop()
    return OpenAI(api_key=api_key)


def select_relevant_links(url, model, openai_client):
    """Use LLM to select relevant links from a webpage"""
    with st.spinner(f"🔍 Analyzing links on {url} using {model}..."):
        link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""

        links = fetch_website_links(url)
        user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company, 
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

{chr(10).join(links)}
"""

        try:
            response = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": link_system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            result = response.choices[0].message.content
            links_data = json.loads(result)
            st.success(
                f"✅ Found {len(links_data.get('links', []))} relevant links")
            return links_data
        except Exception as e:
            st.error(f"❌ Error selecting links: {str(e)}")
            return {"links": []}


def fetch_page_and_relevant_links(url, model, openai_client):
    """Fetch main page content and all relevant linked pages"""
    with st.spinner("📄 Fetching page contents..."):
        contents = fetch_website_contents(url)
        relevant_links = select_relevant_links(url, model, openai_client)

        result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"

        for link in relevant_links.get('links', []):
            try:
                result += f"\n\n### Link: {link['type']}\n"
                result += fetch_website_contents(link["url"])
            except Exception as e:
                st.warning(
                    f"⚠️ Could not fetch {link.get('type', 'link')}: {str(e)}")

        return result


def generate_content(company_name, url, content_type, model, openai_client, custom_prompt=None):
    """Generate content based on template and inputs"""

    # Get template
    template = CONTENT_TEMPLATES.get(
        content_type, CONTENT_TEMPLATES["Company Brochure"])

    # Use custom prompt if provided
    system_prompt = custom_prompt if custom_prompt else template["system_prompt"]

    # Build user prompt
    user_prompt = template["user_prompt_template"].format(
        company_name=company_name,
        url=url
    )

    # Add page contents
    user_prompt += fetch_page_and_relevant_links(url, model, openai_client)
    user_prompt = user_prompt[:10_000]  # Truncate if too long

    # Generate content with streaming
    with st.spinner(f"✨ Generating {content_type.lower()} using {model}..."):
        stream = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=True
        )

        response = ""
        content_placeholder = st.empty()

        for chunk in stream:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                content_placeholder.markdown(response)

        return response


def main():
    """Main application"""

    # Header
    st.markdown('<h1 class="main-header">🤖 AI-Powered Content Generator</h1>',
                unsafe_allow_html=True)
    st.markdown(
        "Generate professional content using AI - from company brochures to job postings and more!")

    # Initialize OpenAI
    openai_client = initialize_openai()

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Content Type Selection
        content_type = st.selectbox(
            "📝 Content Type",
            list(CONTENT_TEMPLATES.keys()),
            help="Select the type of content you want to generate"
        )

        st.markdown("---")

        # Model Selection
        st.subheader("🧠 AI Models")

        link_model = st.selectbox(
            "Link Analysis Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            index=0,
            help="Model for analyzing and selecting relevant links (cheaper model recommended)"
        )

        content_model = st.selectbox(
            "Content Generation Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0,
            help="Model for generating the final content"
        )

        st.markdown("---")

        # Advanced Options
        with st.expander("🔧 Advanced Options"):
            use_custom_prompt = st.checkbox("Use Custom System Prompt")

            if use_custom_prompt:
                custom_prompt = st.text_area(
                    "Custom System Prompt",
                    value=CONTENT_TEMPLATES[content_type]["system_prompt"],
                    height=200,
                    help="Customize the AI's behavior and output style"
                )
            else:
                custom_prompt = None

        st.markdown("---")

        # Export Options
        st.subheader("📤 Export Options")
        export_format = st.radio(
            "Format",
            ["Markdown", "PDF"],
            help="Choose output format"
        )

        # S3 Upload Option
        enable_s3 = st.checkbox(
            "Enable S3 Upload", help="Upload generated content to AWS S3")

        if enable_s3:
            s3_bucket = st.text_input(
                "S3 Bucket Name", help="Your AWS S3 bucket name")
            s3_prefix = st.text_input(
                "S3 Prefix (optional)", value="ai-content/")

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 📋 Input Details")
        st.markdown('</div>', unsafe_allow_html=True)

        company_name = st.text_input(
            "Company Name",
            value=st.session_state.company_name,
            placeholder="e.g., HuggingFace",
            help="Enter the company name"
        )

        company_url = st.text_input(
            "Company Website URL",
            value=st.session_state.company_url,
            placeholder="https://example.com",
            help="Enter the full URL including https://"
        )

        # Update session state
        st.session_state.company_name = company_name
        st.session_state.company_url = company_url

        # Generate button
        generate_button = st.button(
            "🚀 Generate Content", type="primary", use_container_width=True)

    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### ℹ️ Template Info")
        st.markdown(CONTENT_TEMPLATES[content_type]["description"])
        st.markdown('</div>', unsafe_allow_html=True)

    # Generate content
    if generate_button:
        if not company_name or not company_url:
            st.error("❌ Please provide both company name and URL")
        elif not company_url.startswith("http"):
            st.error("❌ URL must start with http:// or https://")
        else:
            try:
                # Generate content
                content = generate_content(
                    company_name,
                    company_url,
                    content_type,
                    content_model,
                    openai_client,
                    custom_prompt if use_custom_prompt else None
                )

                st.session_state.generated_content = content

                st.markdown('<div class="success-box">',
                            unsafe_allow_html=True)
                st.markdown("### ✅ Content Generated Successfully!")
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error generating content: {str(e)}")

    # Display and export generated content
    if st.session_state.generated_content:
        st.markdown("---")
        st.markdown('<h2 class="sub-header">📄 Generated Content</h2>',
                    unsafe_allow_html=True)

        # Display content
        st.markdown(st.session_state.generated_content)

        st.markdown("---")

        # Export options
        col1, col2, col3 = st.columns(3)

        with col1:
            # Download as Markdown
            st.download_button(
                label="⬇️ Download Markdown",
                data=st.session_state.generated_content,
                file_name=f"{company_name.replace(' ', '_')}_{content_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )

        with col2:
            # Download as PDF
            if export_format == "PDF" or st.button("⬇️ Generate & Download PDF"):
                try:
                    pdf_bytes = generate_pdf(
                        st.session_state.generated_content,
                        title=f"{company_name} - {content_type}",
                        company_name=company_name
                    )

                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_bytes,
                        file_name=f"{company_name.replace(' ', '_')}_{content_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")

        with col3:
            # Upload to S3
            if enable_s3 and s3_bucket:
                if st.button("☁️ Upload to S3"):
                    try:
                        file_key = f"{s3_prefix}{company_name.replace(' ', '_')}_{content_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"

                        with st.spinner("Uploading to S3..."):
                            s3_url = upload_to_s3(
                                st.session_state.generated_content,
                                s3_bucket,
                                file_key
                            )

                        st.success(f"✅ Uploaded successfully!")
                        st.code(s3_url, language=None)
                    except Exception as e:
                        st.error(f"❌ Error uploading to S3: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit and OpenAI | Based on LLM Engineering Bootcamp</p>
        <p>💡 <strong>Tip:</strong> Try different content types and models to see varied results!</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
