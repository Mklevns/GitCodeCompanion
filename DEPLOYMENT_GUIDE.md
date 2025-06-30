# Multi-LLM Pipeline Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Multi-LLM Code Quality Pipeline with advanced LangChain-inspired workflow management. The system includes GitPython integration, customizable prompts, and sophisticated orchestration capabilities.

## System Architecture

The deployed pipeline includes:

- **Core Pipeline**: 4-stage LLM gauntlet (Gemini → ChatGPT → Claude → DeepSeek)
- **Advanced Workflow Management**: LangChain-inspired orchestration with memory and conditional logic
- **GitPython Integration**: Direct repository interaction and GitHub API management
- **Customizable Prompts**: Project-specific optimization system
- **Command-Line Interface**: Easy configuration and management tools

## Prerequisites

### Required API Keys

The pipeline requires API keys for all four LLM providers:

```bash
# Required environment variables
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
GITHUB_TOKEN=your_github_token_here
REPOSITORY=owner/repository_name
```

### System Requirements

- Python 3.11+
- Git repository access
- GitHub repository permissions (for PR integration)
- Minimum 2GB RAM for concurrent LLM processing

## Quick Start Deployment

### 1. Clone and Setup

```bash
# Repository is already set up with all dependencies
cd /path/to/multi-llm-pipeline
```

### 2. Configure API Keys

Add your API keys to the environment:

```bash
# For production deployment
export OPENAI_API_KEY="your_key_here"
export ANTHROPIC_API_KEY="your_key_here" 
export GEMINI_API_KEY="your_key_here"
export DEEPSEEK_API_KEY="your_key_here"
export GITHUB_TOKEN="your_token_here"
export REPOSITORY="owner/repo_name"
```

### 3. Test the Pipeline

#### Basic Pipeline Test
```bash
python demo_mode.py
```

#### Advanced Workflow Test
```bash
python advanced_pipeline_workflow.py
```

#### Prompt Customization Test
```bash
python demo_prompt_customization.py
```

### 4. Configure for Your Project

#### Set Project Type
```bash
# For AI/ML projects
python prompt_cli.py --set ai_ml

# For web development
python prompt_cli.py --set web_development

# For security-focused analysis
python prompt_cli.py --set security
```

#### View Current Configuration
```bash
python prompt_cli.py --show
python prompt_cli.py --details ai_ml
```

## GitHub Actions Integration

### Workflow File Setup

Create `.github/workflows/multi-llm-pipeline.yml`:

```yaml
name: Multi-LLM Code Quality Pipeline

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  multi-llm-analysis:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        # Dependencies are managed via pyproject.toml
    
    - name: Set project type (customize for your project)
      run: python prompt_cli.py --set ai_ml
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
    
    - name: Run Multi-LLM Pipeline
      run: python main.py
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        REPOSITORY: ${{ github.repository }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        PR_NUMBER: ${{ github.event.pull_request.number }}
    
    - name: Run Advanced Workflow (Optional)
      run: python advanced_pipeline_workflow.py
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        REPOSITORY: ${{ github.repository }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        PR_NUMBER: ${{ github.event.pull_request.number }}
```

### GitHub Secrets Configuration

In your GitHub repository settings, add these secrets:

1. `OPENAI_API_KEY` - Your OpenAI API key
2. `ANTHROPIC_API_KEY` - Your Anthropic API key  
3. `GEMINI_API_KEY` - Your Google Gemini API key
4. `DEEPSEEK_API_KEY` - Your DeepSeek API key
5. `GITHUB_TOKEN` - GitHub token (usually auto-provided)

## Local Development Setup

### For Development and Testing

```bash
# Run in demo mode (no GitHub integration required)
python demo_mode.py

# Test prompt customization
python demo_prompt_customization.py

# Test advanced workflow
python advanced_pipeline_workflow.py

# Interactive prompt management
python prompt_cli.py --customize
```

### Local Testing with GitHub Integration

```bash
# Set up environment for local testing
export GITHUB_TOKEN="your_personal_access_token"
export REPOSITORY="your_username/your_repo"
export PR_NUMBER="123"  # Specific PR to test

# Run pipeline
python main.py
```

## Production Deployment Options

### Option 1: GitHub Actions (Recommended)

Automatically triggers on PR events and posts results as comments.

**Pros:**
- Seamless GitHub integration
- No server maintenance required
- Scalable with GitHub infrastructure

**Cons:**
- Limited to GitHub-hosted projects
- Runtime limits in GitHub Actions

### Option 2: Self-Hosted Server

Deploy on your own infrastructure for maximum control.

**Requirements:**
- Server with Python 3.11+
- Webhook endpoint for GitHub events
- SSL certificate for HTTPS webhooks

**Setup:**
```bash
# Install production dependencies
pip install gunicorn

# Create webhook server (custom implementation needed)
# Configure GitHub webhook to POST to your server
# Process webhook events and trigger pipeline
```

### Option 3: Cloud Functions

Deploy individual stages as serverless functions.

**Benefits:**
- Cost-effective for sporadic usage
- Auto-scaling
- Managed infrastructure

**Platforms:**
- AWS Lambda
- Google Cloud Functions
- Azure Functions

## Configuration Management

### Project-Specific Prompts

#### AI/ML Projects (like JanusAI_V2)
```bash
python prompt_cli.py --set ai_ml
python prompt_cli.py --details ai_ml
```

Focus areas:
- Model architecture issues
- Training stability
- Data processing bugs
- Numerical stability
- Performance bottlenecks

#### Web Development Projects
```bash
python prompt_cli.py --set web_development
```

Focus areas:
- XSS and CSRF vulnerabilities
- API security
- Performance bottlenecks
- Accessibility issues
- SEO problems

#### Custom Project Types
```bash
python prompt_cli.py --create-custom
# Follow interactive prompts to create specialized configuration
```

### Team Configuration Sharing

```bash
# Export team configuration
python prompt_cli.py --export team_config.json

# Import on other machines/CI
python prompt_cli.py --import team_config.json
```

## Monitoring and Maintenance

### Pipeline Performance Monitoring

The pipeline provides comprehensive logging and metrics:

```bash
# View execution history
python -c "
from advanced_pipeline_workflow import AdvancedMultiLLMPipeline
pipeline = AdvancedMultiLLMPipeline(demo_mode=True)
history = pipeline.get_execution_history()
for exec in history[-5:]:
    print(f'{exec[\"execution_id\"]}: {exec[\"status\"]} - {exec.get(\"total_duration\", 0):.2f}s')
"
```

### Log Analysis

Pipeline logs are structured and include:
- Execution timestamps
- Stage completion times
- API response quality metrics
- Error tracking and retry attempts

### Resource Usage

Monitor API usage across providers:
- OpenAI: GPT-4o for code generation
- Anthropic: Claude Sonnet 4 for integration
- Google: Gemini 2.5 Pro for analysis
- DeepSeek: For final verification

## Troubleshooting

### Common Issues

#### API Key Problems
```bash
# Test individual API connections
python -c "
from llm_clients import LLMClients
clients = LLMClients()
print('All clients initialized successfully')
"
```

#### GitHub Integration Issues
```bash
# Test GitHub connection
python -c "
from git_github_utils import GitHubManager
try:
    github = GitHubManager()
    print('GitHub connection successful')
except Exception as e:
    print(f'GitHub error: {e}')
"
```

#### Workflow Execution Problems
```bash
# Test workflow components
python -c "
from langchain_workflow import WorkflowOrchestrator
orchestrator = WorkflowOrchestrator()
stats = orchestrator.get_workflow_stats()
print(f'Workflow stats: {stats}')
"
```

### Performance Optimization

#### Rate Limiting
The pipeline includes built-in rate limiting for all LLM providers. Adjust in `llm_clients.py` if needed.

#### Memory Management
Workflow memory automatically evicts old entries. Configure size in `WorkflowMemory(max_entries=1000)`.

#### Parallel Processing
For large PRs, consider implementing parallel file analysis (requires custom modification).

## Security Considerations

### API Key Security
- Never commit API keys to version control
- Use GitHub Secrets for CI/CD
- Rotate keys regularly
- Monitor API usage for anomalies

### Input Sanitization
The pipeline includes security utilities in `security_utils.py`:
- Code injection prevention
- Input validation
- Safe file path handling

### Network Security
- Use HTTPS for all external API calls
- Validate webhook signatures in production
- Implement IP whitelisting if needed

## Advanced Features

### LangChain Workflow Management

The advanced pipeline includes:

- **Memory Management**: Persistent storage of analysis results
- **Conditional Logic**: Quality gates and retry mechanisms
- **Workflow Visualization**: Graph-based execution flow
- **Error Recovery**: Automatic retry with exponential backoff

#### Usage Example
```python
from advanced_pipeline_workflow import AdvancedMultiLLMPipeline
import asyncio

async def main():
    pipeline = AdvancedMultiLLMPipeline(demo_mode=False)
    results = await pipeline.run_advanced_pipeline(pr_number=123)
    print(f"Pipeline completed: {results['success']}")

asyncio.run(main())
```

### Custom Workflow Creation

```python
from langchain_workflow import WorkflowOrchestrator, WorkflowContext

# Create custom workflow
orchestrator = WorkflowOrchestrator()

# Add custom nodes
orchestrator.create_llm_node(
    node_id="custom_analysis",
    name="Custom Code Analysis",
    llm_function=your_custom_function,
    system_prompt="Your custom system prompt"
)

# Execute workflow
context = WorkflowContext(data={"input": "data"}, ...)
result = await orchestrator.execute_workflow("custom_analysis", context)
```

## Support and Updates

### Getting Help

1. Check this deployment guide
2. Review the README.md for architecture details
3. Examine demo scripts for usage examples
4. Check logs for specific error messages

### Version Updates

The pipeline is designed for easy updates:

```bash
# Update dependencies
uv sync

# Test after updates
python demo_mode.py
python advanced_pipeline_workflow.py
```

### Contributing

When contributing:
1. Test all four pipeline stages
2. Verify prompt customization works
3. Check advanced workflow execution
4. Update documentation as needed

## Conclusion

This deployment guide provides everything needed to successfully deploy and operate the Multi-LLM Pipeline with advanced workflow management. The system is production-ready and includes comprehensive monitoring, security, and customization capabilities.

For questions or issues, refer to the documentation files and demo scripts included in the repository.