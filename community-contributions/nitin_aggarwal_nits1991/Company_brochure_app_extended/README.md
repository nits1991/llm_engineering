# AI-Powered Content Generator

A flexible, customizable Streamlit application for generating various types of professional content using Large Language Models (LLMs). Built on concepts from the LLM Engineering Bootcamp Week 1 Day 5.

## 🌟 Features

### Core Capabilities

- **Multiple Content Types**: Generate 10+ different types of content including:
  - Company Brochures (Professional & Humorous)
  - Job Postings Summaries
  - Investment Pitches
  - Product Catalogs
  - Competitive Analysis
  - Company Culture Reports
  - Technical Overviews
  - Customer Success Stories
  - Executive Summaries

### Flexible AI Models

- Choose different models for link analysis (cheaper models recommended)
- Choose different models for content generation (quality vs. cost trade-off)
- Support for:
  - GPT-4o
  - GPT-4o-mini (recommended for cost-effectiveness)
  - GPT-4-turbo
  - GPT-3.5-turbo

### Advanced Features

- **Custom System Prompts**: Customize AI behavior for specific needs
- **PDF Export**: Download generated content as professionally formatted PDFs
- **S3 Upload**: Direct upload to AWS S3 buckets
- **Streaming Responses**: Real-time content generation with typewriter effect
- **Smart Link Analysis**: AI automatically identifies relevant pages to include
- **Template System**: Easily extensible with new content types

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- AWS credentials (optional, for S3 upload feature)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   cd community-contributions/nitin_aggarwal_contributions
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project directory:

   ```env
   OPENAI_API_KEY=sk-proj-your-api-key-here

   # Optional: AWS credentials for S3 upload
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_DEFAULT_REGION=us-east-1
   ```

   Alternatively, use AWS CLI to configure credentials:

   ```bash
   aws configure
   ```

## 🎯 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Application

1. **Select Content Type**: Choose from the dropdown menu
2. **Configure AI Models**:
   - Select model for link analysis (gpt-4o-mini recommended)
   - Select model for content generation
3. **Enter Company Details**:
   - Company name
   - Company website URL
4. **Generate Content**: Click the "Generate Content" button
5. **Export Options**:
   - Download as Markdown
   - Generate and download PDF
   - Upload to S3 (if configured)

### Advanced Options

Click "Advanced Options" in the sidebar to:

- Use custom system prompts
- Modify AI behavior
- Fine-tune output style

## 📁 Project Structure

```
nitin_aggarwal_contributions/
├── app.py                  # Main Streamlit application
├── scraper.py             # Web scraping utilities
├── templates.py           # Content templates library
├── pdf_generator.py       # PDF generation module
├── s3_uploader.py         # AWS S3 upload utilities
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── DEVELOPMENT.md        # Development guide
├── .env.example          # Environment variables template
└── examples/             # Example outputs
    ├── brochure_example.md
    └── brochure_example.pdf
```

## 🎨 Customization

### Adding New Content Templates

Edit `templates.py` and add a new template:

```python
"Your Template Name": {
    "description": """
    Description of what this template generates
    """,
    "system_prompt": """
    Instructions for the AI about how to generate content
    """,
    "user_prompt_template": """
    Template for user prompt with {company_name} and {url} placeholders
    """
}
```

### Modifying Scraper Behavior

Edit `scraper.py` to:

- Change maximum content length
- Add custom link filtering
- Modify request headers
- Handle specific website structures

### Customizing PDF Output

Edit `pdf_generator.py` to:

- Change PDF styling
- Modify page layout
- Add custom headers/footers
- Adjust fonts and colors

## 💡 Use Cases

### Business Applications

1. **Marketing Teams**

   - Generate company brochures for different audiences
   - Create product catalogs automatically
   - Develop customer success stories

2. **HR & Recruiting**

   - Analyze and summarize job postings
   - Create culture reports for candidates
   - Generate recruitment materials

3. **Sales & Business Development**

   - Create investment pitch materials
   - Generate competitive analysis reports
   - Develop executive summaries

4. **Product Teams**
   - Generate technical overviews
   - Create product documentation
   - Build feature comparison documents

## 🔧 Configuration Options

### Model Selection Guide

| Task              | Recommended Model | Why                                   |
| ----------------- | ----------------- | ------------------------------------- |
| Link Analysis     | gpt-4o-mini       | Fast, cheap, sufficient for this task |
| Simple Brochures  | gpt-4o-mini       | Cost-effective, good quality          |
| Complex Analysis  | gpt-4o            | Better reasoning, worth the cost      |
| Technical Content | gpt-4o            | Better accuracy for technical details |

### Cost Optimization Tips

1. Use `gpt-4o-mini` for link analysis (always)
2. Use `gpt-4o-mini` for simple content generation
3. Reserve `gpt-4o` for complex analysis and technical content
4. Limit page fetching to relevant pages only
5. Cache results when possible (future feature)

## 📊 Performance

- **Link Analysis**: ~2-5 seconds
- **Content Generation**: ~10-30 seconds (depends on model and content length)
- **PDF Generation**: ~1-3 seconds
- **S3 Upload**: ~1-2 seconds

## 🐛 Troubleshooting

### Common Issues

**1. API Key Not Found**

```
Error: No API key found
Solution: Check your .env file and ensure OPENAI_API_KEY is set
```

**2. Website Scraping Fails**

```
Error: Failed to fetch website
Solution: Some websites block scrapers. Try a different URL or check if the site is accessible
```

**3. PDF Generation Fails**

```
Error: PDF generation failed
Solution: Ensure reportlab is installed correctly: pip install reportlab
```

**4. S3 Upload Fails**

```
Error: AWS credentials not found
Solution: Configure AWS credentials using 'aws configure' or set environment variables
```

## 🔐 Security Notes

- **Never commit `.env` files** to version control
- **Rotate API keys regularly**
- **Use IAM roles** for S3 access in production
- **Set spending limits** on your OpenAI account
- **Monitor API usage** regularly

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets (API keys) in Streamlit Cloud settings
5. Deploy!

### Deploy to AWS/GCP/Azure

See `DEVELOPMENT.md` for detailed deployment instructions.

## 📈 Future Enhancements

- [ ] Add caching for website content
- [ ] Support for multiple websites comparison
- [ ] Batch processing multiple companies
- [ ] Custom branding for PDFs
- [ ] Email delivery of generated content
- [ ] API endpoint for programmatic access
- [ ] Database integration for content storage
- [ ] User authentication and content history
- [ ] A/B testing different prompts
- [ ] Analytics dashboard

## 🤝 Contributing

This is a community contribution project! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## 📝 License

This project is part of the LLM Engineering Bootcamp community contributions.
Feel free to use, modify, and distribute as needed.

## 👤 Author

**Nitin Aggarwal**

- Based on: LLM Engineering Bootcamp Week 1 Day 5
- Instructor: Ed Donner

## 🙏 Acknowledgments

- Ed Donner for the excellent LLM Engineering Bootcamp
- OpenAI for the powerful GPT models
- Streamlit for the amazing web framework
- The LLM Engineering Bootcamp community

## 📧 Support

For questions or issues:

1. Check the troubleshooting section above
2. Review `DEVELOPMENT.md` for technical details
3. Contact the course instructor or community

## 🎓 Learning Resources

- [LLM Engineering Bootcamp](https://edwarddonner.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)

---

**Happy Content Generating! 🚀**
