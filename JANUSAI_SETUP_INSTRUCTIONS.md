# JanusAI_V2 Multi-LLM Pipeline Setup Instructions

## Quick Setup for Your Repository

### 1. Add the Workflow File

Copy the `multi-llm-pipeline.yml` file to your repository:

```bash
# In your JanusAI_V2 repository
mkdir -p .github/workflows
cp multi-llm-pipeline.yml .github/workflows/
```

### 2. Add Required Secrets

Go to https://github.com/Mklevns/JanusAI_V2/settings/secrets/actions

Add these repository secrets:

**Required API Keys:**
- `OPENAI_API_KEY` - Your OpenAI API key (for ChatGPT)
- `ANTHROPIC_API_KEY` - Your Anthropic API key (for Claude)
- `GEMINI_API_KEY` - Your Google Gemini API key
- `DEEPSEEK_API_KEY` - Your DeepSeek API key

**How to get these keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google Gemini**: https://aistudio.google.com/app/apikey
- **DeepSeek**: https://platform.deepseek.com/

### 3. Test the Setup

Once you've added the secrets:

1. Create a new branch in your repository
2. Make a small code change (add a comment to any Python file)
3. Create a pull request
4. The Multi-LLM Pipeline will automatically run

### 4. What the Pipeline Does for JanusAI_V2

The workflow is specifically configured for your multimodal AI project:

**Analysis Focus:**
- Model architecture optimization
- Training pipeline stability
- Vision-language integration issues
- Memory and GPU utilization
- Multimodal processing efficiency
- Numerical stability in computations

**File Types Analyzed:**
- Python files (.py)
- Jupyter notebooks (.ipynb)
- Configuration files (.yaml, .json, .toml)
- Requirements and setup files
- Documentation files

**AI Models Used:**
1. **Gemini** - Deep code analysis and architecture review
2. **ChatGPT** - Code improvements and optimization suggestions
3. **Claude** - Integration and consistency checking
4. **DeepSeek** - Final verification and quality assurance

### 5. Expected Results

After each pull request, you'll see:
- Detailed analysis comments on your PR
- Specific suggestions for your multimodal AI code
- Performance optimization recommendations
- Potential bug identification
- Architecture improvement suggestions

### 6. Manual Testing (Optional)

You can also test the pipeline locally:

```bash
export GITHUB_TOKEN="your_github_token"
export REPOSITORY="Mklevns/JanusAI_V2"
export PR_NUMBER="1"  # Replace with actual PR number

python main.py
```

## Customization for JanusAI_V2

The workflow includes special configuration for your project:

```yaml
PROJECT_TYPE: "ai_ml"
focus_areas:
  - model_architecture
  - training_stability
  - multimodal_integration
  - gpu_utilization
```

This ensures the AI models focus on aspects most relevant to your multimodal AI research.

## Troubleshooting

**If the workflow fails:**
1. Check that all 4 API keys are correctly added as secrets
2. Verify the API keys have sufficient credits/quota
3. Check the Actions tab for detailed error logs

**Common issues:**
- API rate limits: Wait a few minutes and retry
- Invalid API keys: Double-check the key format and permissions
- Repository permissions: Ensure the workflow has write access to pull requests

## Support

The pipeline is designed to help with your multimodal AI development by providing automated code quality analysis focused on the unique challenges of training and deploying vision-language models.