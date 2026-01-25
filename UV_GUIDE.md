# UV Package Manager Guide

## What is UV?

UV is a blazingly fast Python package and project manager written in Rust. It's designed to replace pip, pip-tools, pipx, poetry, pyenv, virtualenv, and more - all in one tool.

### Key Benefits

- **Fast**: 10-100x faster than pip
- **Simple**: One tool for all Python package management
- **Reliable**: Deterministic dependency resolution
- **No Activation Needed**: UV automatically manages virtual environments

## Installation

```bash
# MacOS/Linux (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew
brew install uv

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, restart your terminal or run:

```bash
source $HOME/.cargo/env
```

## Core Concepts

1. **No Manual Activation**: Unlike traditional virtual environments, you don't need to activate anything
2. **Automatic Environment Management**: UV creates and manages `.venv` for you
3. **Lock Files**: `uv.lock` ensures reproducible installs across machines
4. **Project Configuration**: `pyproject.toml` defines your project dependencies

---

## Most Used Commands

### 1. Project Setup

```bash
# Sync dependencies from pyproject.toml (first time setup)
uv sync

# Update UV itself to latest version
uv self update
```

**Real-life example:**

```bash
# Clone a repo and set up environment
git clone https://github.com/user/project.git
cd project
uv sync  # Installs all dependencies automatically
```

---

### 2. Running Python Code

```bash
# Run a Python script
uv run python script.py

# Run a Python command
uv run python -c "print('Hello, World!')"

# Run Jupyter notebooks
uv run jupyter notebook

# Run a specific notebook
uv run jupyter notebook week1/day1.ipynb
```

**Real-life example:**

```bash
# Run the week1 day1 notebook
uv run jupyter notebook week1/day1.ipynb

# Run a scraper script
uv run python week1/scraper.py

# Run a Gradio app
uv run python app.py
```

---

### 3. Package Management

```bash
# Add a new package
uv add package-name

# Add a specific version
uv add "package-name==1.2.3"

# Add a development dependency
uv add --dev pytest

# Remove a package
uv remove package-name

# Update all packages
uv sync --upgrade
```

**Real-life examples:**

```bash
# Add OpenAI package
uv add openai

# Add multiple packages at once
uv add anthropic google-generativeai

# Add a dev tool for testing , --dev is used to specify development dependencies which means they are only needed during development and not in production environments and can be excluded from production installs.
uv add --dev pytest ipdb

# Remove an unused package
uv remove old-package
```

---

### 4. Python Version Management

```bash
# Install a specific Python version
uv python install 3.12

# Use a specific Python version for project
uv python pin 3.12

# List installed Python versions
uv python list
```

**Real-life example:**

```bash
# Ensure you're using Python 3.12
uv python install 3.12
uv python pin 3.12
uv sync  # Re-sync with correct Python version
```

---

### 5. Environment Information

```bash
# Show installed packages
uv pip list

# Show dependency tree
uv tree

# Check environment location
uv venv --help
```

---

## Real-World Workflow Examples

### Example 1: Starting a New Day's Work

```bash
# Navigate to project
cd ~/Documents/llm_learning_2025_bootcamp/llm_engineering

# Pull latest changes
git pull

# Sync any new dependencies
uv sync

# Start Jupyter
uv run jupyter notebook
```

### Example 2: Installing and Testing a New Package

```bash
# Add the package
uv add langchain-community

# Test it in a Python REPL
uv run python
>>> from langchain_community import something
>>> # Test your code
>>> exit()

# If it works, commit the changes to pyproject.toml
git add pyproject.toml uv.lock
git commit -m "Add langchain-community dependency"
```

### Example 3: Running Week-Specific Notebooks

```bash
# Week 1 - Web Scraper
uv run jupyter notebook week1/day1.ipynb

# Week 5 - RAG System
uv run jupyter notebook week5/day1.ipynb

# Week 8 - Agents
uv run python week8/price_is_right_final.py
```

### Example 4: Troubleshooting Dependencies

```bash
# Clear and reinstall everything
rm -rf .venv uv.lock
uv sync

# Or just update everything
uv sync --upgrade
```

### Example 5: Working with Scripts

```bash
# Run a Python script with UV
uv run python week1/scraper.py

# Run with arguments
uv run python script.py --input data.csv --output results.json

# Run a module
uv run python -m http.server 8000
```

---

## Comparison with Traditional Tools

| Task              | Traditional                       | UV                        |
| ----------------- | --------------------------------- | ------------------------- |
| Create venv       | `python -m venv .venv`            | Automatic                 |
| Activate venv     | `source .venv/bin/activate`       | Not needed                |
| Install packages  | `pip install package`             | `uv add package`          |
| Run script        | `python script.py`                | `uv run python script.py` |
| Freeze deps       | `pip freeze > requirements.txt`   | Automatic in `uv.lock`    |
| Install from file | `pip install -r requirements.txt` | `uv sync`                 |

---

## Important Tips

1. **Never manually activate .venv**: UV handles this automatically
2. **Always use `uv run`**: This ensures commands run in the correct environment
3. **Commit both files**: Always commit `pyproject.toml` AND `uv.lock`
4. **Use `uv sync`**: After pulling changes, run `uv sync` to update dependencies
5. **Check UV version**: Occasionally run `uv self update` for latest features

---

## Troubleshooting

### Command not found

```bash
# UV not in PATH - reload shell
source $HOME/.cargo/env

# Or add to your ~/.zshrc or ~/.bashrc
export PATH="$HOME/.cargo/bin:$PATH"
```

### Dependencies not found

```bash
# Resync dependencies
uv sync

# Force clean install
rm -rf .venv uv.lock
uv sync
```

### Python version issues

```bash
# Install required Python version
uv python install 3.12
uv python pin 3.12
uv sync
```

### Package conflicts

```bash
# Update all packages
uv sync --upgrade

# Or remove problematic package and re-add
uv remove problematic-package
uv add problematic-package
```

---

## Additional Resources

- Official UV Documentation: https://docs.astral.sh/uv/
- UV GitHub: https://github.com/astral-sh/uv
- Getting Started Guide: https://docs.astral.sh/uv/getting-started/

---

## Quick Reference Card

```bash
# Setup
uv sync                          # Install/sync all dependencies
uv self update                   # Update UV itself

# Running
uv run python script.py          # Run Python script
uv run jupyter notebook          # Start Jupyter

# Packages
uv add package-name              # Add package
uv remove package-name           # Remove package
uv pip list                      # List packages
uv tree                          # Show dependency tree

# Python
uv python install 3.12           # Install Python version
uv python list                   # List Python versions
```

---

**Remember**: With UV, you never need to manually activate virtual environments. Just use `uv run` before any Python command, and UV handles the rest!
