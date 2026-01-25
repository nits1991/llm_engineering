# How to Import OpenAI API Collection into Postman

## Step 1: Import the Collection

1. **Open Postman**
2. **Click on "Import"** (top left corner)
3. **Select "File"** tab
4. **Choose the file**: `OpenAI_API_Postman_Collection.json`
5. **Click "Import"**

You should now see a new collection called "OpenAI API Collection" in your Postman sidebar.

## Step 2: Set Up Environment Variable

### Option A: Create an Environment (Recommended)

1. **Click on "Environments"** (left sidebar)
2. **Click "+ Create Environment"** or "+" button
3. **Name it**: `OpenAI Development` (or any name you like)
4. **Add a variable**:
   - Variable: `OPENAI_API_KEY`
   - Type: `secret` (this will hide your key)
   - Initial Value: `your-actual-api-key`
   - Current Value: `your-actual-api-key`
5. **Click "Save"**
6. **Select this environment** from the dropdown in the top right

### Option B: Quick Setup (Global Variable)

1. **Click on the collection** "OpenAI API Collection"
2. **Go to "Variables"** tab
3. **Find `OPENAI_API_KEY`**
4. **Replace `your-api-key-here`** with your actual API key
5. **Click "Save"**

## Step 3: Test the Collection

### Start with Simple Requests:

1. **Expand "Chat Completions"** folder
2. **Click "Basic Chat Completion"**
3. **Click "Send"**
4. **You should see a response!**

### Try Other Endpoints:

- **Models → List All Models** - No body required, just click Send
- **Moderations → Check Content Safety** - Quick and cheap to test
- **Embeddings → Create Embedding** - Returns vector embeddings

## Step 4: Understand the Structure

The collection is organized into folders:

```
OpenAI API Collection
├── Chat Completions
│   ├── Basic Chat Completion
│   ├── Chat with System Prompt
│   ├── Multi-turn Conversation
│   └── JSON Mode Response
├── Embeddings
│   ├── Create Embedding
│   └── Batch Embeddings
├── Images (DALL-E)
│   ├── Generate Image
│   └── Generate HD Image
├── Audio
│   ├── Text-to-Speech
│   ├── Text-to-Speech HD
│   ├── Speech-to-Text (Transcription)
│   └── Speech-to-Text (Translation)
├── Moderations
│   ├── Check Content Safety
│   └── Batch Moderation
└── Models
    ├── List All Models
    └── Get Model Details
```

## Step 5: Customize and Experiment

### Modify Parameters:

Each request has a body you can edit. Try changing:

**Chat Completions:**

- `model`: Try `gpt-4o`, `gpt-4o-mini`, or `gpt-3.5-turbo`
- `temperature`: 0.0 (focused) to 2.0 (creative)
- `max_tokens`: Control response length
- `messages`: Add your own prompts

**Images:**

- `prompt`: Describe any image you want
- `size`: `1024x1024`, `1792x1024`, or `1024x1792`
- `quality`: `standard` or `hd`

**Text-to-Speech:**

- `voice`: Try `alloy`, `echo`, `fable`, `onyx`, `nova`, or `shimmer`
- `input`: Any text you want spoken

### Save Your Variations:

1. **Right-click on any request**
2. **Select "Duplicate"**
3. **Rename it** (e.g., "My Custom Chat")
4. **Modify the parameters**
5. **Click "Save"**

## Step 6: Working with Special Endpoints

### For Text-to-Speech:

Instead of clicking "Send", use **"Send and Download"** button:

1. Click the **arrow next to "Send"**
2. Select **"Send and Download"**
3. Save the `.mp3` file to your computer
4. Open it with your audio player

### For Speech-to-Text:

1. Open **"Speech-to-Text (Transcription)"**
2. Go to **"Body"** tab
3. Click on **"form-data"**
4. Find the **"file"** field
5. Click **"Select Files"** and choose an audio file (mp3, wav, etc.)
6. Click **"Send"**

## Step 7: Monitor Your Usage

### In Each Response:

Look for the `usage` object to see token consumption:

```json
{
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 150,
    "total_tokens": 170
  }
}
```

### Cost Calculation:

For `gpt-4o-mini`:

- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

Example: 20 input + 150 output tokens ≈ $0.00012

## Common Issues and Solutions

### ❌ 401 Unauthorized

**Problem:** Invalid API key  
**Solution:** Check your API key in environment variables

### ❌ 400 Bad Request

**Problem:** Invalid model name or parameters  
**Solution:** Verify model name (use `gpt-4o-mini`, not `gpt-5-nano`)

### ❌ 429 Too Many Requests

**Problem:** Rate limit exceeded  
**Solution:** Wait a moment and try again, or check your rate limits

### ❌ 500 Internal Server Error

**Problem:** OpenAI service issue  
**Solution:** Wait and retry, check [OpenAI Status](https://status.openai.com)

## Pro Tips

### 1. Use Collections for Different Projects

Duplicate the collection for different projects with different settings.

### 2. Use Pre-request Scripts

Add scripts to generate timestamps, random data, etc.

### 3. Use Tests Tab

Add assertions to validate responses automatically:

```javascript
pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("Response has content", function () {
  var jsonData = pm.response.json();
  pm.expect(jsonData.choices[0].message.content).to.exist;
});
```

### 4. Save Responses as Examples

Right-click on a response → "Save as Example" to document expected outputs.

### 5. Use Variables for Dynamic Content

In request bodies, use `{{variable_name}}` to reference environment variables:

```json
{
  "model": "{{MODEL}}",
  "messages": [...]
}
```

## Next Steps

1. ✅ Import the collection
2. ✅ Set up your API key
3. ✅ Test basic endpoints
4. ✅ Read the API reference guide
5. ✅ Experiment with different parameters
6. ✅ Build your own requests
7. ✅ Create custom collections for your projects

## Resources

- **API Reference Guide:** `openai_api_reference.md`
- **OpenAI Documentation:** https://platform.openai.com/docs
- **Postman Learning:** https://learning.postman.com/
- **OpenAI Pricing:** https://openai.com/pricing
- **Rate Limits:** https://platform.openai.com/account/rate-limits

## Need Help?

- Check the `openai_api_reference.md` for detailed API documentation
- Visit OpenAI's official documentation
- Review the troubleshooting section above
- Test with simpler models first (gpt-4o-mini is cheapest)

Happy testing! 🚀
