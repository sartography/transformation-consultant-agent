"""
Setup Verification Script
Run this script to verify your development environment is configured correctly.
Validates both the Anthropic plugin structure and the Python backup mode.
"""

from pathlib import Path
import os
import sys
import json

# Handle Unicode on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_plugin_structure():
    """Test that the Anthropic plugin structure is correct."""
    print("\nChecking plugin structure...")

    required_files = [
        ".claude-plugin/plugin.json",
        ".mcp.json",
        "commands/analyze-transcript.md",
        "commands/generate-bpmn.md",
        "commands/optimize-process.md",
        "commands/full-transformation.md",
        "skills/transcript-analysis/SKILL.md",
        "skills/bpmn-generation/SKILL.md",
        "skills/process-optimization/SKILL.md",
        "CONNECTORS.md",
        "LICENSE",
    ]

    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  \u2713 {file_path}")
        else:
            print(f"  \u274c {file_path} - file missing")
            all_exist = False

    # Validate plugin.json content
    plugin_json = Path(".claude-plugin/plugin.json")
    if plugin_json.exists():
        try:
            data = json.loads(plugin_json.read_text(encoding="utf-8"))
            for field in ["name", "version", "description", "author"]:
                if field in data:
                    print(f"  \u2713 plugin.json has '{field}': {str(data[field])[:50]}")
                else:
                    print(f"  \u274c plugin.json missing '{field}'")
                    all_exist = False
        except json.JSONDecodeError as e:
            print(f"  \u274c plugin.json is invalid JSON: {e}")
            all_exist = False

    # Validate .mcp.json content
    mcp_json = Path(".mcp.json")
    if mcp_json.exists():
        try:
            data = json.loads(mcp_json.read_text(encoding="utf-8"))
            if "mcpServers" in data:
                print(f"  \u2713 .mcp.json has 'mcpServers' with {len(data['mcpServers'])} connector(s)")
            else:
                print(f"  \u274c .mcp.json missing 'mcpServers'")
                all_exist = False
        except json.JSONDecodeError as e:
            print(f"  \u274c .mcp.json is invalid JSON: {e}")
            all_exist = False

    return all_exist


def test_imports():
    """Test that required packages can be imported."""
    print("\nTesting package imports...")

    try:
        import anthropic
        print("  \u2713 anthropic")
    except ImportError:
        print("  \u274c anthropic - run: pip install anthropic")
        return False

    try:
        import dotenv
        print("  \u2713 python-dotenv")
    except ImportError:
        print("  \u274c python-dotenv - run: pip install python-dotenv")
        return False

    try:
        import jupyter
        print("  \u2713 jupyter")
    except ImportError:
        print("  \u274c jupyter - run: pip install jupyter")
        return False

    return True

def test_env_file():
    """Test that .env file exists and has required variables."""
    print("\nChecking environment configuration...")

    env_path = Path("config/.env")
    if not env_path.exists():
        print("  \u274c config/.env file not found")
        print("     Run: copy config\\.env.example config\\.env")
        return False

    print("  \u2713 config/.env file exists")

    # Try loading environment variables
    from dotenv import load_dotenv
    load_dotenv(env_path)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_anthropic_api_key_here":
        print("  \u26a0 ANTHROPIC_API_KEY not set or using placeholder")
        print("     Edit config/.env and add your API key from https://console.anthropic.com/")
        return False

    print("  \u2713 ANTHROPIC_API_KEY is set")
    return True

def test_api_connection():
    """Test connection to Anthropic API."""
    print("\nTesting API connection...")

    from dotenv import load_dotenv
    from anthropic import Anthropic

    load_dotenv("config/.env")
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "your_anthropic_api_key_here":
        print("  \u26a0 Skipping API test (no valid API key)")
        return None

    try:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=100,
            messages=[{"role": "user", "content": "Hello, Claude! Respond with just 'API test successful'."}]
        )
        print("  \u2713 API connection successful")
        print(f"  \u2713 Response: {response.content[0].text[:60]}...")
        return True
    except Exception as e:
        print(f"  \u274c API connection failed: {e}")
        return False

def test_directories():
    """Test that required directories exist."""
    print("\nChecking directory structure...")

    required_dirs = [
        ".claude-plugin",
        "commands",
        "skills/transcript-analysis",
        "skills/transcript-analysis/domain-knowledge",
        "skills/bpmn-generation",
        "skills/bpmn-generation/domain-knowledge",
        "skills/process-optimization",
        "skills/process-optimization/domain-knowledge",
        "data/sample-transcripts",
        "outputs/analysis",
        "outputs/bpmn-diagrams",
        "outputs/recommendations",
        "notebooks",
        "config"
    ]

    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  \u2713 {dir_path}")
        else:
            print(f"  \u274c {dir_path} - directory missing")
            all_exist = False

    return all_exist

def test_skill_files():
    """Test that skill and domain knowledge files exist."""
    print("\nChecking skill files...")

    required_files = [
        "skills/transcript-analysis/SKILL.md",
        "skills/transcript-analysis/README.md",
        "skills/transcript-analysis/domain-knowledge/example-01-ap-transcript.txt",
        "skills/transcript-analysis/domain-knowledge/example-01-ap-analysis.md",
        "skills/bpmn-generation/SKILL.md",
        "skills/bpmn-generation/domain-knowledge/apqc-activities.md",
        "skills/process-optimization/SKILL.md",
        "skills/process-optimization/domain-knowledge/example-01-ap-recommendations.md",
    ]

    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  \u2713 {file_path}")
        else:
            print(f"  \u274c {file_path} - file missing")
            all_exist = False

    return all_exist

def main():
    """Run all verification tests."""
    print("=" * 70)
    print("TRANSFORMATION CONSULTANT - SETUP VERIFICATION")
    print("=" * 70)

    # Change to project root if we're not already there
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    results = {
        "plugin_structure": test_plugin_structure(),
        "directories": test_directories(),
        "skill_files": test_skill_files(),
        "imports": test_imports(),
        "env": test_env_file(),
    }

    # API test is optional if no key is set
    api_result = test_api_connection()
    if api_result is not None:
        results["api"] = api_result

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for v in results.values() if v is True)
    total = len(results)

    for test_name, result in results.items():
        status = "\u2713 PASS" if result else "\u274c FAIL"
        print(f"{status}: {test_name}")

    print(f"\n{passed}/{total} tests passed")

    if all(results.values()):
        print("\n\u2705 All tests passed! Your environment is ready.")
        print("\nPlugin mode:")
        print("  Use /transformation-consultant:full-transformation in Claude")
        print("\nPython backup mode:")
        print("  python -m src.main data/sample-transcripts/ap-process.txt outputs/test")
        return 0
    else:
        print("\n\u26a0 Some tests failed. Please fix the issues above and run again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
