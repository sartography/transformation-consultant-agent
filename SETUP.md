# Setup Guide

This guide covers both plugin mode and Python backup mode for the Transformation Consultant.

## Plugin Mode (Recommended)

Install as a Claude plugin for the simplest experience — no Python setup required.

```bash
claude plugins add knowledge-work-plugins/transformation-consultant
```

Once installed, use slash commands like `/transformation-consultant:full-transformation` directly in Claude Code or Claude Cowork. See [README.md](README.md) for command documentation.

---

## Python Backup Mode

The project also includes a standalone Python implementation. Use this for programmatic execution or when you need the pipeline's built-in retry logic and cost tracking.

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Step-by-Step Setup

### 1. Create Virtual Environment

**Windows:**
```bash
cd c:\Projects\transformation-consultant-agent\transformation-consultant-agent
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd /path/to/transformation-consultant-agent
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example configuration
cp config/.env.example config/.env

# Edit config/.env with your actual API keys
# You'll need:
# - ANTHROPIC_API_KEY from https://console.anthropic.com/
# - ELEVENLABS_API_KEY from https://elevenlabs.io/ (optional, for Phase 3)
```

**Windows users:** If `cp` doesn't work, manually copy the file:
```bash
copy config\.env.example config\.env
```

### 4. Verify Installation

```bash
# Test that Anthropic SDK is installed
python -c "import anthropic; print('Anthropic SDK installed successfully')"

# Test that Jupyter is installed
jupyter --version
```

### 5. Get Your Anthropic API Key

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to `config/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

### 6. Create Required Directories

```bash
# Create output directories if they don't exist
mkdir -p outputs/analysis
mkdir -p outputs/bpmn-diagrams
mkdir -p outputs/recommendations
mkdir -p outputs/voice-walkthroughs
```

**Windows users:**
```bash
mkdir outputs\analysis
mkdir outputs\bpmn-diagrams
mkdir outputs\recommendations
mkdir outputs\voice-walkthroughs
```

### 7. Launch Jupyter Notebook

```bash
jupyter notebook
```

This will open Jupyter in your browser. You can now create or open notebooks in the `notebooks/` directory.

## Next Steps

1. Test the transcript analysis skill - see `skills/transcript-analysis/README.md`
2. Create your first notebook: `notebooks/01-transcript-analysis-prototype.ipynb`
3. Run the skill against sample data

## Troubleshooting

### Issue: `pip install` fails

**Solution:** Upgrade pip first:
```bash
python -m pip install --upgrade pip
```

### Issue: Anthropic API import error

**Solution:** Ensure you're using the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Issue: API key not found

**Solution:** Make sure your `.env` file is in the `config/` directory and contains:
```
ANTHROPIC_API_KEY=your_actual_key_here
```

### Issue: Jupyter won't start

**Solution:** Try installing Jupyter explicitly:
```bash
pip install --upgrade jupyter notebook
```

## Environment Variables Reference

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key | None |
| `ELEVENLABS_API_KEY` | No (Phase 3) | ElevenLabs API key for voice | None |
| `DEFAULT_MODEL` | No | Claude model to use | claude-sonnet-4-5-20250929 |
| `MAX_TOKENS` | No | Default max tokens | 4000 |

## Verifying Your Setup

Run this test to verify everything is working:

```python
# test_setup.py
from pathlib import Path
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv("config/.env")

# Check API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ANTHROPIC_API_KEY not found in config/.env")
else:
    print("✓ ANTHROPIC_API_KEY found")

    # Test API connection
    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=100,
            messages=[{"role": "user", "content": "Hello, Claude!"}]
        )
        print("✓ Anthropic API connection successful")
        print(f"✓ Response: {response.content[0].text[:50]}...")
    except Exception as e:
        print(f"❌ API connection failed: {e}")

# Check required directories
required_dirs = [
    "skills/transcript-analysis",
    "outputs/analysis",
    "data/sample-transcripts"
]

for dir_path in required_dirs:
    if Path(dir_path).exists():
        print(f"✓ Directory exists: {dir_path}")
    else:
        print(f"❌ Directory missing: {dir_path}")

print("\n✅ Setup verification complete!")
```

Save this as `test_setup.py` and run:
```bash
python test_setup.py
```

## Ready to Go!

Your environment is now set up. Continue to:
- [Transcript Analysis Skill Documentation](skills/transcript-analysis/README.md)
- [Main README](README.md)
