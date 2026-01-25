# Development Guide

This guide provides detailed information for developers who want to understand, modify, or extend the AI-Powered Content Generator application.

## 📚 Table of Contents

- [Architecture](#architecture)
- [Core Components](#core-components)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)
- [Deployment](#deployment)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)

## 🏗️ Architecture

### High-Level Overview

```
User Interface (Streamlit)
        ↓
    app.py (Main Controller)
        ↓
    ┌───────┴───────┐
    ↓               ↓
scraper.py    templates.py
    ↓               ↓
OpenAI API   Content Generation
    ↓               ↓
    └───────┬───────┘
            ↓
    ┌───────┴───────┐
    ↓               ↓
pdf_generator.py  s3_uploader.py
```

### Data Flow

1. **User Input** → Company name + URL
2. **Web Scraping** → Fetch website content and links
3. **Link Analysis** → AI selects relevant pages (using cheaper model)
4. **Content Fetching** → Retrieve content from selected pages
5. **Content Generation** → AI generates content (using selected model)
6. **Export** → Markdown, PDF, or S3 upload

## 🧩 Core Components

### 1. app.py - Main Application

**Purpose**: Orchestrates the entire application flow and provides the UI.

**Key Functions**:

```python
def select_relevant_links(links, num_links=3, model="gpt-4o-mini")
```

- Analyzes scraped links using AI
- Returns most relevant links for content generation
- Uses cheaper model for cost optimization

```python
def fetch_page_and_relevant_links(url, model="gpt-4o-mini")
```

- Fetches main page content
- Selects and fetches relevant linked pages
- Combines all content for context

```python
def generate_content(company_name, url, template, model="gpt-4o")
```

- Generates content using selected template
- Streams response for better UX
- Returns full generated content

**State Management**:

- Uses `st.session_state` for storing generated content
- Maintains content across user interactions
- Enables download without re-generation

**UI Components**:

- Sidebar: Model selection, content type, advanced options
- Main area: Input fields, generate button, content display
- Export section: Download buttons, S3 upload

### 2. scraper.py - Web Scraping

**Purpose**: Fetches and parses website content.

**Key Functions**:

```python
def fetch_website_contents(url)
```

- Fetches HTML content from URL
- Extracts title and text
- Limits to 2000 characters
- Handles errors gracefully

```python
def fetch_website_links(url)
```

- Extracts all links from page
- Converts relative URLs to absolute
- Returns list of unique links

**Error Handling**:

- Timeout after 10 seconds
- User-agent spoofing to avoid blocking
- Graceful degradation on failure

**Limitations**:

- Maximum 2000 characters per page
- No JavaScript rendering
- Basic HTML parsing only

### 3. templates.py - Content Templates

**Purpose**: Defines content generation templates.

**Structure**:

```python
CONTENT_TEMPLATES = {
    "Template Name": {
        "description": "What this template does",
        "system_prompt": "AI behavior instructions",
        "user_prompt_template": "Template with {company_name} and {url}"
    }
}
```

**Current Templates**:

1. **Company Brochure** - Professional marketing material
2. **Humorous Brochure** - Entertaining, witty version
3. **Job Postings Summary** - Analysis of career opportunities
4. **Investment Pitch** - Investor-focused content
5. **Product Catalog** - Product listings and features
6. **Competitive Analysis** - Market positioning analysis
7. **Company Culture Report** - Values and work environment
8. **Technical Overview** - Developer-focused documentation
9. **Customer Success Stories** - Case studies and testimonials
10. **Executive Summary** - High-level strategic overview

**Helper Functions**:

```python
def create_custom_template(name, description, system_prompt, user_prompt)
```

- Create templates dynamically
- Useful for A/B testing
- Enables programmatic template creation

### 4. pdf_generator.py - PDF Creation

**Purpose**: Converts markdown content to PDF documents.

**Key Functions**:

```python
def markdown_to_pdf_content(markdown_text)
```

- Converts markdown to HTML
- Parses HTML to extract formatted elements
- Returns reportlab flowables

```python
def generate_pdf(content, company_name, filename)
```

- Creates PDF with custom styling
- Adds headers, dates, and formatting
- Handles lists, paragraphs, and headings

**Styling**:

- Custom paragraph styles
- Heading hierarchy (H1-H6)
- Bullet and numbered lists
- Professional layout

**Fallback**:

```python
def generate_simple_pdf(content, company_name, filename)
```

- Plain text PDF if markdown parsing fails
- Ensures PDFs always generate

### 5. s3_uploader.py - AWS S3 Integration

**Purpose**: Upload generated content to AWS S3.

**Key Functions**:

```python
def upload_to_s3(content, bucket_name, object_name, content_type='text/markdown')
```

- Main upload function
- Handles credentials automatically
- Returns S3 URL on success

```python
def upload_pdf_to_s3(pdf_bytes, bucket_name, object_name)
```

- Specialized PDF upload
- Handles binary content
- Sets correct content type

**Helper Functions**:

- `check_s3_access()` - Verify credentials
- `list_s3_objects()` - List bucket contents
- `create_s3_bucket()` - Create bucket if needed

**Authentication**:

- Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- AWS CLI credentials (~/.aws/credentials)
- IAM roles (for EC2/Lambda deployment)

## 🔧 Adding New Features

### Adding a New Content Template

1. **Edit templates.py**:

```python
CONTENT_TEMPLATES["Your Template Name"] = {
    "description": """
    Describe what this template generates and when to use it.
    """,
    "system_prompt": """
    You are an expert in [domain].
    Generate [type of content] that is [characteristics].
    Focus on [key aspects].
    """,
    "user_prompt_template": """
    Generate a {type of content} for {company_name}.
    Website: {url}

    Website Content:
    {content}

    Additional Instructions: [any specific guidance]
    """
}
```

2. **Test the template**:

```bash
streamlit run app.py
# Select your new template from the dropdown
```

3. **Iterate**:

- Test with different companies
- Refine prompts based on output
- Add example outputs to documentation

### Adding New Export Formats

1. **Create new export module** (e.g., `docx_generator.py`):

```python
from docx import Document

def generate_docx(content, company_name, filename):
    doc = Document()
    doc.add_heading(f'{company_name} - Content', 0)
    doc.add_paragraph(content)
    doc.save(filename)
    return filename
```

2. **Add to app.py**:

```python
import docx_generator

# In the export section:
if st.button("Download as DOCX"):
    docx_file = docx_generator.generate_docx(
        st.session_state.generated_content,
        company_name,
        "content.docx"
    )
    # Add download button
```

3. **Update requirements.txt**:

```
python-docx==0.8.11
```

### Adding Database Storage

1. **Create database module** (`database.py`):

```python
import sqlite3
from datetime import datetime

def save_content(company_name, url, template, content):
    conn = sqlite3.connect('content_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO content_history
        (company_name, url, template, content, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (company_name, url, template, content, datetime.now()))
    conn.commit()
    conn.close()

def get_content_history(company_name):
    conn = sqlite3.connect('content_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM content_history
        WHERE company_name = ?
        ORDER BY created_at DESC
    ''', (company_name,))
    results = cursor.fetchall()
    conn.close()
    return results
```

2. **Integrate in app.py**:

```python
import database

# After content generation:
database.save_content(company_name, url, content_type, generated_content)

# Add history viewer:
if st.checkbox("View History"):
    history = database.get_content_history(company_name)
    for item in history:
        st.write(item)
```

### Adding Caching

1. **Add Streamlit caching**:

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_website_contents(url):
    # existing implementation
    pass

@st.cache_data(ttl=3600)
def fetch_page_and_relevant_links(url, model="gpt-4o-mini"):
    # existing implementation
    pass
```

2. **Benefits**:

- Faster subsequent loads
- Reduced API calls
- Lower costs
- Better UX

## 🧪 Testing

### Manual Testing Checklist

- [ ] Test each content template
- [ ] Test with different model combinations
- [ ] Test PDF generation
- [ ] Test S3 upload (if configured)
- [ ] Test with various website URLs
- [ ] Test error handling (invalid URL, no API key, etc.)
- [ ] Test custom system prompts
- [ ] Test download buttons
- [ ] Test streaming display

### Automated Testing (Future)

Create `tests/test_scraper.py`:

```python
import pytest
from scraper import fetch_website_contents, validate_url

def test_fetch_website_success():
    content = fetch_website_contents("https://example.com")
    assert content is not None
    assert "title" in content
    assert "text" in content

def test_validate_url():
    assert validate_url("https://example.com") == True
    assert validate_url("not-a-url") == False
```

Run tests:

```bash
pytest tests/
```

## 🚀 Deployment

### Streamlit Cloud

1. **Prepare repository**:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Deploy**:

- Go to [share.streamlit.io](https://share.streamlit.io)
- Click "New app"
- Select your repository
- Choose `app.py` as main file
- Add secrets in settings:
  ```toml
  OPENAI_API_KEY = "sk-proj-..."
  AWS_ACCESS_KEY_ID = "..."
  AWS_SECRET_ACCESS_KEY = "..."
  ```

3. **Configure** (optional `.streamlit/config.toml`):

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
maxUploadSize = 200
enableXsrfProtection = true
```

### Docker Deployment

1. **Create Dockerfile**:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and run**:

```bash
docker build -t content-generator .
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="sk-proj-..." \
  content-generator
```

### AWS EC2 Deployment

1. **Launch EC2 instance** (t2.small or larger)

2. **SSH and setup**:

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="sk-proj-..."

# Run with nohup
nohup streamlit run app.py --server.port=8501 &
```

3. **Configure security group**: Allow inbound traffic on port 8501

## ⚡ Performance Optimization

### 1. Model Selection

**Cost vs Quality Trade-offs**:

| Model         | Input Cost | Output Cost | Speed     | Quality    |
| ------------- | ---------- | ----------- | --------- | ---------- |
| gpt-4o        | $5/1M      | $15/1M      | Medium    | Excellent  |
| gpt-4o-mini   | $0.15/1M   | $0.60/1M    | Fast      | Good       |
| gpt-3.5-turbo | $0.50/1M   | $1.50/1M    | Very Fast | Acceptable |

**Recommendations**:

- Link analysis: Always use `gpt-4o-mini`
- Simple content: Use `gpt-4o-mini`
- Complex content: Use `gpt-4o`
- Batch processing: Use `gpt-3.5-turbo`

### 2. Caching Strategy

```python
# Cache website content
@st.cache_data(ttl=3600)
def fetch_website_contents(url):
    pass

# Cache link analysis
@st.cache_data(ttl=3600)
def select_relevant_links(links, num_links, model):
    pass
```

### 3. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    def decorator(func):
        last_called = [0.0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = 60.0 / calls_per_minute
            if elapsed < wait_time:
                time.sleep(wait_time - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_minute=50)
def call_openai_api(*args, **kwargs):
    pass
```

## 🐛 Troubleshooting

### Common Development Issues

**1. Import Errors**

```python
# Problem: ModuleNotFoundError: No module named 'openai'
# Solution:
pip install -r requirements.txt
```

**2. OpenAI API Errors**

```python
# Problem: RateLimitError or AuthenticationError
# Solution: Check API key and usage limits
import openai
print(openai.api_key)  # Verify key is set
```

**3. Streamlit Cache Issues**

```python
# Problem: Stale cached data
# Solution: Clear cache
st.cache_data.clear()
# Or restart: Ctrl+C and rerun
```

**4. PDF Generation Issues**

```python
# Problem: PDF formatting breaks on special characters
# Solution: Add fallback in pdf_generator.py
try:
    # markdown parsing
except Exception as e:
    # use simple text PDF
    return generate_simple_pdf(content, company_name, filename)
```

### Debugging Tips

**1. Enable debug mode**:

```python
# Add to app.py
if st.checkbox("Debug Mode"):
    st.write("Debug Info:")
    st.write(f"API Key set: {bool(os.getenv('OPENAI_API_KEY'))}")
    st.write(f"Session state: {st.session_state}")
```

**2. Log API calls**:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# In generate_content():
logging.debug(f"Generating content with model: {model}")
logging.debug(f"System prompt: {system_prompt[:100]}...")
```

**3. Test components individually**:

```python
# Test scraper
python -c "from scraper import fetch_website_contents; print(fetch_website_contents('https://example.com'))"

# Test PDF generator
python -c "from pdf_generator import generate_pdf; generate_pdf('Test content', 'Test Co', 'test.pdf')"
```

## 📊 Monitoring

### Track Usage

```python
# Add to app.py
import json
from datetime import datetime

def log_usage(company_name, template, model, tokens_used):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "company": company_name,
        "template": template,
        "model": model,
        "tokens": tokens_used
    }
    with open("usage_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# After content generation:
log_usage(company_name, content_type, model, response.usage.total_tokens)
```

### Cost Tracking

```python
# Calculate costs
def calculate_cost(model, input_tokens, output_tokens):
    costs = {
        "gpt-4o": {"input": 5/1000000, "output": 15/1000000},
        "gpt-4o-mini": {"input": 0.15/1000000, "output": 0.60/1000000}
    }
    total = (input_tokens * costs[model]["input"] +
             output_tokens * costs[model]["output"])
    return round(total, 4)
```

## 🎯 Best Practices

1. **Always use environment variables** for sensitive data
2. **Implement error handling** at every external API call
3. **Add user feedback** for long-running operations
4. **Cache expensive operations** when possible
5. **Monitor API usage and costs** regularly
6. **Test with various inputs** before deploying
7. **Document new features** in README and this guide
8. **Use type hints** for better code maintainability
9. **Follow PEP 8** style guidelines
10. **Version control** all changes

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**Happy Developing! 🚀**
