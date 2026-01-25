# Quick Start Guide

Get up and running with the AI-Powered Content Generator in 5 minutes!

## 📋 Prerequisites Check

Before starting, ensure you have:

- ✅ Python 3.8 or higher installed
- ✅ An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ✅ Terminal/Command Prompt access

## 🚀 5-Minute Setup

### Step 1: Navigate to Project Directory (30 seconds)

```bash
cd community-contributions/nitin_aggarwal_contributions
```

### Step 2: Install Dependencies (2 minutes)

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 3: Configure API Key (1 minute)

Create a `.env` file in the project directory:

```bash
# Option 1: Copy the example file
cp .env.example .env

# Option 2: Create manually
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### Step 4: Launch Application (30 seconds)

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`

If not, manually navigate to that URL.

### Step 5: Generate Your First Content (1 minute)

1. **Select Content Type**: Choose "Company Brochure (Professional)" from dropdown
2. **Choose Models**:
   - Link Analysis: gpt-4o-mini (recommended)
   - Content Generation: gpt-4o-mini (cheaper) or gpt-4o (better quality)
3. **Enter Details**:
   - Company Name: `Example Tech Inc.`
   - Website URL: `https://example.com`
4. **Click**: "Generate Content" button
5. **Wait**: 10-20 seconds for AI to generate content
6. **Download**: Click "Download as Markdown" or "Generate PDF"

## 🎯 What You Should See

### Expected Output

```
✅ Fetching website content...
✅ Analyzing relevant links...
✅ Fetching 3 relevant pages...
✅ Generating content with gpt-4o-mini...

[Streaming content appears here...]
```

### Success Indicators

- ✅ Content appears with typewriter effect
- ✅ Download buttons become active
- ✅ No error messages in red

## ❌ Troubleshooting Quick Fixes

### Problem 1: "No API key found"

```bash
# Verify .env file exists
ls -la .env

# Check content
cat .env

# Make sure it contains:
OPENAI_API_KEY=sk-proj-...
```

### Problem 2: "Module not found"

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep streamlit
pip list | grep openai
```

### Problem 3: "Port already in use"

```bash
# Use different port
streamlit run app.py --server.port=8502
```

### Problem 4: "Failed to fetch website"

- Try a different, well-known website (e.g., https://example.com)
- Check your internet connection
- Some websites block scrapers (this is normal)

## 💡 Quick Tips

### Save Money

- Use `gpt-4o-mini` for both models initially (~$0.001 per generation)
- Only use `gpt-4o` for important/complex content (~$0.01 per generation)

### Get Better Results

- Use descriptive company names
- Ensure website URLs are accessible
- Try different content types for variety
- Customize system prompts in Advanced Options

### Work Faster

- Keep the app running (no need to restart)
- Generate multiple versions quickly
- Download as Markdown for easy editing

## 📊 Cost Estimate

Typical generation costs:

- **Budget Mode** (gpt-4o-mini for both): ~$0.001/generation
- **Balanced Mode** (mini for links, gpt-4o for content): ~$0.008/generation
- **Quality Mode** (gpt-4o for both): ~$0.015/generation

With $5 of API credits, you can generate:

- 5,000+ brochures in Budget Mode
- 600+ brochures in Balanced Mode
- 300+ brochures in Quality Mode

## 🎓 Next Steps

Once you're comfortable with the basics:

1. **Explore Templates**: Try all 10 content types
2. **Customize Prompts**: Use Advanced Options to modify AI behavior
3. **Export Options**: Try PDF generation and S3 upload
4. **Add Templates**: Edit `templates.py` to add your own
5. **Read Documentation**: Check `README.md` and `DEVELOPMENT.md`

## 📚 Additional Resources

- **Full Documentation**: See `README.md`
- **Developer Guide**: See `DEVELOPMENT.md`
- **Example Output**: Check `examples/example_brochure.md`
- **OpenAI Docs**: https://platform.openai.com/docs
- **Streamlit Docs**: https://docs.streamlit.io

## 🆘 Still Having Issues?

1. Check the Troubleshooting section in `README.md`
2. Review error messages carefully
3. Ensure all prerequisites are met
4. Try with `example.com` first (known working URL)

## ✅ Verification Checklist

Before asking for help, verify:

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Dependencies installed (`pip list | grep streamlit`)
- [ ] .env file exists and contains valid API key
- [ ] Internet connection working
- [ ] Port 8501 available
- [ ] No error messages during startup

## 🎉 You're Ready!

If everything works, congratulations! You now have a powerful AI content generation tool at your fingertips.

Start experimenting with different:

- Content types
- Model combinations
- Company websites
- Custom prompts

**Happy generating! 🚀**

---

_Estimated total setup time: 5 minutes_  
_Estimated cost for first test: $0.001_
