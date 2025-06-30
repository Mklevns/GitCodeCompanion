# Multi-LLM Code Quality Pipeline

A sophisticated GitHub-integrated code analysis system that leverages four different Large Language Models in a sequential "gauntlet" approach to provide comprehensive code quality assessment, bug detection, security analysis, and improvement suggestions.

## Overview

This pipeline orchestrates Gemini, ChatGPT, Claude, and DeepSeek in a four-stage process where each AI specializes in different aspects of code quality:

- **Stage 1 - Gemini Analysis**: Deep code analysis for bugs, performance issues, and security vulnerabilities
- **Stage 2 - ChatGPT Generation**: Code improvement and fix generation based on analysis
- **Stage 3 - Claude Integration**: Seamless integration of improvements with existing codebase
- **Stage 4 - DeepSeek Verification**: Final verification and quality assurance

## Features

- **Multi-LLM Architecture**: Combines strengths of four leading AI models
- **GitHub Integration**: Automatically triggers on pull requests
- **Security-First Design**: Input sanitization and prompt injection protection
- **Comprehensive Reporting**: Detailed analysis and improvement recommendations
- **Demo Mode**: Test functionality without GitHub repository

## Quick Start

### 1. Environment Setup

Set the following environment variables:

```bash
# Required API Keys
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key" 
export GEMINI_API_KEY="your_gemini_api_key"
export DEEPSEEK_API_KEY="your_deepseek_api_key"

# For GitHub integration
export GITHUB_TOKEN="your_github_token"
export REPOSITORY="owner/repo-name"
export PR_NUMBER="pull_request_number"
```

### 2. Demo Mode

Test the pipeline with sample code:

```bash
python demo_mode.py
```

### 3. GitHub Action Integration

Add to `.github/workflows/multi-llm-pipeline.yml`:

```yaml
name: Multi-LLM Code Quality Pipeline

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main, master, develop]

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  code-quality-pipeline:
    runs-on: ubuntu-latest
    name: Multi-LLM Code Analysis Pipeline
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        token: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests PyGithub python-dotenv openai anthropic google-genai
    
    - name: Run Multi-LLM Pipeline
      uses: ./
      with:
        github-token: ${{ secrets.GITHUB_TOKEN }}
        gemini-api-key: ${{ secrets.GEMINI_API_KEY }}
        openai-api-key: ${{ secrets.OPENAI_API_KEY }}
        anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
        deepseek-api-key: ${{ secrets.DEEPSEEK_API_KEY }}
        pr-number: ${{ github.event.pull_request.number }}
        repository: ${{ github.repository }}
```

## API Keys Setup

### OpenAI
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Add to GitHub secrets as `OPENAI_API_KEY`

### Anthropic (Claude)
1. Visit https://console.anthropic.com/
2. Create an API key
3. Add to GitHub secrets as `ANTHROPIC_API_KEY`

### Google Gemini
1. Visit https://aistudio.google.com/apikey
2. Generate an API key
3. Add to GitHub secrets as `GEMINI_API_KEY`

### DeepSeek
1. Visit https://platform.deepseek.com/api_keys
2. Create an API key
3. Add to GitHub secrets as `DEEPSEEK_API_KEY`

### GitHub Token
1. Go to https://github.com/settings/tokens
2. Create a Personal Access Token with `repo` permissions
3. Add to GitHub secrets as `GITHUB_TOKEN`

## Architecture

### Core Components

- **Main Orchestrator** (`main.py`): Central pipeline coordinator
- **LLM Clients** (`llm_clients.py`): Unified interface for all AI providers
- **Pipeline Stages** (`pipeline_stages.py`): Four-stage analysis implementation
- **GitHub Integration** (`github_utils.py`): Pull request management
- **Security Layer** (`security_utils.py`): Input sanitization and security
- **Report Generator** (`report_generator.py`): Comprehensive reporting

### Data Flow

1. GitHub webhook triggers on PR creation/update
2. Pipeline extracts changed code files
3. Stage 1: Gemini performs comprehensive analysis
4. Stage 2: ChatGPT generates improvements
5. Stage 3: Claude integrates changes seamlessly
6. Stage 4: DeepSeek performs final verification
7. Comprehensive report posted to PR

## Supported Languages

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C++ (.cpp)
- C (.c)
- C# (.cs)
- Go (.go)
- Rust (.rs)
- PHP (.php)
- Ruby (.rb)
- Swift (.swift)
- Kotlin (.kt)
- And more...

## Security Features

- Input sanitization for all code
- Prompt injection protection
- Rate limiting for API calls
- Sensitive data masking
- Path traversal prevention

## Example Output

The pipeline generates detailed reports including:

- Issue identification and severity assessment
- Performance optimization suggestions
- Security vulnerability analysis
- Code quality improvements
- Integration notes and compatibility checks
- Final quality scores and recommendations

## Troubleshooting

### Common Issues

**API Rate Limits**: The pipeline includes retry logic and rate limiting
**Invalid Responses**: Built-in validation ensures proper JSON responses
**GitHub Permissions**: Ensure your token has proper repository access

### Logs

Check workflow logs for detailed error information:
- Initialization and API client setup
- Stage-by-stage processing details
- Error handling and retry attempts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review workflow logs
- Ensure all API keys are properly configured
- Verify repository permissions